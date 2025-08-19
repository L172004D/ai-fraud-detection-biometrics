#!/usr/bin/env bash
set -e

# create venv if not exists
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate

pip install -r requirements.txt

# start uvicorn (backend)
echo "Starting FastAPI on http://127.0.0.1:8000"
uvicorn backend.main:app --reload & 
UVICORN_PID=$!

# start streamlit (dashboard)
echo "Starting Streamlit on http://127.0.0.1:8501"
streamlit run dashboard/app.py & 
ST_PID=$!

# serve frontend static files
echo "Serving frontend on http://127.0.0.1:8080"
python3 -m http.server 8080 --directory frontend & 
HTTP_PID=$!

echo "Demo started. UVICORN=$UVICORN_PID ST=$ST_PID HTTP=$HTTP_PID"
wait $UVICORN_PID $ST_PID $HTTP_PID
