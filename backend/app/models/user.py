from datetime import datetime
from typing import Optional
import enum

from sqlalchemy import String, Boolean, DateTime, Enum, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

class UserRole(str, enum.Enum):
    CUSTOMER = "customer"
    STAFF = "staff"
    ADMIN = "admin"

class User(Base):
    phone_number: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.CUSTOMER)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

class VerificationRequest(Base):
    """
    Stores OTP or other verification requests.
    V0+: Also acts as the 'Visit' record initiated by staff.
    """
    phone_number: Mapped[str] = mapped_column(String, index=True)
    code: Mapped[str] = mapped_column(String, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Context
    cafe_id: Mapped[Optional[int]] = mapped_column(ForeignKey("cafe.id"), nullable=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"), nullable=True)

    # Visit/Bill Info (Staff Input)
    bill_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    bill_amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    staff_id: Mapped[Optional[str]] = mapped_column(String, nullable=True, comment="ID/Name of staff member")
    verbal_consent: Mapped[bool] = mapped_column(Boolean, default=False)
    customer_name_input: Mapped[Optional[str]] = mapped_column(String, nullable=True)