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
    {"id": 1, "name": "Laptop", "price": 1200, "price_ngn": 345000, "image": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400"},
    {"id": 2, "name": "Phone", "price": 800, "price_ngn": 620000, "image": "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400"},
    {"id": 3, "name": "Headphones", "price": 150, "price_ngn": 185000, "image": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=400"}
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
