from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Customer Service")

# Models
class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    company: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# In-memory database
customers_db = []
customer_id_counter = 1

@app.get("/")
async def root():
    return {"service": "Customer Service", "status": "running"}

@app.get("/customers", response_model=List[Customer])
async def get_customers():
    return customers_db

@app.get("/customers/{customer_id}", response_model=Customer)
async def get_customer(customer_id: int):
    for customer in customers_db:
        if customer["id"] == customer_id:
            return customer
    raise HTTPException(status_code=404, detail="Customer not found")

@app.post("/customers", response_model=Customer, status_code=201)
async def create_customer(customer: CustomerCreate):
    global customer_id_counter
    
    new_customer = {
        "id": customer_id_counter,
        "name": customer.name,
        "email": customer.email,
        "phone": customer.phone,
        "address": customer.address,
        "company": customer.company,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    
    customers_db.append(new_customer)
    customer_id_counter += 1
    
    return new_customer

@app.put("/customers/{customer_id}", response_model=Customer)
async def update_customer(customer_id: int, customer: CustomerCreate):
    for idx, existing_customer in enumerate(customers_db):
        if existing_customer["id"] == customer_id:
            updated_customer = {
                "id": customer_id,
                "name": customer.name,
                "email": customer.email,
                "phone": customer.phone,
                "address": customer.address,
                "company": customer.company,
                "created_at": existing_customer["created_at"],
                "updated_at": datetime.utcnow(),
            }
            customers_db[idx] = updated_customer
            return updated_customer
    
    raise HTTPException(status_code=404, detail="Customer not found")

@app.delete("/customers/{customer_id}")
async def delete_customer(customer_id: int):
    for idx, customer in enumerate(customers_db):
        if customer["id"] == customer_id:
            customers_db.pop(idx)
            return {"message": "Customer deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Customer not found")
