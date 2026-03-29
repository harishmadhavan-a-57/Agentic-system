from collections import defaultdict
from datetime import datetime

class SessionStore:
    """
    Stores context between requests for the same session.
    Example: invoiceId created in request 1 is available in request 2.
    In production this would be Redis.
    """
    def __init__(self):
        self._store = defaultdict(lambda: {"context": {}, "history": []})
    
    def get_context(self, session_id: str) -> dict:
        return self._store[session_id]["context"].copy()
    
    def update_context(self, session_id: str, context: dict):
        self._store[session_id]["context"].update(context)
    
    def add_to_history(self, session_id: str, query: str, response: str):
        self._store[session_id]["history"].append({
            "query": query,
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_history(self, session_id: str) -> list:
        return self._store[session_id]["history"]

session_store = SessionStore()