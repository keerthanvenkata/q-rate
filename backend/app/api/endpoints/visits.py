from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.schemas.visit import VisitCreate, VisitResponse
from app.models.user import VerificationRequest, User
from app.models.cafe import Cafe
from app.services.whatsapp import whatsapp_service

router = APIRouter()

@router.post("/visits", response_model=VisitResponse)
async def create_visit(visit: VisitCreate, session: AsyncSession = Depends(get_db)):
    # 1. Resolve Cafe (Mock for V0 - Default to 'Q-Rate Cafe')
    stmt = select(Cafe).where(Cafe.name == "Q-Rate Cafe")
    result = await session.execute(stmt)
    cafe = result.scalars().first()
    
    if not cafe:
        # Create default if missing
        cafe = Cafe(name="Q-Rate Cafe", reward_policy="Free Cookie", chain_id=None)
        session.add(cafe)
        await session.flush()
        
    # 2. Resolve/Create User (Loyalty Account)
    # We track them by phone number
    stmt_user = select(User).where(User.phone_number == visit.phone_number)
    res_user = await session.execute(stmt_user)
    user = res_user.scalars().first()
    
    if not user:
        user = User(phone_number=visit.phone_number)
        session.add(user)
        # No flush needed yet, will commit together
    
    # [Check Rate Limits]
    from app.core.config import settings
    from sqlalchemy import func
    from datetime import datetime
    
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Global Count
    q_global = select(func.count()).where(
        VerificationRequest.phone_number == visit.phone_number,
        VerificationRequest.created_at >= today_start
    )
    res_global = await session.execute(q_global)
    count_global = res_global.scalar() or 0
    
    # Cafe Count
    q_cafe = select(func.count()).where(
        VerificationRequest.phone_number == visit.phone_number,
        VerificationRequest.cafe_id == cafe.id,
        VerificationRequest.created_at >= today_start
    )
    res_cafe = await session.execute(q_cafe)
    count_cafe = res_cafe.scalar() or 0
    
    # Determine Check-in Eligibility (Soft Limit)
    # Logic: If count < limit, they get a Check-in.
    # This means if we raise the limit to 2/day, a Bill Entry (2nd visit) WILL trigger a Check-in.
    is_checkin_eligible = True
    limit_reason = None
    
    if count_global >= settings.MAX_DAILY_CHECKINS_GLOBAL:
        is_checkin_eligible = False
        limit_reason = "Global Limit Exceeded"
    elif count_cafe >= settings.MAX_DAILY_CHECKINS_PER_CAFE:
        is_checkin_eligible = False
        limit_reason = "Cafe Limit Exceeded"
    

        
    # 3. Create VerificationRequest (The Visit)
    # This is the "Hook" record the Worker will look for later
    vr = VerificationRequest(
        phone_number=visit.phone_number,
        bill_id=visit.bill_id,
        bill_amount=visit.bill_amount,
        verbal_consent=visit.verbal_consent,
        customer_name_input=visit.customer_name,
        guest_count=visit.guest_count,
        cafe_id=cafe.id,
        is_verified=False,
        code="PENDING" if is_checkin_eligible else "SKIPPED_CHECKIN" # Just a flag for now
    )
    session.add(vr)
    # 5. Audit Logging (Compliance)
    from app.services.audit import audit_service
    from app.models.audit import ActorType
    
    await audit_service.log(
        session=session,
        actor_type=ActorType.STAFF,
        actor_id=None, # In V0 we don't have logged-in staff ID yet
        event_name="VISIT_INITIATED",
        target_resource=f"verification_request:{vr.id}",
        payload={
             "phone": visit.phone_number, # Mask in future
             "consent": visit.verbal_consent,
             "guest_count": visit.guest_count,
             "amount": visit.bill_amount
        }
    )
    
    # Commit Everything (Visit + Audit Log)
    await session.commit()
    await session.refresh(vr)

    # 4. Trigger WhatsApp Message (The Nudge)
    # For V0, we send a text with a link. In V1/Prod, this is a Template Message.
    # The link should ideally be a "Magic Link" to our Customer PWA or directly to Google Maps if we are bold.
    # Let's send a generic "Rate us" message.
    
    message_text = (
        f"Hi there! Thanks for visiting {cafe.name}. "
        f"Rate us on Google to get a free {cafe.reward_policy or 'Reward'}: "
        f"https://goo.gl/maps/example" 
        # In real scenario, this link points to our Landing Page (Customer PWA)
    )
    
    try:
        await whatsapp_service.send_text_message(visit.phone_number, message_text)
    except Exception as e:
        print(f"Failed to send WhatsApp message: {e}")
        # We don't fail the request, just log it. 
        
    return VisitResponse(id=vr.id, status=vr.code)
