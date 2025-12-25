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
            
            # 2. Verify (Hardcoded Cafe Name for V0 Prototype)
            # In production, cafe context comes from the 'to' number or session history
            print("Verifying screenshot...")
            verification = await verify_review_screenshot(image_bytes, cafe_name="Q-Rate Cafe")
            
            if verification.get("is_valid_review"):
                # 3. Valid: Generate Coupon (Mock logic / DB insert later)
                # For V0 Prototype: Just mock the code
                code = f"FREE{random.randint(100,999)}"
                
                rating = verification.get("star_rating")
                reply = f"✅ Verified! ({rating} stars). Your Coupon Code: *{code}*. Show this to staff!"
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

