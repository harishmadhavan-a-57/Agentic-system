import re
from tools.registry import Tool
from loguru import logger
from typing import Any

def extract_parameters(query: str, tool: Tool) -> dict:
    params = {}

    if "amount" in tool.parameters:
        match = re.search(r'\$?(\d+(?:\.\d{2})?)', query)
        params["amount"] = match.group(1) if match else "10.00"

    if "email" in tool.parameters:
        match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', query)
        params["email"] = match.group(0) if match else None

    if "category" in tool.parameters:
        categories = ["electronics", "jewelery", "men's clothing", "women's clothing"]
        q = query.lower()
        for cat in categories:
            if cat.split("'")[0] in q:
                params["category"] = cat
                break
        if "category" not in params:
            params["category"] = "electronics"

    return params

async def execute(tool: Tool, query: str, context: dict = {}) -> Any:
    try:
        params = extract_parameters(query, tool)
        all_params = {**params, **context}

        # ✅ Always pass query — RAG and other tools need it
        all_params["query"] = query

        logger.info(f"Executing tool: {tool.name} with params: {all_params}")

        result = await tool.handler(**all_params)

        logger.info(f"Tool result: {str(result)[:100]}...")
        return result

    except Exception as e:
        logger.error(f"Tool execution failed: {tool.name} - {e}")
        return {"error": str(e), "tool": tool.name}