from sentence_transformers import SentenceTransformer
import numpy as np
from tools.registry import registry, Tool
from loguru import logger
from typing import Optional

# Load embedding model once
_embedder = None

def get_embedder():
    global _embedder
    if _embedder is None:
        logger.info("Loading sentence embedder...")
        _embedder = SentenceTransformer("all-MiniLM-L6-v2")
        logger.info("Embedder loaded.")
    return _embedder

def select_tool(action: str, domain: str) -> Optional[Tool]:
    """
    Find the best tool for an action within a domain.
    
    Strategy:
    1. Try exact action name match first (fast)
    2. If not found, use semantic similarity (smart)
    3. Fallback to first tool in domain
    """
    
    # 1. Exact match
    tool = registry.get_by_action(action)
    if tool and tool.domain == domain:
        logger.info(f"Exact match found: {tool.name}")
        return tool
    
    # 2. Semantic search within domain tools
    domain_tools = registry.get_by_domain(domain)
    if not domain_tools:
        logger.warning(f"No tools found for domain: {domain}")
        return None
    
    embedder = get_embedder()
    
    # Embed the action we're looking for
    query_vec = embedder.encode(action, convert_to_numpy=True)
    
    # Embed all tool descriptions in this domain
    descriptions = [f"{t.action}: {t.description}" for t in domain_tools]
    tool_vecs = embedder.encode(descriptions, convert_to_numpy=True)
    
    # Cosine similarity
    similarities = np.dot(tool_vecs, query_vec) / (
        np.linalg.norm(tool_vecs, axis=1) * np.linalg.norm(query_vec) + 1e-8
    )
    
    best_idx = int(np.argmax(similarities))
    best_score = similarities[best_idx]
    
    logger.info(f"Semantic match: {domain_tools[best_idx].name} (score: {best_score:.3f})")
    
    # If similarity is too low, it's probably wrong
    if best_score < 0.3:
        logger.warning(f"Low similarity score {best_score:.3f}, using fallback")
        return domain_tools[0]
    
    return domain_tools[best_idx]