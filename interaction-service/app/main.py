from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

app = FastAPI(title="Interaction Service")

# Enums
class InteractionType(str, Enum):
    CALL = "call"
    EMAIL = "email"
    MEETING = "meeting"
    NOTE = "note"

class InteractionStatus(str, Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

# Models
class InteractionBase(BaseModel):
    customer_id: int
    type: InteractionType
    subject: str
    description: Optional[str] = None
    status: InteractionStatus = InteractionStatus.SCHEDULED
    scheduled_date: Optional[datetime] = None

class InteractionCreate(InteractionBase):
    pass

class Interaction(InteractionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# In-memory database
interactions_db = []
interaction_id_counter = 1

@app.get("/")
async def root():
    return {"service": "Interaction Service", "status": "running"}

@app.get("/interactions", response_model=List[Interaction])
async def get_interactions(
    customer_id: Optional[int] = None,
    type: Optional[InteractionType] = None,
    status: Optional[InteractionStatus] = None
):
    filtered_interactions = interactions_db
    
    if customer_id:
        filtered_interactions = [i for i in filtered_interactions if i["customer_id"] == customer_id]
    if type:
        filtered_interactions = [i for i in filtered_interactions if i["type"] == type]
    if status:
        filtered_interactions = [i for i in filtered_interactions if i["status"] == status]
    
    return filtered_interactions

@app.get("/interactions/{interaction_id}", response_model=Interaction)
async def get_interaction(interaction_id: int):
    for interaction in interactions_db:
        if interaction["id"] == interaction_id:
            return interaction
    raise HTTPException(status_code=404, detail="Interaction not found")

@app.post("/interactions", response_model=Interaction, status_code=201)
async def create_interaction(interaction: InteractionCreate):
    global interaction_id_counter
    
    new_interaction = {
        "id": interaction_id_counter,
        "customer_id": interaction.customer_id,
        "type": interaction.type,
        "subject": interaction.subject,
        "description": interaction.description,
        "status": interaction.status,
        "scheduled_date": interaction.scheduled_date,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    
    interactions_db.append(new_interaction)
    interaction_id_counter += 1
    
    return new_interaction

@app.put("/interactions/{interaction_id}", response_model=Interaction)
async def update_interaction(interaction_id: int, interaction: InteractionCreate):
    for idx, existing_interaction in enumerate(interactions_db):
        if existing_interaction["id"] == interaction_id:
            updated_interaction = {
                "id": interaction_id,
                "customer_id": interaction.customer_id,
                "type": interaction.type,
                "subject": interaction.subject,
                "description": interaction.description,
                "status": interaction.status,
                "scheduled_date": interaction.scheduled_date,
                "created_at": existing_interaction["created_at"],
                "updated_at": datetime.utcnow(),
            }
            interactions_db[idx] = updated_interaction
            return updated_interaction
    
    raise HTTPException(status_code=404, detail="Interaction not found")

@app.patch("/interactions/{interaction_id}/status")
async def update_interaction_status(interaction_id: int, status: InteractionStatus):
    for idx, interaction in enumerate(interactions_db):
        if interaction["id"] == interaction_id:
            interactions_db[idx]["status"] = status
            interactions_db[idx]["updated_at"] = datetime.utcnow()
            return {"message": "Status updated successfully", "new_status": status}
    
    raise HTTPException(status_code=404, detail="Interaction not found")

@app.delete("/interactions/{interaction_id}")
async def delete_interaction(interaction_id: int):
    for idx, interaction in enumerate(interactions_db):
        if interaction["id"] == interaction_id:
            interactions_db.pop(idx)
            return {"message": "Interaction deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Interaction not found")
