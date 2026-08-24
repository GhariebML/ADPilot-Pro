# ADPilot Pro — Vercel Production Deployment Guide

> **Enterprise Autonomous Marketing Operating System**  
> **Authoritative Deployment & Hosting Specification**

---

## 🌟 Executive Overview

ADPilot Pro is structured with a high-performance **React 18 + Vite 7 + TypeScript** dashboard paired with an **AsyncIO FastAPI 2.0 / Python 3.12+** multi-agent backend.

This guide provides the exact, production-grade instructions to deploy the ADPilot Pro frontend to **Vercel** with zero configuration friction, automated CI/CD synchronization with GitHub, and seamless API routing.

---

## 🚀 Method 1: 1-Click GitHub Integration (Recommended)

### Step 1: Log in to Vercel
1. Go to [https://vercel.com](https://vercel.com) and log in with your GitHub account.
2. Click the **"Add New..."** button in your dashboard and select **"Project"**.

### Step 2: Import the GitHub Repository
1. In the search box, find **`GhariebML/ADPilot-Pro`**.
2. Click **"Import"**.

### Step 3: Configure Project Build Settings
Vercel will detect Vite automatically. Verify or set the following values:

| Configuration Field | Value | Notes |
| :--- | :--- | :--- |
| **Project Name** | `adpilot-pro` | (Or your custom project name) |
| **Framework Preset** | `Vite` | Auto-detected |
| **Root Directory** | `frontend` | ⚠️ **Click "Edit" and choose `frontend`** |
| **Build Command** | `npm run build` | Default |
| **Output Directory** | `dist` | Default |
| **Install Command** | `npm install` | Default |

### Step 4: Add Environment Variables (Optional)
In the **"Environment Variables"** accordion section, add:

```env
VITE_API_URL=https://your-adpilot-backend-url.com/api
VITE_APP_TITLE=ADPilot Pro
VITE_APP_VERSION=3.0.0
```
> *Note: If `VITE_API_URL` is omitted, the frontend automatically runs in interactive standalone demonstration and simulation mode.*

### Step 5: Deploy
Click **"Deploy"**. Vercel will build the frontend in ~15 seconds and provide a production HTTPS URL (e.g. `https://adpilot-pro.vercel.app`).

---

## 💻 Method 2: Deployment via Vercel CLI

If you prefer deploying directly from your terminal:

```bash
# 1. Navigate to the frontend directory
cd frontend

# 2. Login to Vercel (first time only)
npx vercel login

# 3. Deploy to Preview
npx vercel

# 4. Deploy directly to Production
npx vercel --prod
```

When prompted by the CLI:
- `Set up and deploy "frontend"?` -> **Yes (`y`)**
- `Which scope do you want to deploy to?` -> Select your personal/team account
- `Link to existing project?` -> **No (`N`)** (or Yes if linking)
- `What's your project's name?` -> **`adpilot-pro`**
- `In which directory is your code located?` -> **`./`**
- `Want to modify these settings?` -> **No (`N`)**

---

## 🛠️ Vercel Configuration Reference (`vercel.json`)

The repository includes pre-configured `vercel.json` files for both root and frontend deployments:

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "framework": "vite",
  "cleanUrls": true,
  "trailingSlash": false,
  "rewrites": [
    {
      "source": "/((?!api/|assets/|favicon|logo|.*\\..*).*)",
      "destination": "/index.html"
    }
  ],
  "headers": [
    {
      "source": "/assets/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    },
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "X-XSS-Protection", "value": "1; mode=block" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" }
      ]
    }
  ]
}
```

### Why this configuration matters:
1. **SPA Client-Side Routing:** Prevents `404 Not Found` when directly refreshing routes such as `/showcase`, `/campaigns`, `/technology-stack`, `/dashboard`, or `/analytics`.
2. **Asset Cache Invalidation:** Caches hashed JS/CSS assets for 1 year with `immutable` tags for optimal Lighthouse and Core Web Vitals performance.
3. **Enterprise Security Headers:** Enforces `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, and strict referrer policies.

---

## 🌐 Full-Stack Architecture: Connecting the Backend

To connect the Vercel frontend to a live cloud backend:

```
┌─────────────────────────┐               ┌───────────────────────────┐
│     Vercel Edge CDN     │               │   Backend Cloud Service   │
│  (React 18 + Vite SPA)  │ ────────────> │  (FastAPI + Python 3.12)  │
│  adpilot-pro.vercel.app │  HTTPS / WSS  │   (Render / Railway / AWS)│
└─────────────────────────┘               └───────────────────────────┘
```

### Recommended Free/Low-Cost Backend Hosting Options:
1. **Render.com** (Web Service):
   - Build Command: `pip install uv && uv pip install -e .`
   - Start Command: `uv run uvicorn adpilot.api.main:app --host 0.0.0.0 --port $PORT`
2. **Railway.app** (Docker / Nixpacks):
   - Directly deploys the root `Dockerfile`.
3. **Fly.io** (Global Edge Containers):
   - `fly launch` using the included `Dockerfile` and `docker-compose.yml`.

---

## ✅ Deployment Checklist

- [x] High-resolution transparent logo configured at `frontend/public/logo.png`
- [x] Crisp favicon configured at `frontend/public/favicon.png`
- [x] Production SPA rewrite rules enabled in `vercel.json`
- [x] 52/52 Vitest component and unit tests passing
- [x] Zero TypeScript compilation errors (`tsc && vite build` passes in ~9s)
- [x] Production environment templates configured (`.env.production`, `.env.example`)
- [x] Synchronized with GitHub `main` branch
