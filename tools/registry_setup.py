from tools.registry import registry, Tool
from tools.paypal_tools import create_invoice, send_invoice, list_invoices, get_balance, list_transactions
from tools.ecommerce_tools import get_products, get_product, get_categories, get_products_by_category
from tools.rag_tool import rag_tool
from tools.system_tool import list_tools_handler, get_logs_handler

def setup_registry():
    """Register all tools. Called once at startup."""
    
    # PayPal tools
    registry.register(Tool(
        name="paypal.create_invoice",
        action="create_invoice",
        domain="paypal",
        description="Create a new PayPal invoice for a given dollar amount",
        handler=create_invoice,
        parameters=["amount"]
    ))
    registry.register(Tool(
        name="paypal.send_invoice",
        action="send_invoice",
        domain="paypal",
        description="Send an existing PayPal invoice to the recipient by invoice ID",
        handler=send_invoice,
        parameters=["invoiceId"]
    ))
    registry.register(Tool(
        name="paypal.list_invoices",
        action="list_invoices",
        domain="paypal",
        description="List all PayPal invoices in the account",
        handler=list_invoices,
        parameters=[]
    ))
    registry.register(Tool(
        name="paypal.get_balance",
        action="get_balance",
        domain="paypal",
        description="Get the current PayPal account balance",
        handler=get_balance,
        parameters=[]
    ))
    registry.register(Tool(
        name="paypal.list_transactions",
        action="list_transactions",
        domain="paypal",
        description="List recent PayPal transactions and payment history",
        handler=list_transactions,
        parameters=[]
    ))
    
    # RAG tool
    registry.register(Tool(
        name="knowledge.rag_answer",
        action="rag_answer",
        domain="knowledge",
        description="Answer general questions using the knowledge base",
        handler=rag_tool.answer,
        parameters=[]
    ))
    
    # System tools
    registry.register(Tool(
        name="system.list_tools",
        action="list_tools",
        domain="system",
        description="List all available tools and their capabilities",
        handler=list_tools_handler,
        parameters=[]
    ))