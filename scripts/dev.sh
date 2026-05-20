#!/usr/bin/env bash
# LeafLens — local development launcher.
# Starts the Flask backend on port 5001 and the Vite dev server on 5173.
# Press Ctrl+C once to stop both cleanly.
#
# Usage:
#   ./scripts/dev.sh
#
# Override ports:
#   BACKEND_PORT=5002 FRONTEND_PORT=3000 ./scripts/dev.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

BACKEND_PORT="${BACKEND_PORT:-5001}"
FRONTEND_PORT="${FRONTEND_PORT:-5173}"
LOG_DIR="$REPO_ROOT/.dev-logs"
mkdir -p "$LOG_DIR"

# Colors
G="\033[0;32m"; B="\033[0;34m"; Y="\033[0;33m"; R="\033[0;31m"; N="\033[0m"

# --- pre-flight checks ---
if [ ! -d .venv ]; then
    echo -e "${R}ERROR${N}: .venv not found. Run ./scripts/setup.sh first."
    exit 1
fi
if [ ! -d frontend/node_modules ]; then
    echo -e "${R}ERROR${N}: frontend/node_modules not found. Run ./scripts/setup.sh first."
    exit 1
fi
if [ ! -f models/checkpoints/best.pt ]; then
    echo -e "${Y}WARN${N}: no model at models/checkpoints/best.pt — /api/predict will return 503"
fi
if [ ! -f backend/leaflens.db ]; then
    echo -e "${Y}WARN${N}: no DB at backend/leaflens.db — run 'python scripts/seed_db.py' first"
fi

# --- check ports are free ---
for port in "$BACKEND_PORT" "$FRONTEND_PORT"; do
    if lsof -ti tcp:"$port" >/dev/null 2>&1; then
        echo -e "${R}ERROR${N}: port $port is already in use."
        echo "  Free it with: lsof -ti tcp:$port | xargs kill"
        exit 1
    fi
done

# --- cleanup on Ctrl+C ---
BACKEND_PID=""
FRONTEND_PID=""

cleanup() {
    echo ""
    echo -e "${Y}Stopping LeafLens dev servers...${N}"
    [ -n "$BACKEND_PID" ] && kill "$BACKEND_PID" 2>/dev/null || true
    [ -n "$FRONTEND_PID" ] && kill "$FRONTEND_PID" 2>/dev/null || true
    # also kill any child workers spawned by the data loader / vite
    pkill -P $$ 2>/dev/null || true
    sleep 1
    echo -e "${G}Stopped.${N}"
}
trap cleanup INT TERM EXIT

# --- start backend ---
echo -e "${B}→${N} Starting backend on http://localhost:$BACKEND_PORT ..."
(
    source .venv/bin/activate
    exec python -c "
from backend.app import create_app
app = create_app()
app.run(host='127.0.0.1', port=$BACKEND_PORT, debug=False, use_reloader=False)
" > "$LOG_DIR/backend.log" 2>&1
) &
BACKEND_PID=$!

# Wait until /api/health responds (max 30 s)
SECONDS_WAITED=0
until curl -sf "http://localhost:$BACKEND_PORT/api/health" >/dev/null 2>&1; do
    if ! kill -0 "$BACKEND_PID" 2>/dev/null; then
        echo -e "${R}Backend died on startup. Tail of log:${N}"
        tail -20 "$LOG_DIR/backend.log"
        exit 1
    fi
    if [ "$SECONDS_WAITED" -ge 30 ]; then
        echo -e "${R}Backend did not become ready within 30 s. Check $LOG_DIR/backend.log${N}"
        exit 1
    fi
    sleep 1
    SECONDS_WAITED=$((SECONDS_WAITED + 1))
done
echo -e "${G}✓${N} Backend ready at http://localhost:$BACKEND_PORT"

# --- start frontend ---
echo -e "${B}→${N} Starting frontend on http://localhost:$FRONTEND_PORT ..."
(
    cd frontend
    exec env VITE_API_BASE_URL="http://localhost:$BACKEND_PORT" \
         npm run dev -- --port "$FRONTEND_PORT" --strictPort > "$LOG_DIR/frontend.log" 2>&1
) &
FRONTEND_PID=$!

SECONDS_WAITED=0
until curl -sf "http://localhost:$FRONTEND_PORT" >/dev/null 2>&1; do
    if ! kill -0 "$FRONTEND_PID" 2>/dev/null; then
        echo -e "${R}Frontend died on startup. Tail of log:${N}"
        tail -20 "$LOG_DIR/frontend.log"
        exit 1
    fi
    if [ "$SECONDS_WAITED" -ge 30 ]; then
        echo -e "${R}Frontend did not become ready within 30 s. Check $LOG_DIR/frontend.log${N}"
        exit 1
    fi
    sleep 1
    SECONDS_WAITED=$((SECONDS_WAITED + 1))
done
echo -e "${G}✓${N} Frontend ready at http://localhost:$FRONTEND_PORT"

# --- summary ---
echo ""
echo -e "${G}LeafLens is running.${N}"
echo ""
echo -e "  ${B}Frontend${N}   http://localhost:$FRONTEND_PORT"
echo -e "  ${B}Backend${N}    http://localhost:$BACKEND_PORT/api/health"
echo -e "  ${B}Logs${N}       $LOG_DIR/{backend,frontend}.log"
echo ""
echo -e "  Press ${Y}Ctrl+C${N} to stop both."
echo ""

# Keep the script alive while the children run
wait
