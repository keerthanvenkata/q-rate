from pydantic import BaseModel, Field
from typing import Optional

class VisitCreate(BaseModel):
    phone_number: str
    bill_id: str
    bill_amount: float
    verbal_consent: bool
    customer_name: Optional[str] = None
    guest_count: int = 1
    # In V1, we'd pass cafe_id in header or auth token
    
class VisitResponse(BaseModel):
    id: int
    status: str
