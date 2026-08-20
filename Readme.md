# ✨ AI Content & Meeting Summarizer Engine

An end-to-end, full-stack AI application that transforms raw audio and video recordings into structured summaries, key takeaways, decisions, and action items instantly. Powered by **FastAPI**, **Streamlit**, **FFmpeg**, and **Groq Cloud API** (`whisper-large-v3` + `qwen/qwen3.6-27b`).

---

## 🎬 Product Demo & Sample Media

### 🎥 Full End-to-End Walkthrough
Watch the complete end-to-end processing pipeline, dynamic UI rendering, and history logs in real time:

<video src="./assets/demo_video.mp4" controls="controls" style="max-width: 100%; width: 100%;"></video>

*(If your browser does not render the inline video player above, [download or view demo_video.mp4 directly](./assets/demo.mp4).)*

---

### 📁 Input Sample Assets

* 🔊 **Sample Audio Input:** [Download / Listen to `sample_audio.mp3`](./assets/sample_audio.mp3)
* 🎥 **Sample Video Input:** [Download / View `sample_video.mp4`](./assets/sample_video.mp4)

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
├── assets/         # Local media assets (demo_video.mp4, sample_audio.mp3, sample_video.mp4)
├── app.py          # Streamlit UI interface and dynamic card layout
├── main.py         # FastAPI backend server & Groq transcription/analysis pipeline
├── schemas.py      # Pydantic data models for structured response validation
├── styles.css      # Custom CSS styling for modern UI theme
├── history.json    # Local persistent storage for analysis logs
└── .env            # Local environment file storing API keys
