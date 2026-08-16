import os
from pathlib import Path

from deepgram import DeepgramClient
from dotenv import load_dotenv



def convert_text_to_doctor_audio(text):
    """
    Convert doctor's text response into an MP3 audio file
    using Deepgram Text-to-Speech.
    """

    api_key = os.environ.get("Deepgram_API_KEY")

    if not api_key:
        raise ValueError("Missing Deepgram_API_KEY in .env")

    # Deepgram Aura-2 accepts max 2000 characters per TTS request.
    max_chars = 1900
    text = text.strip()

    if len(text) > max_chars:
        text = text[:max_chars]

        # Avoid cutting a word in half
        last_space = text.rfind(" ")
        if last_space > 0:
            text = text[:last_space]

        text += "."

    print(f"TTS input characters: {len(text)}")

    deepgram = DeepgramClient(api_key=api_key)

    audio = deepgram.speak.v1.audio.generate(
        text=text,
        model="aura-2-thalia-en",
        encoding="mp3",
    )

    audio_file = "doctor_response.mp3"
    audio_path = Path(__file__).with_name(audio_file)

    with audio_path.open("wb") as file:
        for chunk in audio:
            file.write(chunk)

    print(f"Doctor audio saved to: {audio_path}")

    return audio_path