import os
from google import genai
from google.genai import types
from .config import GEMINI_API_KEY, MODEL_NAME
from .models import WaybillData

def extract_waybill_data(file_path: str) -> WaybillData:
    """
    Extracts structured waybill data from an image or PDF using Gemini.
    """
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set. Please check your .env file.")

    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = (
        "Extract the following information from this waybill (İrsaliye) or invoice: "
        "document date, document number, supplier name, and a list of items. "
        "For each item, extract the product name, quantity, unit, and unit price. "
        "Return the output strictly matching the provided JSON schema."
    )

    # Upload the file first using the Files API
    uploaded_file = client.files.upload(file=file_path)

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                uploaded_file,
                prompt
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=WaybillData,
                temperature=0.0, # Use low temperature for extraction
            )
        )
    finally:
        # Clean up the uploaded file
        client.files.delete(name=uploaded_file.name)

    if not response.text:
        raise ValueError("Failed to extract data: Empty response from Gemini.")

    # Parse the response JSON into the Pydantic model
    return WaybillData.model_validate_json(response.text)
