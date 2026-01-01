from sqlalchemy import String, Boolean, ForeignKey, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.base_class import Base

class StaffRole(str, enum.Enum):
    MANAGER = "manager"
    WAITER = "waiter"

class Staff(Base):
    """
    Represents a staff member who can log in to the Staff PWA.
    """
    name: Mapped[str] = mapped_column(String, index=True)
    pin_hash: Mapped[str] = mapped_column(String, nullable=False) # Hashed PIN
    role: Mapped[StaffRole] = mapped_column(Enum(StaffRole), default=StaffRole.WAITER)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Validation/Permissions
    cafe_id: Mapped[int] = mapped_column(ForeignKey("cafe.id"))
    cafe: Mapped["Cafe"] = relationship("Cafe", back_populates="staff_members")
