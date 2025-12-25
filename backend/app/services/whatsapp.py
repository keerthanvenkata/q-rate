import httpx
from app.core.config import settings

class WhatsAppService:
    def __init__(self):
        self.api_url = "https://graph.facebook.com/v21.0"
        self.token = settings.WHATSAPP_ACCESS_TOKEN
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
    
    async def send_text_message(self, to_phone: str, message: str):
        url = f"{self.api_url}/{self.phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        data = {
            "messaging_product": "whatsapp",
            "to": to_phone,
            "type": "text",
            "text": {"body": message}
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=headers, json=data)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                print(f"WhatsApp API Error: {e.response.text}")
                raise

whatsapp_service = WhatsAppService()
