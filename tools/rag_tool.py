from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from loguru import logger

KNOWLEDGE_BASE = [
    "An invoice is a document issued by a seller to a buyer requesting payment for goods or services.",
    "PayPal is an online payment platform that lets users send and receive money digitally.",
    "A transaction is a completed exchange of money between two parties.",
    "Account balance refers to the amount of money currently available in a PayPal account.",
    "Products are items listed in the store that customers can purchase.",
    "Categories group similar products together, like electronics, clothing, or jewelery.",
    "A cart contains items a customer has selected but not yet purchased.",
    "An invoice dispute occurs when the payer contests the charges on an invoice.",
    "Sandbox mode in PayPal is a testing environment that simulates real transactions without real money.",
    "I am an AI agentic assistant that can help with PayPal operations, e-commerce product queries, and answer general knowledge questions.",
]

class RAGTool:
    def __init__(self):
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self._build_index()

    def _build_index(self):
        logger.info("Building RAG index...")
        embeddings = self.embedder.encode(KNOWLEDGE_BASE, convert_to_numpy=True)
        faiss.normalize_L2(embeddings)
        self.index = faiss.IndexFlatIP(embeddings.shape[1])
        self.index.add(embeddings)
        logger.info(f"RAG index built with {len(KNOWLEDGE_BASE)} documents")

    # ✅ Added **kwargs so extra context params don't cause errors
    async def answer(self, query: str, **kwargs) -> dict:
        q_vec = self.embedder.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(q_vec)

        scores, indices = self.index.search(q_vec, k=3)

        relevant = [KNOWLEDGE_BASE[i] for i in indices[0] if i < len(KNOWLEDGE_BASE)]
        best_score = float(scores[0][0])

        if best_score < 0.3:
            return {
                "answer": "This system handles PayPal operations and e-commerce. I cannot answer that query.",
                "confidence": "low"
            }

        return {
            "answer": " ".join(relevant[:2]),
            "confidence": "high",
            "score": round(best_score, 3)
        }

rag_tool = RAGTool()