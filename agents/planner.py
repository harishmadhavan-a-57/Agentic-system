from utils.llm import ask_llm
from loguru import logger
import re

def plan_steps(query: str, domain: str) -> list[dict]:
    """
    Figure out what sequence of actions to take.
    Example: "Create invoice for $50 and send it" 
    → [create_invoice, send_invoice]
    """
    
    prompt = f"""You are a task planner for an AI agent.
Given a user query and its domain, list the actions needed in order.

Domain: {domain}

Available actions per domain:
- paypal: create_invoice, send_invoice, list_invoices, get_balance, list_transactions
- ecommerce: get_products, get_product, get_categories, get_products_by_category, get_carts
- knowledge: rag_answer
- system: list_tools, get_logs

Query: "{query}"

List the actions needed, one per line, in order. Use only action names from the list above.
Actions:"""

    result = ask_llm(prompt)
    
    # Parse the LLM output into a list
    lines = [line.strip().lower() for line in result.strip().split("\n")]
    
    steps = []
    valid_actions = [
        "create_invoice", "send_invoice", "list_invoices", "get_balance",
        "list_transactions", "get_products", "get_product", "get_categories",
        "get_products_by_category", "get_carts", "rag_answer", "list_tools", "get_logs"
    ]
    
    for i, line in enumerate(lines):
        # Clean up — LLM might output "1. create_invoice" or "- create_invoice"
        action = re.sub(r'^[\d\.\-\*\s]+', '', line).strip()
        if action in valid_actions:
            steps.append({"step": i + 1, "action": action, "domain": domain})
    
    if not steps:
        # Default fallback
        logger.warning("Planner found no valid steps, defaulting to rag_answer")
        return [{"step": 1, "action": "rag_answer", "domain": "knowledge"}]
    
    logger.info(f"Planned steps: {[s['action'] for s in steps]}")
    return steps