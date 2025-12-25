# Import all models here for Alembic to see
from app.db.base_class import Base  # noqa
from app.models.user import User, VerificationRequest  # noqa
from app.models.loyalty import LoyaltyAccount, Transaction  # noqa
from app.models.cafe import Cafe, Coupon  # noqa