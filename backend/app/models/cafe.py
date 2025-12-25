from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, Boolean, DateTime, JSON, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class Chain(Base):
    """
    Represents a brand/franchise that owns multiple Cafe locations.
    Loyalty points are aggregated at this level if a cafe belongs to a chain.
    """
    name: Mapped[str] = mapped_column(String, index=True)
    
    cafes: Mapped[list["Cafe"]] = relationship("Cafe", back_populates="chain")

class Cafe(Base):
    """
    Represents a specific cafe location. 
    """
    name: Mapped[str] = mapped_column(String, index=True)
    location: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    # If set, this cafe is part of a chain (shared loyalty)
    chain_id: Mapped[Optional[int]] = mapped_column(ForeignKey("chain.id"), nullable=True)
    chain: Mapped[Optional["Chain"]] = relationship("Chain", back_populates="cafes")
    
    # Simple V0 Reward Policy: Text description of the "Freebie" (e.g., "Free Cookie")
    reward_policy: Mapped[str] = mapped_column(String, default="Free Coffee")
    
    # Configurable Loyalty Rules (JSON)
    # e.g., {"points_ratio": 0.1, "redeemables": [...], "freebies": [...]}
    loyalty_config: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    coupons: Mapped[list["Coupon"]] = relationship("Coupon", back_populates="cafe")

import enum
class CouponType(str, enum.Enum):
    REVIEW_REWARD = "review_reward"
    LOYALTY_REDEMPTION = "loyalty_redemption"

class Coupon(Base):
    """
    A generated reward for a user at a specific cafe.
    """
    code: Mapped[str] = mapped_column(String, unique=True, index=True)
    type: Mapped[CouponType] = mapped_column(Enum(CouponType), default=CouponType.REVIEW_REWARD)
    points_cost: Mapped[Optional[int]] = mapped_column(default=0) # If redeemed with points
    
    is_redeemed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    cafe_id: Mapped[int] = mapped_column(ForeignKey("cafe.id"))
    cafe: Mapped["Cafe"] = relationship("Cafe", back_populates="coupons")
    
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    # Relationship to User needed, assuming user.py handles the back_populates or we add it there.
    # For now, just FK is enough for the coupon side.
    
    # Link to the verification request that earned this coupon (for audit)
    # verification_request_id: ... (Optional optimization)
