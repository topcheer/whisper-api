import os
import subprocess
import tempfile
import time
import logging
from pathlib import Path

from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Whisper API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

WHISPER_MODEL = "turbo"
WHISPER_MODEL_DIR = os.getenv("WHISPER_MODEL_DIR", "/root/.cache/whisper")
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", None)


@app.post("/v1/audio/transcriptions")
async def transcriptions(
    file: UploadFile = File(...),
    model: str = Form("turbo"),
    language: str = Form(None),
    prompt: str = Form(None),
    response_format: str = Form("json"),
    temperature: str = Form("0"),
    timestamp_granularities: str = Form(None),
):

    suffix = Path(file.filename).suffix if file.filename else ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        start = time.time()

        cmd = [
            "whisper",
            tmp_path,
            "--model", WHISPER_MODEL,
            "--model_dir", WHISPER_MODEL_DIR,
            "--output_format", "json",
            "--task", "transcribe",
        ]

        if language:
            cmd.extend(["--language", language])
        elif DEFAULT_LANGUAGE:
            cmd.extend(["--language", DEFAULT_LANGUAGE])

        if prompt:
            cmd.extend(["--initial_prompt", prompt])

        if temperature:
            cmd.extend(["--temperature", temperature])

        if timestamp_granularities and "word" in timestamp_granularities:
            cmd.append("--word_timestamps")

        cmd.append("--output_dir")
        cmd.append(os.path.dirname(tmp_path))

        logger.info("Running: %s", " ".join(cmd))
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            logger.error("whisper stderr: %s", result.stderr)
            raise HTTPException(status_code=500, detail=f"Transcription failed: {result.stderr[:500]}")

        elapsed = time.time() - start

        json_path = Path(tmp_path).with_suffix(".json")
        if not json_path.exists():
            raise HTTPException(status_code=500, detail="Transcription output not found")

        import json as json_mod
        with open(json_path) as f:
            data = json_mod.load(f)

        if response_format == "verbose_json":
            return {
                "id": f"whisper-{int(time.time())}",
                "object": "whisper.result",
                "created": int(time.time()),
                "model": WHISPER_MODEL,
                "data": data,
                "processing_time": round(elapsed, 2),
            }
        else:
            text = data.get("text", "")
            segments = data.get("segments", [])
            full_text = " ".join(s.get("text", "") for s in segments) if segments else text
            return {
                "id": f"whisper-{int(time.time())}",
                "object": "whisper.result",
                "created": int(time.time()),
                "model": WHISPER_MODEL,
                "text": full_text.strip(),
            }
    finally:
        for ext in [".wav", ".mp3", ".m4a", ".flac", ".ogg", ".webm", ".json"]:
            p = Path(tmp_path).with_suffix(ext)
            if p.exists():
                p.unlink()


@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [{"id": WHISPER_MODEL, "object": "model", "owned_by": "openai"}],
    }


@app.get("/health")
async def health():
    return {"status": "ok"}
