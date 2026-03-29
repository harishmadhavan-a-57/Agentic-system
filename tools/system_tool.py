from loguru import logger


async def list_tools_handler(**kwargs):
    """List all registered tools grouped by domain"""
    from tools.registry import registry
    summary = registry.summary()
    result = {}
    for domain, actions in summary.items():
        result[domain] = {
            "count": len(actions),
            "actions": actions
        }
    return {
        "message": "Here are all available tools",
        "domains": result,
        "total_tools": sum(len(v) for v in summary.values())
    }

async def get_logs_handler(**kwargs):
    """Return recent system activity (placeholder - extend with real log file reading)"""
    return {
        "message": "System is running normally",
        "log_entries": [
            "Agent system initialized",
            "Tool registry loaded",
            "Models loaded successfully"
        ]
    }