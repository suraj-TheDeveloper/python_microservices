import os
import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI()

PRODUCT_SERVICE_URL = os.environ.get(
    "PRODUCT_SERVICE_URL",
    "http://127.0.0.1:8001"
)


@app.post("/orders/{product_id}")
def create_order(product_id: int):

    try:
        response = httpx.get(f"{PRODUCT_SERVICE_URL}/api/products/{product_id}/", timeout=5.0)

        response.raise_for_status()
        product = response.json()

    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Product not found. Order cannot be created.")

        raise HTTPException(status_code=502, detail="Product Service returned an error.")

    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Product Service is unavailable.")

    return { "message": "Order created successfully", "product": product, "quantity": 1, "total_price": float(product["price"])}