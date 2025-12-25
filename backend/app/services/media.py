import httpx
from app.core.config import settings

async def download_whatsapp_media(media_id: str) -> bytes:
    """
    Downloads media from WhatsApp Cloud API.
    Two-step process:
    1. Retrieve URL from media_id.
    2. Download content from URL.
    """
    async with httpx.AsyncClient() as client:
        # Step 1: Get Media URL
        url = f"https://graph.facebook.com/v21.0/{media_id}"
        headers = {
            "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}"
        }
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        media_info = response.json()
        download_url = media_info.get("url")
        
        if not download_url:
            raise ValueError(f"No URL found for media ID: {media_id}")
            
        # Step 2: Download Media
        # Note: We reuse the same Authorization token
        media_response = await client.get(download_url, headers=headers)
        media_response.raise_for_status()
        return media_response.content
