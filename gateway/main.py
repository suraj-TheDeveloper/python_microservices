import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Microservices API Gateway")

PRODUCT_SERVICE_URL = "http://product_service:8001"
ORDER_SERVICE_URL = "http://order_service:8002"


@app.get("/")
def home():
    return {"message": "API Gateway is running"}


@app.get("/api/products/{product_id}/")
def get_product(product_id: int):
    try:
        response = httpx.get(
            f"{PRODUCT_SERVICE_URL}/api/products/{product_id}/",
            timeout=5.0,
        )
        response.raise_for_status()
        return response.json()

    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Product not found")
        raise HTTPException(status_code=502, detail="Product Service error")

    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Product Service is unavailable",
        )


@app.post("/api/orders/{product_id}")
def create_order(product_id: int):
    try:
        response = httpx.post(
            f"{ORDER_SERVICE_URL}/orders/{product_id}",
            timeout=10.0,
        )
        response.raise_for_status()
        return response.json()

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=exc.response.json().get("detail", "Order Service error"),
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Order Service is unavailable",
        )
