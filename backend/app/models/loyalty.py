from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

class LoyaltyAccount(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True)
    points_balance: Mapped[int] = mapped_column(default=0)
    
    user: Mapped["User"] = relationship("User", backref="loyalty_account")

class Transaction(Base):
    customer_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    staff_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"), nullable=True)
    
    amount: Mapped[int] = mapped_column(comment="In smallest currency unit (e.g. cents)")
    points_earned: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships 
    # Note: Requires clear imports in user.py or string based to avoid circular dep issues.
    # For now, simplistic.