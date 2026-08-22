# Local Deployment & Execution Guide

**Status:** [IMPLEMENTED]  
**OS Target:** Windows (PowerShell) / Linux / macOS  

---

## 1. Prerequisites
- **Python:** 3.12 or higher (`python --version`)
- **Node.js:** 20 or higher (`node -v`)
- **Redis:** Running locally or accessible remotely

---

## 2. Windows PowerShell Step-by-Step Instructions

### Step 1: Clone Repository & Create Virtual Environment
```powershell
git clone https://github.com/GhariebML/ADPilot-Pro.git
cd ADPilot-Pro

python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 2: Install Python Dependencies
```powershell
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Step 3: Configure Environment Variables
```powershell
Copy-Item .env.example .env
# Edit .env with your LLM API keys (or run in default simulated demo mode)
```

### Step 4: Start the FastAPI Backend Server
```powershell
$env:PYTHONPATH="src"
uvicorn adpilot.api.main:app --host 127.0.0.1 --port 8001 --reload
```
- Health Check: `http://127.0.0.1:8001/healthz`
- Swagger Documentation: `http://127.0.0.1:8001/docs`

### Step 5: Start the React Frontend Dashboard (Separate PowerShell Terminal)
```powershell
cd frontend
npm install
npm run dev
```
- Open browser at: `http://localhost:3000`

---

## 3. Docker Multi-Container Deployment

```powershell
docker-compose up --build -d
```
Boots:
- `fastapi-backend` on port `8000`
- `vite-frontend` on port `3000`
- `redis` on port `6379`
- `qdrant` on port `6333`
