from dataclasses import dataclass, field
from typing import Callable, List, Optional
from loguru import logger

@dataclass
class Tool:
    name: str           # "paypal.create_invoice"
    action: str         # "create_invoice"  
    domain: str         # "paypal" / "ecommerce" / "knowledge" / "system"
    description: str    # Human-readable — used for semantic search
    handler: Callable   # The actual function to call
    parameters: List[str] = field(default_factory=list)  # ["amount", "email"]
    tags: List[str] = field(default_factory=list)

class ToolRegistry:
    def __init__(self):
        self._tools: List[Tool] = []
    
    def register(self, tool: Tool):
        self._tools.append(tool)
        logger.debug(f"Registered tool: {tool.name}")
    
    def get_by_domain(self, domain: str) -> List[Tool]:
        """Get all tools for a domain — used after routing"""
        return [t for t in self._tools if t.domain == domain]
    
    def get_by_action(self, action: str) -> Optional[Tool]:
        """Find exact tool by action name"""
        for t in self._tools:
            if t.action == action:
                return t
        return None
    
    def get_all(self) -> List[Tool]:
        return self._tools
    
    def summary(self) -> dict:
        """For the system_tool — what tools exist?"""
        domains = {}
        for t in self._tools:
            domains.setdefault(t.domain, []).append(t.action)
        return domains

# Global singleton — import this everywhere
registry = ToolRegistry()