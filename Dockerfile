FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir openai-whisper

COPY app/ ./app/

EXPOSE 8000

ENV WHISPER_MODEL_DIR=/root/.cache/whisper
ENV DEFAULT_MODEL=turbo

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
