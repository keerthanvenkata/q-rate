from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend
from app.core.config import settings

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
    # Logic will go here:
    # 1. Parse message type (image/text)
    # 2. If image -> call Gemini Verifier
    # 3. Send response via WhatsAppService
