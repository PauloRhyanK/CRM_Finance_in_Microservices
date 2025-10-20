from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

app = FastAPI(title="Product Service")

# Models
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None
    stock_quantity: int = 0

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# In-memory database
products_db = []
product_id_counter = 1

@app.get("/")
async def root():
    return {"service": "Product Service", "status": "running"}

@app.get("/products", response_model=List[Product])
async def get_products(category: Optional[str] = None):
    if category:
        return [p for p in products_db if p.get("category") == category]
    return products_db

@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int):
    for product in products_db:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/products", response_model=Product, status_code=201)
async def create_product(product: ProductCreate):
    global product_id_counter
    
    new_product = {
        "id": product_id_counter,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "category": product.category,
        "stock_quantity": product.stock_quantity,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    
    products_db.append(new_product)
    product_id_counter += 1
    
    return new_product

@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, product: ProductCreate):
    for idx, existing_product in enumerate(products_db):
        if existing_product["id"] == product_id:
            updated_product = {
                "id": product_id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "category": product.category,
                "stock_quantity": product.stock_quantity,
                "created_at": existing_product["created_at"],
                "updated_at": datetime.utcnow(),
            }
            products_db[idx] = updated_product
            return updated_product
    
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    for idx, product in enumerate(products_db):
        if product["id"] == product_id:
            products_db.pop(idx)
            return {"message": "Product deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Product not found")

@app.patch("/products/{product_id}/stock")
async def update_stock(product_id: int, quantity: int):
    for idx, product in enumerate(products_db):
        if product["id"] == product_id:
            products_db[idx]["stock_quantity"] = quantity
            products_db[idx]["updated_at"] = datetime.utcnow()
            return {"message": "Stock updated successfully", "new_stock": quantity}
    
    raise HTTPException(status_code=404, detail="Product not found")
