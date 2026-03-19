#!/bin/bash
set -e

TUNNEL_MODE="${TUNNEL_MODE:-none}"

start_tailscale() {
    echo "[tunnel] Starting Tailscale..."
    mkdir -p /var/run/tailscale /var/lib/tailscale
    tailscaled --state=/var/lib/tailscale/tailscaled.state --socket=/var/run/tailscale/tailscaled.sock &
    sleep 5
    tailscale --socket=/var/run/tailscale/tailscaled.sock up --authkey="${TS_AUTHKEY}" --accept-dns=false
    sleep 5
    NODE_NAME=$(tailscale --socket=/var/run/tailscale/tailscaled.sock status --self 2>/dev/null | head -1 | awk '{print $2}')
    tailscale --socket=/var/run/tailscale/tailscaled.sock serve --bg --https=443 http://127.0.0.1:8000
    tailscale --socket=/var/run/tailscale/tailscaled.sock funnel --bg 443
    echo "[tunnel] Tailscale Funnel ready: https://${NODE_NAME}"
}

start_cloudflare() {
    echo "[tunnel] Starting Cloudflare anonymous tunnel..."
    cloudflared tunnel --url http://localhost:8000 2>/tmp/cloudflared.log &
    sleep 5
    CF_URL=$(grep -o 'https://[a-z0-9-]*\.trycloudflare\.com' /tmp/cloudflared.log | head -1)
    if [ -n "$CF_URL" ]; then
        echo "[tunnel] Cloudflare tunnel ready: $CF_URL"
    else
        echo "[tunnel] Waiting for Cloudflare tunnel URL..."
        for i in $(seq 1 15); do
            CF_URL=$(grep -o 'https://[a-z0-9-]*\.trycloudflare\.com' /tmp/cloudflared.log | head -1)
            [ -n "$CF_URL" ] && break
            sleep 2
        done
        echo "[tunnel] Cloudflare tunnel ready: $CF_URL"
    fi
}

case "$TUNNEL_MODE" in
    tailscale)
        if [ -z "$TS_AUTHKEY" ]; then
            echo "Error: TS_AUTHKEY is required for tailscale mode"
            exit 1
        fi
        start_tailscale
        ;;
    cloudflare)
        start_cloudflare
        ;;
    none)
        echo "[tunnel] No tunnel, local mode"
        ;;
    *)
        echo "Error: Unknown TUNNEL_MODE '$TUNNEL_MODE' (none|tailscale|cloudflare)"
        exit 1
        ;;
esac

exec uvicorn app.main:app --host 0.0.0.0 --port 8000
