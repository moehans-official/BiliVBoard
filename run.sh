#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_COLLECTOR_DIR="$SCRIPT_DIR/DataCollector"
FRONTEND_DIR="$SCRIPT_DIR/frontend/bilivboard-sveltekit"
BACKEND_DIR="$SCRIPT_DIR/backend"
DB_FILE="$DATA_COLLECTOR_DIR/bilibili_video_data.db"

echo "=== BiliVBoard 自动化流水线 ==="
echo ""

# Step 1: Extract BVIDs from songs.json
echo "[1/4] 提取 BVID..."
python3 "$SCRIPT_DIR/extract_bvids.py"
echo ""

# Step 2: Run DataCollector (limit to top 100 for speed, configurable)
LIMIT=${1:-100}
echo "[2/4] 运行数据采集器 (限制 $LIMIT 个视频)..."
cd "$DATA_COLLECTOR_DIR"

# Create a temporary limited bvid.txt
head -n "$LIMIT" bvid.txt > bvid_limited.txt
mv bvid_limited.txt bvid.txt

python3 main.py normal
echo ""

# Step 3: Kill existing servers
echo "[3/4] 重启服务..."
pkill -f "uvicorn main:app" 2>/dev/null || true
pkill -f "vite dev" 2>/dev/null || true
sleep 1

# Start backend
cd "$BACKEND_DIR"
nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
echo "  后端已启动 (PID: $BACKEND_PID)"

# Start frontend
cd "$FRONTEND_DIR"
nohup npm run dev > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "  前端已启动 (PID: $FRONTEND_PID)"

echo ""
echo "[4/4] 完成!"
echo ""
echo "=== 运行信息 ==="
echo "数据库: $DB_FILE"
echo "后端 API: http://localhost:8000"
echo "前端预览: http://localhost:5173"
echo ""
echo "使用方式:"
echo "  ./run.sh          # 默认采集 100 个视频"
echo "  ./run.sh 50       # 采集 50 个视频"
echo "  ./run.sh 200      # 采集 200 个视频"
