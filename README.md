<<<<<<< HEAD
# cognee-agentic-mem
=======
# Private Cognee Memory App

A local-only demo using the Python `cognee` package, FastAPI, Node.js, and Ollama.

## Architecture

Browser (`127.0.0.1:3000`) -> Node.js proxy -> FastAPI (`127.0.0.1:8000`) -> Cognee -> local SQLite + LanceDB + Kuzu + Ollama.

The browser never stores the FastAPI token. Node keeps it server-side and adds it to proxied requests.

## Files

- `.env` / `.env.example`: local configuration and privacy controls
- `requirements.txt`: Python dependencies
- `backend/sample_data/chunks.json`: six sample chunks
- `backend/ingest_sample.py`: loads those chunks through `cognee.remember`
- `backend/app/memory_service.py`: `remember`, `recall`, `improve`, `forget`
- `backend/app/main.py`: secured FastAPI API
- `backend/run_api.py`: local API launcher
- `frontend/server.mjs`: local Node server + reverse proxy
- `frontend/public/*`: simple UI

## Requirements

- Python 3.10-3.14
- Node.js 18+
- Ollama
- An Ollama chat model and embedding model

## Commands (PowerShell)

From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Install Ollama models:

```powershell
ollama pull llama3.1:8b
ollama pull nomic-embed-text
```

Generate a random API token and update `.env`:

```powershell
$token = [guid]::NewGuid().ToString('N') + [guid]::NewGuid().ToString('N')
$token
```

Set `BACKEND_API_TOKEN=` in `.env` to that value.

Start FastAPI in terminal 1:

```powershell
cd backend
..\.venv\Scripts\python.exe run_api.py
```

Run the ingestion script once in terminal 2:

```powershell
cd backend
..\.venv\Scripts\python.exe ingest_sample.py
```

Start Node.js in terminal 3:

```powershell
cd frontend
$env:BACKEND_API_TOKEN = (Get-Content ..\.env | Where-Object { $_ -match '^BACKEND_API_TOKEN=' }) -replace '^BACKEND_API_TOKEN=', ''
$env:BACKEND_PORT = '8000'
$env:FRONTEND_PORT = '3000'
npm start
```

Open:

`http://127.0.0.1:3000`

## Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
ollama pull llama3.1:8b
ollama pull nomic-embed-text
```

Terminal 1:

```bash
cd backend
../.venv/bin/python run_api.py
```

Terminal 2:

```bash
cd backend
../.venv/bin/python ingest_sample.py
```

Terminal 3:

```bash
cd frontend
export BACKEND_API_TOKEN="$(grep '^BACKEND_API_TOKEN=' ../.env | cut -d= -f2-)"
export BACKEND_PORT=8000
export FRONTEND_PORT=3000
npm start
```

Open `http://127.0.0.1:3000`.

## Direct API smoke tests

Health:

```bash
curl http://127.0.0.1:8000/health
```

Recall through the API requires the secret header:

```bash
curl -X POST http://127.0.0.1:8000/memory/recall \
  -H "content-type: application/json" \
  -H "x-api-key: YOUR_BACKEND_API_TOKEN" \
  -d '{"query":"Which databases does Aurora use for memory?","top_k":5}'
```

## Privacy notes

1. The API and UI bind to `127.0.0.1`, not `0.0.0.0`.
2. Only `http://127.0.0.1:3000` is allowed by FastAPI CORS.
3. Every memory endpoint requires `X-API-Key`.
4. The browser never receives the API token; Node proxies requests and injects it server-side.
5. The backend never logs request bodies and uvicorn access logs are disabled.
6. The Cognee telemetry switch is disabled with `TELEMETRY_DISABLED=1` and `ENV=dev`.
7. Ollama is configured on `127.0.0.1`; no OpenAI/cloud provider is configured.
8. Cognee relational/vector/graph state is stored under `backend/data/` and is ignored by Git.
9. The API exposes only one fixed dataset name (`private_memory`); callers cannot choose another dataset.
10. `forget` deletes the Cognee dataset and its graph/vector/raw data records, but the sample source JSON remains so you can ingest again.

This is a strong local-development setup. For production, add TLS, a real identity provider, OS/container hardening, encrypted disks/backups, secret management, and network policy.
>>>>>>> ed9b985 (Cognee implementation with sample data)
