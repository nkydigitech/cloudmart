from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

products = [
    {"id": 1, "name": "Laptop", "price": 999.99},
    {"id": 2, "name": "Phone", "price": 499.99},
    {"id": 3, "name": "Headphones", "price": 99.99}
]

@app.get("/")
def root():
    return {"service": "product-service", "status": "running", "version": "v1"}

@app.get("/products")
def get_products():
    return products

@app.get("/api/products")
def get_api_products():
    return products

@app.get("/health")
def health():
    return {"status": "healthy"}
