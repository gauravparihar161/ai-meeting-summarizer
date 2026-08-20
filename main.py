import os
import json
import tempfile
import subprocess
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, HTTPException
from groq import Groq
from dotenv import load_dotenv
from schemas import MeetingAnalysis

load_dotenv()

app = FastAPI(
    title="AI Meeting & Content Analyzer Engine",
    description="Production-grade API for audio/video transcription and structured analysis extraction.",
    version="1.0.0"
)

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
HISTORY_FILE = "history.json"


def save_to_history(record: dict):
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
        except Exception:
            history = []
    history.insert(0, record)  # Newest records first
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


@app.get("/")
def health_check():
    return {"status": "online", "system": "AI Meeting Summarizer API"}


@app.get("/api/v1/history")
def get_history():
    if not os.path.exists(HISTORY_FILE):
        return {"history": []}
    with open(HISTORY_FILE, "r") as f:
        try:
            return {"history": json.load(f)}
        except Exception:
            return {"history": []}


@app.delete("/api/v1/history")
def clear_all_history():
    """Clear all saved history records."""
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    return {"status": "success", "message": "All history records cleared."}


@app.delete("/api/v1/history/{index}")
def delete_history_item(index: int):
    """Delete a specific history entry by index."""
    if not os.path.exists(HISTORY_FILE):
        raise HTTPException(status_code=404, detail="History log is empty.")
    try:
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
        if index < 0 or index >= len(history):
            raise HTTPException(status_code=400, detail="Invalid record index.")

        deleted_item = history.pop(index)
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)

        return {"status": "success", "deleted": deleted_item.get("filename", "Record")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/process-audio")
async def process_audio(file: UploadFile = File(...)):
    allowed_extensions = [".mp3", ".wav", ".m4a", ".ogg", ".mp4", ".mkv", ".mov", ".avi"]
    file_ext = os.path.splitext(file.filename)[1].lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Unsupported file format. Use: {allowed_extensions}")

    temp_input_path = None
    compressed_audio_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_input_path = temp_file.name

        compressed_audio_path = f"{temp_input_path}_compressed.mp3"

        # Extract audio stream and downsample to 16kHz mono MP3
        ffmpeg_cmd = [
            "ffmpeg", "-y", "-i", temp_input_path,
            "-vn", "-ar", "16000", "-ac", "1", "-b:a", "64k",
            compressed_audio_path
        ]
        subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        # 1. High-speed Transcription via Groq Whisper-large-v3
        with open(compressed_audio_path, "rb") as audio:
            transcription = groq_client.audio.transcriptions.create(
                file=(os.path.basename(compressed_audio_path), audio.read()),
                model="whisper-large-v3",
                response_format="text"
            )

        # 2. Schema-guaranteed LLM Extraction via Groq
        system_prompt = (
            "You are an expert audio and video content analyzer.\n"
            "You must respond strictly with a valid raw JSON object matching the requested schema.\n\n"
            "Rules:\n"
            "1. Identify content 'category': 'meeting', 'tutorial', 'news', or 'presentation'.\n"
            "2. Provide a clear 2-3 sentence 'summary'.\n"
            "3. For 'tutorial' or 'presentation' content: populate 'key_takeaways' with actionable points/tips. Leave 'key_decisions' and 'action_items' as empty lists [].\n"
            "4. For 'meeting' content: populate 'key_decisions' and 'action_items'. Leave 'key_takeaways' empty [] if not applicable.\n"
            "5. Ensure ALL schema keys ('category', 'summary', 'key_takeaways', 'key_decisions', 'action_items') are present in the JSON response.\n"
            "6. Do NOT include markdown formatting (like ```json), introductions, or commentary."
        )

        user_prompt = f"""Analyze the transcript below and extract structured information.

Output MUST strictly match this JSON schema:
{json.dumps(MeetingAnalysis.model_json_schema(), indent=2)}

Transcript:
{transcription}
"""

        response = groq_client.chat.completions.create(
            model="qwen/qwen3.6-27b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            max_tokens=4096
        )

        raw_json = json.loads(response.choices[0].message.content)
        validated_data = MeetingAnalysis(**raw_json)

        result_payload = {
            "timestamp": datetime.now().strftime("%b %d, %Y • %I:%M %p"),
            "filename": file.filename,
            "transcript": transcription,
            "analysis": validated_data.model_dump()
        }

        # Save record to local JSON store
        save_to_history(result_payload)

        return {"status": "success", **result_payload}

    except subprocess.CalledProcessError:
        raise HTTPException(status_code=500, detail="FFmpeg media extraction failed. Check media format.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

    finally:
        # Cleanup temporary files
        for file_path in [temp_input_path, compressed_audio_path]:
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception:
                    pass