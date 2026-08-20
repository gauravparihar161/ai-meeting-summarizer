# ✨ AI Content & Meeting Summarizer Engine

An end-to-end, full-stack AI application that transforms raw audio and video recordings into structured summaries, key takeaways, decisions, and action items instantly. Powered by **FastAPI**, **Streamlit**, **FFmpeg**, and **Groq Cloud API** (`whisper-large-v3` + `qwen/qwen3.6-27b`).

---

## 🎬 Product Demo & Sample Pipeline

### 🔊 Input Sample Audio
Listen to the input audio file tested in the demonstration:
🎵 **[Download / Play Sample MP3 Audio](https://github.com/user-attachments/files/31277708/Babies.-.Phrases.lingoneo.org.mp3)**

### 🎥Input Sample Video

https://github.com/user-attachments/assets/5c99f57a-24a1-461c-96cb-539c9530ae0b

### ⚡ Animated UI Output
Watch the complete end-to-end processing pipeline in real time,
Quick visual glance of the rendered output cards and interactive UI:

<img width="800" alt="UI Output Demo GIF" src="https://github.com/user-attachments/assets/f2ba352f-5664-4013-b118-e5fcccba314e" />

---

## ⚡ Key Features

* **Multi-Format Media Support:** Upload `.mp3`, `.wav`, `.m4a`, `.ogg`, `.mp4`, `.mkv`, `.mov`, and `.avi` files.
* **Local Audio Compression:** Uses **FFmpeg** to extract audio tracks and downsample them to 16kHz mono MP3 (`64kbps`) before network requests, minimizing upload sizes and accelerating API processing times.
* **High-Speed Transcription:** Integrates Groq's `whisper-large-v3` engine for near real-time speech-to-text conversion.
* **Smart Schema Categorization:** Automatically classifies uploads into `meeting`, `tutorial`, `news`, or `presentation` categories:
  * **Meetings:** Extracts `key_decisions` and structured `action_items` (task, assignee, priority).
  * **Tutorials / Presentations:** Extracts actionable `key_takeaways` and educational lessons.
* **Strict JSON Schema Enforcement:** Employs Pydantic v2 schemas and JSON mode output formatting to eliminate structural hallucination.
* **Persistent Session History:** Local storage (`history.json`) allowing users to review, refresh, or delete previous analysis logs.

---

## 🛠️ Tech Stack

| Component | Technology / Tool |
| :--- | :--- |
| **Frontend UI** | Streamlit, Custom HTML/CSS (`styles.css`) |
| **Backend API** | FastAPI, Uvicorn |
| **Media Processing** | FFmpeg (CLI via `subprocess`) |
| **Speech-to-Text** | Groq Whisper API (`whisper-large-v3`) |
| **LLM Inference** | Groq API (`qwen/qwen3.6-27b`) |
| **Data Validation** | Pydantic v2 |

---

## 📁 Repository Structure

```text
.
├── app.py          # Streamlit UI interface and dynamic card layout
├── main.py         # FastAPI backend server & Groq transcription/analysis pipeline
├── schemas.py      # Pydantic data models for structured response validation
├── styles.css      # Custom CSS styling for modern UI theme
├── history.json    # Local persistent storage for analysis logs
└── .env            # Local environment file storing API keys