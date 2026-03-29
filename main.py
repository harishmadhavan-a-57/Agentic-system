# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
from loguru import logger
import uvicorn

from tools.registry_setup import setup_registry
from agents.router import route_domain
from agents.planner import plan_steps
from agents.tool_selector import select_tool
from agents.executor import execute
from agents.responder import format_response
from memory.session_store import session_store

# Setup on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Agentic System...")
    setup_registry()
    logger.info("Tool registry initialized.")
    yield
    logger.info("Shutting down.")

app = FastAPI(
    title="Agentic System",
    description="Scalable AI agent with 100+ tool support",
    lifespan=lifespan
)

class ChatRequest(BaseModel):
    query: str
    session_id: str = "default"

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        query = req.query
        session_id = req.session_id
        
        logger.info(f"[{session_id}] Query: {query}")
        
        # Get session context (carries invoiceId, etc. between requests)
        context = session_store.get_context(session_id)
        
        # Stage 1: Route to domain
        domain = route_domain(query)
        
        # Stage 2: Plan steps
        steps = plan_steps(query, domain)
        
        results = []
        for step in steps:
            # Stage 3: Select tool (semantic search)
            tool = select_tool(step["action"], step["domain"])
            
            if not tool:
                results.append({"error": f"No tool found for action: {step['action']}"})
                continue
            
            # Stage 4: Execute
            result = await execute(tool, query, context)
            
            # Pass context forward (e.g., invoiceId from create to send)
            if isinstance(result, dict):
                if "invoiceId" in result:
                    context["invoiceId"] = result["invoiceId"]
                    session_store.update_context(session_id, context)
            
            results.append({"tool": tool.name, "result": result})
        
        # Stage 5: Format response
        response = format_response(query, steps, results)
        
        return {
            "query": query,
            "domain": domain,
            "steps": steps,
            "results": results,
            "response": response
        }
    
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tools")
def get_tools():
    """See all registered tools"""
    from tools.registry import registry
    return registry.summary()

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)