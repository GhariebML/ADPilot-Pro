# ADPilot Pro — Local Run & Verification Guide (Windows PowerShell)

This guide provides the exact PowerShell commands to configure, start, verify, and demo the complete **ADPilot Pro** platform locally on Windows.

---

## A. Prerequisites

Verify installed runtime versions in PowerShell:

```powershell
# 1. Verify Python (>= 3.12 required)
python --version

# 2. Verify Node.js (>= 18 required)
node --version

# 3. Verify npm
npm --version

# 4. (Optional) Verify Git and Docker
git --version
docker --version
```

---

## B. Environment Setup

Create your local `.env` configuration file from the template:

```powershell
# Navigate to repository root
Set-Location -Path d:\ADP\ADPilot_Pro

# Copy example environment configuration
Copy-Item .env.example .env
```

*(Optional)* If you have an LLM API key, open `.env` and configure:
```ini
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your_openrouter_api_key_here
```
> **Note:** If no API key is provided, the system automatically uses deterministic offline ML models and fallback heuristics.

---

## C. Python Virtual Environment

Create and activate a dedicated virtual environment:

```powershell
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment in PowerShell
.\venv\Scripts\Activate.ps1
```
*(If execution policy restricts scripts: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

---

## D. Backend Installation

Install all backend dependencies in editable development mode:

```powershell
# Upgrade pip and build tools
python -m pip install --upgrade pip setuptools wheel

# Install core dependencies and development tools
pip install -e ".[dev]"
```

---

## E. Frontend Installation

Install Node.js dependencies for the React/Vite dashboard:

```powershell
# Navigate into frontend directory and install dependencies
Set-Location -Path d:\ADP\ADPilot_Pro\frontend
npm install

# Return to repository root
Set-Location -Path d:\ADP\ADPilot_Pro
```

---

## F. Database Startup

By default, ADPilot Pro uses embedded async SQLite (`sqlite+aiosqlite:///./adpilot.db`), which initializes automatically on startup.

To explicitly test and seed the database schema:
```powershell
# Initialize database tables and check connection
python -c "import asyncio; from adpilot.core.database import init_db, create_tables; asyncio.run(init_db()); asyncio.run(create_tables()); print('Database initialized successfully.')"
```

*(Optional PostgreSQL)* If using external PostgreSQL:
```powershell
# Set PostgreSQL connection in PowerShell environment
$env:DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/adpilot"
```

---

## G. Redis Startup (Optional for Background Queue)

Redis is required only if you run the asynchronous background task worker (`arq`). For direct API calls and pipeline execution, Redis is optional.

**Option 1: Via Docker (Recommended for Windows)**
```powershell
docker run -d --name adpilot-redis -p 6379:6379 redis:7-alpine
```

**Option 2: Native / WSL Redis**
```powershell
wsl redis-server
```

---

## H. Vector Database Startup (Qdrant)

By default, ADPilot Pro uses embedded local disk storage at `./storage/qdrant_rag` (with automatic `:memory:` fallback), requiring no external server.

*(Optional)* To run external Qdrant in Docker:
```powershell
docker run -d --name adpilot-qdrant -p 6333:6333 -p 6334:6334 -v "${PWD}/storage/qdrant_docker:/qdrant/storage" qdrant/qdrant:latest
```

---

## I. Background Task Worker Startup (Optional)

If running the asynchronous dashboard task queue:

```powershell
# Start ARQ background worker
$env:PYTHONPATH="src"
arq src.adpilot.worker.WorkerSettings
```

---

## J. Backend API Server Startup

Launch the FastAPI backend server with hot reloading:

```powershell
# Set python path and start Uvicorn
$env:PYTHONPATH="src"
uvicorn adpilot.api.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be live at `http://localhost:8000`.  
Interactive Swagger documentation: `http://localhost:8000/docs`.

---

## K. Frontend Dashboard Startup

Open a **separate** PowerShell terminal and launch the Vite dev server:

```powershell
Set-Location -Path d:\ADP\ADPilot_Pro\frontend
npm run dev
```

The dashboard will be available in your browser at:  
👉 **`http://localhost:3000`**

---

## L. Seed & Demo Data Setup

Verify existing sample campaign brief payloads:

```powershell
# View sample brief data
Get-Content data\samples\campaign_input_sample.json | ConvertFrom-Json | Format-List
```

---

## M. Health Checks & Verification

Open a new PowerShell terminal to verify backend service health:

```powershell
# 1. Check root health endpoint
Invoke-RestMethod -Uri "http://localhost:8000/healthz" -Method Get

# 2. Check API v1 health endpoint
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/health" -Method Get
```

Expected Response:
```json
{"status": "ok", "app": "ADPilot Pro", "version": "2.0.0"}
```

---

## N. API Pipeline Verification

Test running a standalone campaign brief through the REST API:

```powershell
# Submit a sample campaign brief to the API
$body = @{
    name = "Apex Enterprise Stream"
    product_name = "Apex Engine"
    product_type = "saas"
    target_audience = "Enterprise Cloud Architects"
    budget = 10000.0
    goals = @("lead_generation")
    channels = @("linkedin")
    tone = "professional"
    duration = "1-month"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/campaigns" -Method Post -Body $body -ContentType "application/json"
```

---

## O. Full 18-Stage Master Pipeline Live Demo

Execute the complete 18-stage end-to-end Master Pipeline demo across all 4 industry archetypes:

```powershell
# Run the Master Pipeline Verification script
$env:PYTHONPATH="src"
python scripts/verify_phase16.py
```

Run RAG & Epistemic Memory Verification:
```powershell
$env:PYTHONPATH="src"
python scripts/verify_phase15.py
```

Run the Full 217-Test Regression Suite:
```powershell
pytest tests/ -v
```

---

## P. Troubleshooting Guide

| Issue | Root Cause | Solution |
| :--- | :--- | :--- |
| `ExecutionPolicy` error on `Activate.ps1` | PowerShell script restriction | Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` |
| `ModuleNotFoundError: No module named 'adpilot'` | `PYTHONPATH` not set | Run `$env:PYTHONPATH="src"` before running python scripts |
| Port `8000` or `3000` already in use | Conflicting background process | Check port with `Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess` |
| SQLite locking warning | Multi-threaded local file access | System automatically falls back gracefully; no action needed |
| Missing `frontend/node_modules` | Node packages not installed | Run `npm install` inside the `frontend/` directory |
