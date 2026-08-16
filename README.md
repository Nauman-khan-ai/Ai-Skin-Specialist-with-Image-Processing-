# AI Skin Specialist

AI Skin Specialist is a multimodal AI medical-information assistant that combines **voice input, skin-image analysis, AI-generated general medical information, and text-to-speech** into a single workflow.

> ⚠️ **Medical Disclaimer:** This project is for educational, demonstration, and general health-information purposes only. It is not a diagnostic system and should not replace evaluation, diagnosis, or treatment by a qualified healthcare professional.

---

## ✨ Features

### 🎙️ Voice Input

- Record patient voice directly from the browser.
- Upload an existing audio file.
- Convert speech to text using **Groq Whisper**.

### 🖼️ Skin Image Analysis

- Upload JPG, JPEG, PNG, or WEBP images.
- Analyze the patient's question together with the uploaded skin image.
- If no image is provided, the AI is instructed not to invent visual findings.

### 🤖 AI Medical Assistant

- Uses **Qwen 3.6 27B** through Groq.
- Provides general medical information.
- Avoids presenting a definitive diagnosis.
- Removes reasoning-style output before displaying or speaking the answer.
- Keeps responses concise for voice generation.

### 🔊 AI Voice Response

- Uses **Deepgram Text-to-Speech**.
- Converts the AI response into an MP3 file.
- Plays the generated response in the browser when autoplay is permitted.
- Allows the user to replay the response manually.

### 🌐 Custom Web Interface

- Modern light medical UI.
- Responsive desktop and mobile layout.
- Voice recording interface.
- Image upload and preview.
- AI response panel.
- Doctor voice playback.

---

# 🏗️ Architecture

```text
Patient Voice
      │
      ▼
Groq Whisper
      │
      ▼
Patient Text
      │
      ├───────────────┐
      │               │
      │          Skin Image
      │               │
      └───────┬───────┘
              ▼
       Groq Multimodal AI
        (Qwen 3.6 27B)
              │
              ▼
   General Medical Information
              │
              ▼
         Deepgram TTS
              │
              ▼
        Doctor's Voice
              │
              ▼
        Browser Player
```

---

# 📁 Project Structure

```text
AI Skin Specialist/
│
├── main.py
├── brain_of_the_doctor.py
├── voice_of_the_patient.py
├── voice_of_the_doctor.py
├── .env
│
├── generated_audio/
│
├── frontend/
│   └── code.html
│
├── design.md
└── README.md
```

### File Responsibilities

| File | Description |
|---|---|
| `main.py` | FastAPI server and API endpoints |
| `brain_of_the_doctor.py` | AI text + image analysis |
| `voice_of_the_patient.py` | Speech-to-text using Groq Whisper |
| `voice_of_the_doctor.py` | Text-to-speech using Deepgram |
| `frontend/code.html` | Frontend UI and API communication |
| `design.md` | UI design system |
| `generated_audio/` | Generated doctor-response audio |

---

# ⚙️ Requirements

Before running the project, make sure you have:

- Python 3.10+
- `uv`
- FFmpeg
- A working microphone
- Groq API key
- Deepgram API key

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-skin-specialist.git
cd ai-skin-specialist
```

Replace the GitHub URL with your actual repository URL.

---

## 2. Install Dependencies

If the project already contains its dependency configuration:

```bash
uv sync
```

Otherwise:

```bash
uv add fastapi uvicorn python-dotenv groq deepgram-sdk SpeechRecognition pydub
```

For microphone support:

```bash
uv add "SpeechRecognition[audio]"
```

---

# 🔧 Install FFmpeg

## Windows

```powershell
winget install --id Gyan.FFmpeg -e
```

Verify:

```powershell
ffmpeg -version
```

## macOS

```bash
brew install ffmpeg
```

## Ubuntu / Debian

```bash
sudo apt update
sudo apt install ffmpeg
```

---

# 🔐 Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=qwen/qwen3.6-27b
WHISPER_MODEL=whisper-large-v3
Deepgram_API_KEY=your_deepgram_api_key
```

> **Never commit your `.env` file to GitHub.**

Recommended `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
generated_audio/*
*.pyc
```

---

# ▶️ Run the Application

Start the FastAPI server:

```bash
uv run main.py
```

Then open:

```text
http://127.0.0.1:8000
```

---

# ❤️ Health Check

You can check whether the backend is running:

```text
http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok"
}
```

---

# 🔌 API

## GET `/`

Serves the frontend application.

## GET `/health`

Returns backend health status.

## POST `/api/analyze`

Accepts:

- `audio` — required patient audio
- `image` — optional skin image

Example:

```bash
curl -X POST http://127.0.0.1:8000/api/analyze \
  -F "audio=@patient-voice.webm" \
  -F "image=@skin-image.jpg"
```

Example response:

```json
{
  "transcript": "Patient's transcribed question",
  "response": "AI-generated general medical information",
  "audio_url": "/media/doctor-response-example.mp3"
}
```

---

# 🔄 Application Workflow

1. Patient records or uploads a voice message.
2. Groq Whisper converts the voice into text.
3. The patient text and optional skin image are sent to the AI model.
4. Qwen generates general medical information.
5. The response is cleaned before being shown or spoken.
6. Deepgram converts the response into speech.
7. The generated audio is returned to the frontend.
8. The browser attempts to automatically play the response.
9. The user can replay the response manually.

---

# 🛡️ Medical Safety

This project is intentionally designed as an **AI medical-information assistant**, not a diagnostic authority.

The AI instructions are designed to:

- Provide general medical information.
- Avoid definitive diagnoses.
- Avoid inventing visual findings.
- Avoid claims of certainty.
- Recommend professional medical evaluation when appropriate.
- Keep responses suitable for text-to-speech.

AI-generated information can still be incorrect. Clinical decisions should **not** be based solely on this application.

---

# ⚠️ Current Limitations

- No medically validated diagnosis system.
- AI responses may contain errors.
- Browser autoplay can be blocked by browser policies.
- No built-in user authentication.
- No production-grade patient data management.
- Generated audio files require cleanup/retention policies in production.

---

# 🔮 Future Improvements

- User authentication
- Patient analysis history
- Secure database integration
- Better image-observation UI
- Streaming speech recognition
- Rate limiting
- Structured logging and monitoring
- Production deployment with HTTPS
- Secure secret management
- Improved accessibility
- Privacy and compliance review for healthcare deployment

---

# 🔒 Security

Never expose API keys in:

- Frontend JavaScript
- HTML
- GitHub
- Screenshots
- Public configuration files

Store secrets in environment variables or a secure secret-management system.

Before deploying a healthcare-related application publicly, review:

- User consent
- Privacy
- Data retention
- Access control
- Security
- Applicable healthcare laws and regulations

---

# 🧰 Technology Stack

- **Python**
- **FastAPI**
- **Groq API**
- **Qwen 3.6 27B**
- **Groq Whisper**
- **Deepgram TTS**
- **SpeechRecognition**
- **PyAudio**
- **PyDub**
- **FFmpeg**
- **HTML**
- **Tailwind CSS**
- **JavaScript**

---

# 📄 License

Choose a license before publishing the project.

For example:

```text
MIT License
```

---

# 👨‍💻 Author

**AI Skin Specialist**

An AI/ML project combining:

**Speech Recognition + Multimodal AI + Medical Image Analysis + Text-to-Speech**
