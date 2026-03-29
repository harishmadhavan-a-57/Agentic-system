import httpx
import os
from loguru import logger

BASE_URL = os.getenv("PAYPAL_BASE_URL", "https://api-m.sandbox.paypal.com")

async def _get_token() -> str:
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{BASE_URL}/v1/oauth2/token",
            data={"grant_type": "client_credentials"},
            auth=(os.getenv("PAYPAL_CLIENT_ID"), os.getenv("PAYPAL_SECRET")),
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        return r.json()["access_token"]

async def _paypal(method: str, url: str, data: dict = None):
    token = await _get_token()
    async with httpx.AsyncClient() as client:
        r = await client.request(
            method, f"{BASE_URL}{url}",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json=data
        )
        return r.json()

async def create_invoice(amount: str = "10", **kwargs):
    result = await _paypal("POST", "/v2/invoicing/invoices", {
        "detail": {"currency_code": "USD"},
        "invoicer": {"name": {"given_name": "Agent", "surname": "System"},
                     "email_address": "sb-seller@business.example.com"},
        "primary_recipients": [{"billing_info": {
            "name": {"given_name": "John", "surname": "Doe"},
            "email_address": "sb-buyer@personal.example.com"
        }}],
        "items": [{"name": "Service", "quantity": "1",
                   "unit_amount": {"currency_code": "USD", "value": str(amount)}}]
    })
    invoice_id = result.get("href", "").split("/").pop()
    return {"message": "Invoice created", "invoiceId": invoice_id, "amount": amount}

async def send_invoice(invoiceId: str = None, **kwargs):
    if not invoiceId:
        return {"error": "No invoiceId available. Create an invoice first."}
    await _paypal("POST", f"/v2/invoicing/invoices/{invoiceId}/send", {"send_to_invoicer": True})
    return {"message": "Invoice sent", "invoiceId": invoiceId}

async def list_invoices(**kwargs):
    result = await _paypal("GET", "/v2/invoicing/invoices")
    return result.get("items", [])[:5]

async def get_balance(**kwargs):
    return await _paypal("GET", "/v1/reporting/balances")

async def list_transactions(**kwargs):
    return await _paypal("GET", "/v1/reporting/transactions")