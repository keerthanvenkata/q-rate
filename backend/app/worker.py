import random

from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend

from app.services.media import download_whatsapp_media
from app.services.verifier import verify_review_screenshot
from app.services.whatsapp import whatsapp_service

# Configure Redis broker
broker = ListQueueBroker(
    url="redis://localhost:6379",
).with_result_backend(
    RedisAsyncResultBackend(
        redis_url="redis://localhost:6379"
    )
)

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
            
                        stmt_vr = (
                            select(VerificationRequest)
                            .where(VerificationRequest.phone_number == sender_phone)
                            .order_by(desc(VerificationRequest.created_at))
                            .limit(1)
                        )
                        result_vr = await session.execute(stmt_vr)
                        latest_visit = result_vr.scalars().first()

                        if not latest_visit:
                            # Edge Case: User sent photo but Staff never initiated "Visit"
                            # For V0, we might auto-assign to a default cafe or reject
                            await whatsapp_service.send_text_message(sender_phone, "⚠️ We couldn't find your visit record. Please ask staff to check you in first!")
                            return

                        # B. Get Cafe Context from the Visit
                        cafe_id = latest_visit.cafe_id
                        if not cafe_id:
                             # Fallback or Error
                             print(f"Error: Visit {latest_visit.id} has no Cafe ID")
                             return

                        # C. Update the Visit Record
                        latest_visit.is_verified = True
                        latest_visit.code = "VERIFIED_BY_AI" # or similar status flag

                        # D. Generate Coupon linked to this Cafe and User
                        unique_suffix = str(uuid.uuid4())[:4].upper()
                        phone_suffix = sender_phone[-4:] if len(sender_phone) >= 4 else "0000"
                        coupon_code = f"FREE-{phone_suffix}-{unique_suffix}"
                        
                        # Find/Create User (Loyalty Account holder)
                        stmt_user = select(User).where(User.phone_number == sender_phone)
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
                            type="review_reward", # Explicitly set type
                            points_cost=0
                        )
                        session.add(coupon)
                
                # Committed via context manager
                rating = verification.get("star_rating")
                reply = f"✅ Verified! ({rating} stars). Your Coupon Code: *{coupon_code}*. Show this to staff!"
                
                # Committed via context manager
                rating = verification.get("star_rating")
                reply = f"✅ Verified! ({rating} stars). Your Coupon Code: *{coupon_code}*. Show this to staff!"
                
            else:
                reason = verification.get("reason", "Unknown")
                reply = f"❌ Verification failed. Reason: {reason}. Please try again."
            
            # 4. Reply
            await whatsapp_service.send_text_message(sender_phone, reply)
            
        elif msg_type == "text":
            # Echo or help
            await whatsapp_service.send_text_message(sender_phone, "Send me a screenshot of your Google Review to get a reward!")

    except Exception as e:
        print(f"Error in worker: {e}")

