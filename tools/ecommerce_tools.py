import httpx
from loguru import logger

BASE_URL = "https://fakestoreapi.com"

async def _get(url: str):
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(f"{BASE_URL}{url}")
        r.raise_for_status()
        return r.json()

async def get_products(**kwargs):
    """Get all products from the store, returns first 5"""
    data = await _get("/products")
    return data[:5]

async def get_product(product_id: int = 1, **kwargs):
    """Get a single product by ID"""
    return await _get(f"/products/{product_id}")

async def get_categories(**kwargs):
    """Get all product categories"""
    return await _get("/products/categories")

async def get_products_by_category(category: str = "electronics", **kwargs):
    """Get products filtered by category"""
    logger.info(f"Fetching products for category: {category}")
    return await _get(f"/products/category/{category}")

async def get_carts(**kwargs):
    """Get all shopping carts"""
    return await _get("/carts")