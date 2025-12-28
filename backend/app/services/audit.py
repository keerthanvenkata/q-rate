from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit import AuditLog, ActorType
from app.core.logging import app_logger

class AuditService:
    async def log(
        self,
        session: AsyncSession,
        actor_type: ActorType,
        event_name: str,
        target_resource: str,
        actor_id: int | None = None,
        payload: dict | None = None
    ) -> AuditLog:
        """
        Creates an immutable audit log entry.
        """
        try:
            log_entry = AuditLog(
                actor_type=actor_type,
                actor_id=actor_id,
                event_name=event_name,
                target_resource=target_resource,
                payload=payload
            )
            session.add(log_entry)
            # We assume the caller handles commit/flush to ensure atomicity with the main transaction
            # But if this is a fire-and-forget logging (e.g. error logging), we might want separate session.
            # For strict audit trails (e.g. "Visit Created"), it MUST belong to the same transaction.
            
            app_logger.info(f"AUDIT: [{actor_type}] {event_name} -> {target_resource}")
            return log_entry
            
        except Exception as e:
            app_logger.error(f"Failed to create audit log: {e}")
            raise e

audit_service = AuditService()
