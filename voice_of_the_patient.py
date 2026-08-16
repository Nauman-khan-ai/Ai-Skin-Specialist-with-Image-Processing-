# Step 1: Record audio from microphone

# Dependencies:
# ffmpeg, portaudio, pyaudio

import logging
import os
from io import BytesIO

import speech_recognition as sr
from pydub import AudioSegment
from groq import Groq
from dotenv import load_dotenv


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

load_dotenv()


def record_audio(file_path, timeout=20, phrase_time_limit=30):
    """
    Record audio from the microphone and save it as an MP3 file.

    Args:
        file_path (str): Path to save the recorded audio.
        timeout (int): Maximum time to wait for speech to start.
        phrase_time_limit (int): Maximum duration of speech.
    """

    recognizer = sr.Recognizer()

    # Wait 3 seconds after speech stops before ending recording
    recognizer.pause_threshold = 3
    recognizer.non_speaking_duration = 1

    # Bluetooth microphone that worked on your system
    with sr.Microphone(device_index=3) as source:

        logging.info("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        logging.info("Start speaking now...")

        audio_data = recognizer.listen(
            source,
            timeout=timeout,
            phrase_time_limit=phrase_time_limit
        )

        logging.info("Recording completed.")

    # Convert WAV data to MP3
    wav_data = audio_data.get_wav_data()

    audio_segment = AudioSegment.from_wav(
        BytesIO(wav_data)
    )

    audio_segment.export(
        file_path,
        format="mp3",
        bitrate="128k"
    )

    logging.info(f"Audio saved to {file_path}")

    return file_path


def transcribe_patient_voice(audio_file):
    """
    Convert patient's audio file into text using Groq Whisper.
    """

    groq_api_key = os.environ.get("GROQ_API_KEY")

    if not groq_api_key:
        raise ValueError("Missing GROQ_API_KEY in .env")

    client = Groq(api_key=groq_api_key)

    with open(audio_file, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=file,
            model=os.environ.get(
                "WHISPER_MODEL",
                "whisper-large-v3"
            ),
        )

    return transcription.text


# Standalone test
# This block runs only when you directly run this file.
# It will NOT run when main.py imports this module.

if __name__ == "__main__":

    audio_file = "patient_voice_test.mp3"

    record_audio(
        audio_file,
        timeout=20,
        phrase_time_limit=30
    )

    patient_text = transcribe_patient_voice(audio_file)

    print("\nPatient said:")
    print(patient_text)