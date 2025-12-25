import json
import os

from google import genai
from google.genai import types
from pydantic import BaseModel

from app.core.config import settings

# Initialize Gemini Client
# We will use the 'gemini-3.0-flash' model or its successor 'gemini-2.0-flash'
# Assuming API key is set in environment or config
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


async def verify_review_screenshot(image_bytes: bytes, cafe_name: str) -> dict:
    """
    Verifies if the uploaded screenshot is a valid Google Review for the specific cafe.
    Returns structured data: {is_valid, star_rating, reviewer_name, confidence, reason}
    """

    class ReviewVerification(BaseModel):
        is_valid_review: bool
        star_rating: int | None
        reviewer_name: str | None
        reason: str

    prompt = f"""
    Analyze this screenshot. It should be a Google Maps review for the cafe "{cafe_name}".
    
    1. Check if the review is for "{cafe_name}".
    2. Extract the star rating (1-5).
    3. Extract the reviewer's name.
    4. Determine if the review is "posted" (not just in draft mode).
    
    Return JSON with keys:
    - is_valid_review: boolean
    - star_rating: integer or null
    - reviewer_name: string or null
    - reason: short explanation
    """

    try:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL_NAME,
            contents=[
                types.Part.from_text(prompt),
                types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ReviewVerification,
            ),
        )

        # Parse JSON response
        result = json.loads(response.text)
        return result

    except Exception as e:
        print(f"Gemini Verification Error: {e}")
        return {"is_valid_review": False, "reason": f"Verification failed: {str(e)}"}
