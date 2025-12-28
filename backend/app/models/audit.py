import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, String, Integer, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.base_class import Base
import enum

class ActorType(str, enum.Enum):
    STAFF = "STAFF"
    CUSTOMER = "CUSTOMER"
    OWNER = "OWNER"
    PLATFORM_ADMIN = "PLATFORM_ADMIN"
    SYSTEM = "SYSTEM"

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    actor_type = Column(Enum(ActorType), nullable=False)
    actor_id = Column(Integer, nullable=True) # ID of Staff, User, or Owner. Null if System.
    
    event_name = Column(String, nullable=False) # e.g. VISIT_INITIATED
    target_resource = Column(String, nullable=True) # e.g. verification_request:101
    
    # We use JSONB for Postgres, but generic JSON for compatibility if needed.
    # In V0 prototype we are using standard JSON type in SQAlchemy which maps to JSONB in PG.
    payload = Column(JSON, nullable=True)
