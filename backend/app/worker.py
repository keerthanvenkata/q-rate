import random
import uuid
import uuid as uuid_lib

from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend
from sqlalchemy import select, desc

from app.services.media import download_whatsapp_media
from app.services.verifier import verify_review_screenshot
from app.services.whatsapp import whatsapp_service
from app.db.session import AsyncSessionLocal
from app.models.user import VerificationRequest, User
from app.models.cafe import Cafe, Coupon

# Configure Redis broker
broker = ListQueueBroker(
    url="redis://localhost:6379",
).with_result_backend(RedisAsyncResultBackend(redis_url="redis://localhost:6379"))


# Task to process incoming webhook (prototype)
@broker.task
async def process_webhook_message(message_body: dict):
    print(f"Processing webhook task: {message_body}")

    try:
        entry = message_body.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])

        if not messages:
            return

        message = messages[0]
        sender_phone = message.get("from")
        msg_type = message.get("type")

        if msg_type == "image":
            image_id = message["image"]["id"]
            print(f"Downloading image {image_id}...")

            # 1. Download
            image_bytes = await download_whatsapp_media(image_id)

            # 2. Dynamic Context & Verification
            async with AsyncSessionLocal() as session:
                async with session.begin():
                    # A. Lookup Pending Visit
                    stmt_vr = (
                        select(VerificationRequest)
                        .where(VerificationRequest.phone_number == sender_phone)
                        .order_by(desc(VerificationRequest.created_at))
                        .limit(1)
                    )
                    result_vr = await session.execute(stmt_vr)
                    latest_visit = result_vr.scalars().first()

                    if not latest_visit:
                        # Fallback for prototype testing if no visit exists
                        print("No visit found. Using default Q-Rate Cafe for testing.")
                        stmt_cafe = select(Cafe).where(Cafe.name == "Q-Rate Cafe")
                        res_cafe = await session.execute(stmt_cafe)
                        cafe = res_cafe.scalars().first()
                        if not cafe:
                            cafe = Cafe(name="Q-Rate Cafe", reward_policy="Free Cookie")
                            session.add(cafe)
                            await session.flush()
                        cafe_id = cafe.id
                        cafe_name = cafe.name
                    else:
                        cafe_id = latest_visit.cafe_id
                        # Resolve Cafe Name
                        stmt_cafe_name = select(Cafe).where(Cafe.id == cafe_id)
                        res_cafe = await session.execute(stmt_cafe_name)
                        cafe_obj = res_cafe.scalars().first()
                        cafe_name = cafe_obj.name if cafe_obj else "Cafe"

                    # B. Verify with dynamic name
                    print(f"Verifying screenshot for {cafe_name}...")
                    verification = await verify_review_screenshot(
                        image_bytes, cafe_name=cafe_name
                    )

                    if verification.get("is_valid_review"):
                        # Update Visit (if exists)
                        if latest_visit:
                            latest_visit.is_verified = True
                            latest_visit.code = "VERIFIED_AI"

                        # C. Generate Coupon
                        unique_suffix = str(uuid.uuid4())[:4].upper()
                        phone_suffix = (
                            sender_phone[-4:] if len(sender_phone) >= 4 else "0000"
                        )
                        coupon_code = f"FREE-{phone_suffix}-{unique_suffix}"

                        # Find/Create User
                        stmt_user = select(User).where(
                            User.phone_number == sender_phone
                        )
                        res_user = await session.execute(stmt_user)
                        user = res_user.scalars().first()
                        if not user:
                            user = User(phone_number=sender_phone)
                            session.add(user)
                            await session.flush()

                        coupon = Coupon(
                            code=coupon_code,
                            cafe_id=cafe_id,
                            user_id=user.id,
                            type="review_reward",
                            points_cost=0,
                        )
                        session.add(coupon)

                        rating = verification.get("star_rating")
                        reply = f"✅ Verified for {cafe_name}! ({rating} stars). Your Coupon Code: *{coupon_code}*."
                    else:
                        reason = verification.get("reason", "Unknown")
                        reply = f"❌ Verification failed. Reason: {reason}. Please try again."

            # 4. Reply (Outside session scope)
            await whatsapp_service.send_text_message(sender_phone, reply)

        elif msg_type == "text":
            # Echo or help
            await whatsapp_service.send_text_message(
                sender_phone,
                "Send me a screenshot of your Google Review to get a reward!",
            )

    except Exception as e:
        print(f"Error in worker: {e}")
