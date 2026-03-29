from utils.llm import ask_llm
from loguru import logger

DOMAINS = ["paypal", "ecommerce", "knowledge", "system"]

def route_domain(query: str) -> str:
    """
    Classify which domain this query belongs to.
    We use LLM for this — smarter than keyword matching.
    """
    
    prompt = f"""You are a query router for an AI assistant.
Classify the following user query into exactly one domain.

Domains:
- paypal: anything about invoices, payments, transactions, balance, sending money, disputes
- ecommerce: anything about products, shopping, categories, carts, store items
- knowledge: general questions, definitions, explanations, "what is", "how does"
- system: questions about the system itself, available tools, capabilities, logs

Query: "{query}"

Reply with ONLY one word from: paypal, ecommerce, knowledge, system
Answer:"""

    result = ask_llm(prompt).lower().strip()
    
    # Validate — LLM might hallucinate
    if result not in DOMAINS:
        logger.warning(f"LLM returned invalid domain '{result}', defaulting to 'knowledge'")
        # Fallback: keyword matching as safety net
        q = query.lower()
        if any(w in q for w in ["invoice", "payment", "balance", "transaction"]):
            return "paypal"
        if any(w in q for w in ["product", "shop", "category", "cart"]):
            return "ecommerce"
        if any(w in q for w in ["tool", "capability", "system", "available"]):
            return "system"
        return "knowledge"
    
    logger.info(f"Query routed to domain: {result}")
    return result