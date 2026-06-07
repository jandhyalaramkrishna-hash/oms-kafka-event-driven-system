from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from typing import List
from app.producer import send_to_kafka

app = FastAPI()

# ------------------ MODELS ------------------

class Customer(BaseModel):
    customer_id: str = Field(..., min_length=1)
    full_name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=1)

class Item(BaseModel):
    sku: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    quantity: int
    unit_price: float

class Payload(BaseModel):
    order_id: str = Field(..., min_length=1)
    customer: Customer
    items: List[Item]

    # STRICT VALIDATION (IMPORTANT)
    @validator("order_id")
    def order_id_not_blank(cls, v):
        if not v.strip():
            raise ValueError("order_id cannot be empty or blank")
        return v

class OrderRequest(BaseModel):
    metadata: dict
    payload: Payload

# ------------------ API ------------------

processed_orders = set()  # for idempotency

@app.post("/orders")
def create_order(order: OrderRequest):
    if not order.payload.order_id.strip():
        raise HTTPException(status_code=400, detail="Order ID cannot be empty")

    order_id = order.payload.order_id

    # Duplicate check
    if order_id in processed_orders:
        raise HTTPException(status_code=409, detail="Duplicate order")

    processed_orders.add(order_id)

    # Send to Kafka
    send_to_kafka(order.dict())

    return {
        "message": "Order sent to Kafka",
        "order_id": order_id
    }