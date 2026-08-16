"""HTTP bridge between the static frontend and the existing AI pipeline."""

from __future__ import annotations

import shutil
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from brain_of_the_doctor import brain_of_the_doctor
from voice_of_the_doctor import convert_text_to_doctor_audio
from voice_of_the_patient import transcribe_patient_voice


BASE_DIR = Path(__file__).resolve().parent

FRONTEND_FILE = BASE_DIR / "frontend" / "code.html"

GENERATED_AUDIO_DIR = BASE_DIR / "generated_audio"
GENERATED_AUDIO_DIR.mkdir(exist_ok=True)


app = FastAPI(title="AI Skin Specialist")

app.mount(
    "/media",
    StaticFiles(directory=GENERATED_AUDIO_DIR),
    name="media"
)


def process_inputs(
    audio_file,
    image_filepath=None
):
    """
    Run the speech-to-text, AI analysis,
    and text-to-speech pipeline.
    """

    # 1. Patient voice -> text
    patient_text = transcribe_patient_voice(audio_file)

    # 2. Patient text + optional image -> doctor response
    doctor_text = brain_of_the_doctor(
        patient_text=patient_text,
        image_filepath=image_filepath,
    )

    # 3. Doctor response -> audio
    doctor_audio = convert_text_to_doctor_audio(
        doctor_text
    )

    return (
        patient_text,
        doctor_text,
        Path(doctor_audio)
    )


async def save_upload(
    upload: UploadFile | None,
    directory: Path,
    stem: str,
    allowed_extensions: set[str],
) -> Path | None:
    """
    Save an uploaded file temporarily,
    retaining only a safe extension.
    """

    if upload is None or not upload.filename:
        return None

    extension = Path(upload.filename).suffix.lower()

    if extension not in allowed_extensions:
        allowed = ", ".join(sorted(allowed_extensions))

        raise HTTPException(
            400,
            f"Unsupported {stem} format. Use: {allowed}"
        )

    destination = directory / f"{stem}{extension}"

    destination.write_bytes(
        await upload.read()
    )

    return destination


@app.get(
    "/",
    include_in_schema=False
)
async def frontend() -> FileResponse:
    return FileResponse(FRONTEND_FILE)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/analyze")
async def analyze_concern(
    audio: UploadFile = File(...),
    image: UploadFile | None = File(None),
) -> dict[str, str]:
    """
    Receive voice + optional image from the frontend
    and run the AI skin specialist pipeline.
    """

    with TemporaryDirectory(
        prefix="skin-specialist-"
    ) as temp_directory:

        temp_path = Path(temp_directory)

        # --------------------------------------------------
        # Save patient audio
        # --------------------------------------------------

        audio_path = await save_upload(
            audio,
            temp_path,
            "patient-audio",
            {
                ".mp3",
                ".wav",
                ".m4a",
                ".ogg",
                ".webm",
                ".mp4",
            },
        )

        # --------------------------------------------------
        # Save optional skin image
        # --------------------------------------------------

        image_path = await save_upload(
            image,
            temp_path,
            "skin-image",
            {
                ".jpg",
                ".jpeg",
                ".png",
                ".webp",
            },
        )

        # --------------------------------------------------
        # Validate audio
        # --------------------------------------------------

        if audio_path is None:
            raise HTTPException(
                400,
                "Please record or upload an audio message first."
            )

        try:

            patient_text, doctor_text, doctor_audio = process_inputs(
                audio_path,
                image_path,
            )

        except Exception as error:

            # Do not expose credentials or traceback
            raise HTTPException(
                502,
                f"Analysis could not be completed: {error}"
            ) from error

    # ------------------------------------------------------
    # Copy generated doctor audio to public media folder
    # ------------------------------------------------------

    audio_name = (
        f"doctor-response-{uuid4().hex}.mp3"
    )

    public_audio_path = (
        GENERATED_AUDIO_DIR / audio_name
    )

    shutil.copy2(
        doctor_audio,
        public_audio_path
    )

    # ------------------------------------------------------
    # Return frontend response
    # ------------------------------------------------------

    return {
        "transcript": patient_text,
        "response": doctor_text,
        "audio_url": f"/media/{audio_name}",
    }


if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )