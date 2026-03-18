# Whisper API

OpenAI-compatible speech-to-text API powered by OpenAI Whisper CLI.

## Quick Start

```bash
# Build and start
docker compose up -d --build

# View logs
docker compose logs -f
```

The service will be available at `http://localhost:8090`.

## OpenClaw Integration

Replace `{WHISPER_URL}` with your actual deployment address (e.g. `http://192.168.31.105:8090`):

```bash
openclaw config set tools.media.audio.models '[{"model":"whisper-1","baseUrl":"{WHISPER_URL}","headers":{"Authorization":"Bearer local"}}]'
```

## API

### Transcribe Audio

```
POST /v1/audio/transcriptions
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file | file | Yes | Audio file (wav/mp3/m4a/flac/ogg/webm) |
| model | string | No | Fixed to turbo, any value will be ignored |
| language | string | No | Language code (e.g. zh/en/ja), auto-detect if omitted |
| prompt | string | No | Context prompt to guide transcription style |
| response_format | string | No | `json` (default) or `verbose_json` |
| temperature | string | No | Sampling temperature, default 0 |
| timestamp_granularities | string | No | Set to `word` to enable word-level timestamps |

**Example request:**

```bash
curl -X POST http://localhost:8090/v1/audio/transcriptions \
  -F "file=@audio.wav" \
  -F "language=zh"
```

**Example response (json):**

```json
{
  "id": "whisper-1773844245",
  "object": "whisper.result",
  "created": 1773844245,
  "model": "turbo",
  "text": "Transcribed text"
}
```

**Example response (verbose_json):**

```json
{
  "id": "whisper-1773844245",
  "object": "whisper.result",
  "created": 1773844245,
  "model": "turbo",
  "processing_time": 211.5,
  "data": {
    "text": "Transcribed text",
    "segments": [...],
    "language": "zh"
  }
}
```

### Other Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/models` | GET | List available models |
| `/health` | GET | Health check |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `WHISPER_MODEL_DIR` | `/root/.cache/whisper` | Model cache directory |
| `DEFAULT_LANGUAGE` | (empty) | Default language, auto-detect if empty |

## Project Structure

```
whisper-api/
├── app/
│   └── main.py          # FastAPI application
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

<!-- Chinese version / 中文版 -->

# Whisper API

基于 OpenAI Whisper CLI 的 OpenAI 兼容语音转文字 API 服务。

## 快速开始

```bash
# 构建并启动
docker compose up -d --build

# 查看日志
docker compose logs -f
```

服务启动后访问 `http://localhost:8090`。

## 接入 OpenClaw

将 `{WHISPER_URL}` 替换为实际部署地址（如 `http://192.168.31.105:8090`）：

```bash
openclaw config set tools.media.audio.models '[{"model":"whisper-1","baseUrl":"{WHISPER_URL}","headers":{"Authorization":"Bearer local"}}]'
```

## API

### 语音转文字

```
POST /v1/audio/transcriptions
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | file | 是 | 音频文件（wav/mp3/m4a/flac/ogg/webm） |
| model | string | 否 | 固定使用 turbo，传参会被忽略 |
| language | string | 否 | 指定语言（如 zh/en/ja），不传则自动检测 |
| prompt | string | 否 | 提示词，引导转写风格 |
| response_format | string | 否 | `json`（默认）或 `verbose_json` |
| temperature | string | 否 | 采样温度，默认 0 |
| timestamp_granularities | string | 否 | 设为 `word` 启用词级时间戳 |

**请求示例：**

```bash
curl -X POST http://localhost:8090/v1/audio/transcriptions \
  -F "file=@audio.wav" \
  -F "language=zh"
```

**响应示例（json）：**

```json
{
  "id": "whisper-1773844245",
  "object": "whisper.result",
  "created": 1773844245,
  "model": "turbo",
  "text": "转写结果文本"
}
```

**响应示例（verbose_json）：**

```json
{
  "id": "whisper-1773844245",
  "object": "whisper.result",
  "created": 1773844245,
  "model": "turbo",
  "processing_time": 211.5,
  "data": {
    "text": "转写结果文本",
    "segments": [...],
    "language": "zh"
  }
}
```

### 其他接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/v1/models` | GET | 查看可用模型 |
| `/health` | GET | 健康检查 |

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `WHISPER_MODEL_DIR` | `/root/.cache/whisper` | 模型缓存目录 |
| `DEFAULT_LANGUAGE` | 空 | 默认语言，空则自动检测 |

## 项目结构

```
whisper-api/
├── app/
│   └── main.py          # FastAPI 应用
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```
