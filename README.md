# Whisper API

OpenAI-compatible speech-to-text API powered by OpenAI Whisper CLI.

## Quick Start

### Use pre-built image

```bash
docker run -d -p 8090:8000 --name whisper-api ggai/whisper-api
```

### Build from source

```bash
# Build and start
docker compose up -d --build

# View logs
docker compose logs -f
```

The service will be available at `http://localhost:8090`.

## Expose via Tunnel

Set `TUNNEL_MODE` in docker-compose.yml to expose the service publicly.

### Tailscale Funnel

1. Get an auth key from [Tailscale Admin Console](https://login.tailscale.com/admin/settings/keys) (check "Reusable" and enable Funnel)
2. Configure in docker-compose.yml:

```yaml
environment:
  - TUNNEL_MODE=tailscale
  - TS_AUTHKEY=tskey-auth-xxxxx
```

3. First run will print an authorization link in the logs. Open it to enable Funnel on your tailnet (one-time only)
4. The public URL will be printed in the logs on subsequent starts

### Cloudflare Anonymous Tunnel

No account or token needed. Just set the mode:

```yaml
environment:
  - TUNNEL_MODE=cloudflare
```

A random `*.trycloudflare.com` URL will be generated and printed in the logs on each startup.

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

## Authentication

Set `API_KEY_ENABLED=true` in docker-compose.yml to enable API key authentication.

A random API key will be generated on each startup and printed in the logs:

```
docker compose logs | grep "API key"
```

Requests must include the key in the `Authorization` header:

```bash
curl -X POST http://localhost:8090/v1/audio/transcriptions \
  -H "Authorization: Bearer <your-api-key>" \
  -F "file=@audio.wav"
```

The `/health` endpoint is exempt from authentication.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `API_KEY_ENABLED` | `false` | Enable API key authentication |
| `TUNNEL_MODE` | `none` | Tunnel mode: `none`, `tailscale`, `cloudflare` |
| `TS_AUTHKEY` | (empty) | Tailscale auth key (required for tailscale mode) |
| `WHISPER_MODEL_DIR` | `/root/.cache/whisper` | Model cache directory |
| `DEFAULT_LANGUAGE` | (empty) | Default language, auto-detect if empty |

## Project Structure

```
whisper-api/
├── app/
│   └── main.py              # FastAPI application
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh            # Startup script with tunnel support
├── requirements.txt
└── README.md
```

---

<!-- Chinese version / 中文版 -->

# Whisper API

基于 OpenAI Whisper CLI 的 OpenAI 兼容语音转文字 API 服务。

## 快速开始

### 使用预构建镜像

```bash
docker run -d -p 8090:8000 --name whisper-api ggai/whisper-api
```

### 从源码构建

```bash
# 构建并启动
docker compose up -d --build

# 查看日志
docker compose logs -f
```

服务启动后访问 `http://localhost:8090`。

## 通过隧道暴露服务

在 docker-compose.yml 中设置 `TUNNEL_MODE` 即可将服务暴露到公网。

### Tailscale Funnel

1. 从 [Tailscale 管理后台](https://login.tailscale.com/admin/settings/keys) 获取 Auth Key（勾选"可复用"并启用 Funnel）
2. 在 docker-compose.yml 中配置：

```yaml
environment:
  - TUNNEL_MODE=tailscale
  - TS_AUTHKEY=tskey-auth-xxxxx
```

3. 首次启动时日志中会打印授权链接，打开链接在管理后台启用 Funnel（仅需一次）
4. 后续启动公网地址会打印到日志中

### Cloudflare 匿名隧道

无需账号或 Token，只需设置模式：

```yaml
environment:
  - TUNNEL_MODE=cloudflare
```

每次启动会自动生成一个随机的 `*.trycloudflare.com` 地址并打印到日志中。

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

## API Key 认证

在 docker-compose.yml 中设置 `API_KEY_ENABLED=true` 开启 API Key 认证。

每次启动时会随机生成 API Key 并打印到日志中：

```
docker compose logs | grep "API key"
```

请求时需要在 `Authorization` 头中携带 Key：

```bash
curl -X POST http://localhost:8090/v1/audio/transcriptions \
  -H "Authorization: Bearer <your-api-key>" \
  -F "file=@audio.wav"
```

`/health` 接口不受认证限制。

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `API_KEY_ENABLED` | `false` | 是否开启 API Key 认证 |
| `TUNNEL_MODE` | `none` | 隧道模式：`none`、`tailscale`、`cloudflare` |
| `TS_AUTHKEY` | 空 | Tailscale 认证密钥（tailscale 模式必填） |
| `WHISPER_MODEL_DIR` | `/root/.cache/whisper` | 模型缓存目录 |
| `DEFAULT_LANGUAGE` | 空 | 默认语言，空则自动检测 |

## 项目结构

```
whisper-api/
├── app/
│   └── main.py              # FastAPI 应用
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh            # 启动脚本（含隧道支持）
├── requirements.txt
└── README.md
```
