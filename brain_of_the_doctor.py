import base64
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


# Load environment variables
load_dotenv()


def clean_doctor_response(text, max_chars=1500):
    """
    Clean the model's response before sending it to the UI and TTS.

    - Removes <think>...</think> sections
    - Removes common reasoning text
    - Limits the response length for Deepgram TTS
    """

    if not text:
        return "I could not generate a response."

    # Remove <think>...</think> blocks
    text = re.sub(
        r"<think>.*?</think>",
        "",
        text,
        flags=re.DOTALL | re.IGNORECASE
    )

    # Remove remaining think tags
    text = re.sub(
        r"</?think>",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Remove common visible reasoning prefixes
    text = re.sub(
        r"(?is)^(?:here'?s\s+a\s+thinking\s+process:|thinking\s+process:).*?\n",
        "",
        text
    )

    text = text.strip()

    # Keep response safely below Deepgram's 2000-character limit
    if len(text) > max_chars:
        text = text[:max_chars]

        # Avoid cutting a word in half
        last_space = text.rfind(" ")

        if last_space > 0:
            text = text[:last_space]

        text += "."

    return text


def brain_of_the_doctor(
    patient_text,
    image_filepath=None
):
    """
    Send patient's text and optional image to Groq
    and return a concise final medical-information response.
    """

    # Get API key
    api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "Missing GROQ_API_KEY in .env or environment"
        )

    # Create Groq client
    client = Groq(api_key=api_key)

    # ---------------------------------------------------------
    # Build prompt depending on whether an image was provided
    # ---------------------------------------------------------

    if image_filepath:
        user_prompt = f"""
Patient's question:
{patient_text}

An image has been provided with this request.

Analyze the patient's question and the actual provided image.

Rules:
- Describe only what is visibly present in the image.
- Do not invent or assume visual findings.
- Provide general medical information only.
- Do not provide a specific diagnosis.
- Do not claim certainty about a medical condition.
- If professional evaluation may be needed, recommend consulting a qualified doctor.
- Keep the response concise and suitable for voice output.
- Do not include internal reasoning.
- Do not include <think> tags.
- Return only the final answer.
"""

    else:
        user_prompt = f"""
Patient's question:
{patient_text}

NO IMAGE WAS PROVIDED.

Answer using only the patient's text.

Rules:
- Do not describe or invent any image findings.
- Do not say "based on the image".
- Do not assume redness, rash, swelling, lesions, or any other visual finding.
- Provide general medical information only.
- Do not provide a specific diagnosis.
- Do not claim certainty about a medical condition.
- If professional evaluation may be needed, recommend consulting a qualified doctor.
- Keep the response concise and suitable for voice output.
- Do not include internal reasoning.
- Do not include <think> tags.
- Return only the final answer.
"""

    # User content
    user_content = [
        {
            "type": "text",
            "text": user_prompt,
        }
    ]

    # ---------------------------------------------------------
    # Add image ONLY if one was provided
    # ---------------------------------------------------------

    if image_filepath:
        image_path = Path(image_filepath)

        if not image_path.exists():
            raise FileNotFoundError(
                f"Image file not found: {image_path}"
            )

        with image_path.open("rb") as file:
            image_data = base64.b64encode(
                file.read()
            ).decode("utf-8")

        mime_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
        }

        mime_type = mime_types.get(
            image_path.suffix.lower(),
            "image/png"
        )

        user_content.append(
            {
                "type": "image_url",
                "image_url": {
                    "url": (
                        f"data:{mime_type};base64,"
                        f"{image_data}"
                    )
                },
            }
        )

    # ---------------------------------------------------------
    # Send request to Groq
    # ---------------------------------------------------------

    response = client.chat.completions.create(
        model=os.environ.get(
            "GROQ_MODEL",
            "qwen/qwen3.6-27b"
        ),

        reasoning_format="hidden",
        reasoning_effort="none",

        max_completion_tokens=700,

        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful medical assistant. "
                    "Provide general medical information only. "
                    "Never invent facts, visual findings, or "
                    "patient information. "
                    "If no image is provided, never describe an image. "
                    "Do not provide a specific diagnosis. "
                    "Do not claim certainty about a medical condition. "
                    "Recommend professional medical evaluation when "
                    "appropriate. "
                    "Return only the final answer without reasoning."
                ),
            },
            {
                "role": "user",
                "content": user_content,
            },
        ],
    )

    # ---------------------------------------------------------
    # Get final response
    # ---------------------------------------------------------

    doctor_response = response.choices[0].message.content

    # Clean response before UI / TTS
    doctor_response = clean_doctor_response(
        doctor_response,
        max_chars=1500
    )

    print(
        f"Doctor response length: "
        f"{len(doctor_response)} characters"
    )

    return doctor_response


# -------------------------------------------------------------
# Standalone test
# -------------------------------------------------------------

if __name__ == "__main__":

    folder = os.path.dirname(__file__)

    test_image = os.path.join(
        folder,
        "t_image.png"
    )

    result = brain_of_the_doctor(
        patient_text="What do you see in this image?",
        image_filepath=test_image
    )

    print("\nDoctor response:")
    print(result)