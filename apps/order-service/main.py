from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import psycopg2
import os
from datetime import datetime

app = FastAPI(title="CloudMart Order Service", version="1.0")

# DB Config from env / secret
DB_HOST = os.getenv("DB_HOST", "postgres-service.dev.svc.cluster.local")
DB_NAME = os.getenv("DB_NAME", "cloudmartdb")
DB_USER = os.getenv("DB_USER", "cloudmart")
DB_PASS = os.getenv("DB_PASS", "cloudmart123")

def get_conn():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)

# Init table
def init_db():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            user_email VARCHAR(255),
            user_name VARCHAR(255),
            total INTEGER,
            items JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Orders table ready")
    except Exception as e:
        print(f"DB init error: {e}")

@app.on_event("startup")
def startup():
    init_db()

class OrderCreate(BaseModel):
    user_email: str
    user_name: str
    total: int
    items: List[dict]

class OrderResponse(BaseModel):
    id: int
    user_email: str
    user_name: str
    total: int
    items: List[dict]
    created_at: datetime

@app.get("/")
def root():
    return {"service": "order-service", "status": "running", "db": DB_HOST}

@app.get("/health")
def health():
    try:
        conn = get_conn()
        conn.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/orders", response_model=OrderResponse)
def create_order(order: OrderCreate):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO orders (user_email, user_name, total, items) VALUES (%s,%s,%s,%s) RETURNING id, created_at",
            (order.user_email, order.user_name, order.total, psycopg2.extras.Json(order.items))
        )
        id, created_at = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return {"id": id, "user_email": order.user_email, "user_name": order.user_name, "total": order.total, "items": order.items, "created_at": created_at}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/orders")
def list_orders():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, user_email, user_name, total, items, created_at FROM orders ORDER BY created_at DESC LIMIT 50")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [{"id": r[0], "user_email": r[1], "user_name": r[2], "total": r[3], "items": r[4], "created_at": r[5]} for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# For /api/orders compatibility
@app.get("/api/orders")
def api_orders():
    return list_orders()

import psycopg2.extras
