from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db
from app.models.staff import Staff
from app.schemas.staff import StaffCreate, StaffResponse

# V0 Auth: Hardcoded "Owner" Context for now
# In V0.5, this will extract cafe_ids from the JWT
MOCK_OWNER_CAFE_ID = 1

router = APIRouter()

@router.get("/staff", response_model=List[StaffResponse])
def read_staff(
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_owner) # V0.5
):
    """
    List all staff members for the current owner's cafe.
    """
    staff_members = db.query(Staff).filter(
        Staff.cafe_id == MOCK_OWNER_CAFE_ID,
        Staff.is_active == True
    ).all()
    return staff_members

@router.post("/staff", response_model=StaffResponse)
def create_staff(
    staff_in: StaffCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new staff member.
    """
    # Simple hash for V0 (In production use passlib/bcrypt)
    # Using a simple hash so we can implement it without heavy dependencies right now
    # Check if pin is 4-6 digits
    if not staff_in.pin.isdigit() or not (4 <= len(staff_in.pin) <= 6):
         raise HTTPException(status_code=400, detail="PIN must be 4-6 digits")

    # In V0, we enforce the cafe_id to match the owner (Prevent cross-posting)
    if staff_in.cafe_id != MOCK_OWNER_CAFE_ID:
        raise HTTPException(status_code=403, detail="Not authorized for this cafe")

    # Hasher (Placeholder) - Real impl would be: pwd_context.hash(pin)
    pin_hash = f"hashed_{staff_in.pin}" 

    new_staff = Staff(
        name=staff_in.name,
        pin_hash=pin_hash,
        role=staff_in.role,
        cafe_id=staff_in.cafe_id,
        is_active=True
    )
    db.add(new_staff)
    db.commit()
    db.refresh(new_staff)
    return new_staff

@router.delete("/staff/{staff_id}")
def delete_staff(
    staff_id: int,
    db: Session = Depends(get_db)
):
    """
    Soft delete a staff member.
    """
    staff = db.query(Staff).filter(
        Staff.id == staff_id,
        Staff.cafe_id == MOCK_OWNER_CAFE_ID
    ).first()
    
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
        
    staff.is_active = False # Soft delete
    db.commit()
    return {"ok": True}
