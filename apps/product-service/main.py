from fastapi import FastAPI
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

app = FastAPI()
REQUESTS = Counter('product_requests_total', 'Total product requests')

@app.get("/")
def root():
    REQUESTS.inc()
    return {"service": "product-service", "status": "running", "version": "v1"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/products")
def products():
    REQUESTS.inc()
    return [
        {"id": 1, "name": "Laptop", "price": 1200},
        {"id": 2, "name": "Phone", "price": 800},
        {"id": 3, "name": "Headphones", "price": 150}
    ]
