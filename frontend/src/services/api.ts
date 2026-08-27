import axios from 'axios';
import type { CampaignBrief, TaskResponse, ContentOutput, DesignAssetsResponse } from '../types';

/**
 * Robust API Base URL resolution supporting VITE_API_URL, VITE_API_BASE_URL,
 * NEXT_PUBLIC_API_URL, and intelligent environment defaults.
 */
export function resolveApiBaseUrl(): string {
  // Check local storage runtime override if user configured it in Settings
  if (typeof window !== 'undefined') {
    const savedBackend = localStorage.getItem('adpilot_backend_url');
    if (savedBackend && savedBackend.trim() !== '') {
      let clean = savedBackend.trim().replace(/\/+$/, '');
      if (!clean.endsWith('/api') && !clean.endsWith('/api/v1')) {
        clean = `${clean}/api`;
      }
      return clean;
    }
  }

  const envUrl = 
    (import.meta.env?.VITE_API_URL as string) || 
    (import.meta.env?.VITE_API_BASE_URL as string) ||
    (import.meta.env?.NEXT_PUBLIC_API_URL as string);

  if (envUrl && envUrl.trim() !== '') {
    let clean = envUrl.trim().replace(/\/+$/, '');
    // If the base domain was passed without /api, append /api
    if (!clean.endsWith('/api') && !clean.endsWith('/api/v1')) {
      clean = `${clean}/api`;
    }
    return clean;
  }

  // Test runner environment (MSW mock server)
  if (import.meta.env.MODE === 'test') {
    return 'http://127.0.0.1:8000/api';
  }

  // Local development fallback
  if (!import.meta.env.PROD) {
    return 'http://127.0.0.1:8001/api';
  }

  // Production fallback — points directly to the live Render FastAPI backend
  return 'https://adpilot-pro.onrender.com/api';
}

export const API_BASE = resolveApiBaseUrl();

export const apiClient = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
  withCredentials: false,
});

// Attach JWT token from localStorage if present
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('adpilot_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Surface error messages — FastAPI 422 returns detail as an array of objects
apiClient.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.code === 'ERR_NETWORK' || err.message?.includes('Network Error')) {
      return Promise.reject(
        new Error('Unable to connect to the backend server. Please verify your Render/FastAPI backend deployment or configure VITE_API_URL on Vercel.')
      );
    }
    const detail = err?.response?.data?.detail;
    let message: string;
    if (Array.isArray(detail)) {
      // Pydantic validation errors: [{loc, msg, type}, ...]
      message = detail
        .map((d: { loc?: string[]; msg?: string }) =>
          d.loc ? `${d.loc.slice(1).join(' → ')}: ${d.msg}` : (d.msg ?? 'Validation error')
        )
        .join(' | ');
    } else if (typeof detail === 'string') {
      message = detail;
    } else {
      message = err?.message ?? 'Unknown error';
    }
    return Promise.reject(new Error(message));
  }
);

// ─── Campaign & Content Service ─────────────────────────────────────────────

export const campaignService = {
  /** Submit a new campaign brief — calls the full multi-agent DAG pipeline. */
  async submitCampaign(brief: CampaignBrief): Promise<TaskResponse> {
    const response = await apiClient.post('/campaigns', brief);
    return response.data;
  },

  /** Poll campaign task status. */
  async getTaskStatus(taskId: string): Promise<TaskResponse> {
    const response = await apiClient.get(`/tasks/${taskId}`);
    return response.data;
  },

  /** Retrieve full campaign content results. */
  async getCampaignContent(campaignId: string): Promise<ContentOutput> {
    const response = await apiClient.get(`/campaigns/${campaignId}/content`);
    return response.data;
  },

  /** Download a ZIP of all design assets for a campaign. */
  async downloadDesignAssets(campaignId: string): Promise<Blob> {
    const response = await apiClient.get(
      `/campaigns/${campaignId}/design-assets/download`,
      { responseType: 'blob' }
    );
    return response.data;
  },

  /** Fetch design asset metadata for a campaign. */
  async getDesignAssets(campaignId: string): Promise<DesignAssetsResponse> {
    const response = await apiClient.get(`/campaigns/${campaignId}/design-assets`);
    return response.data;
  },

  /** Download a single design asset file by ID. */
  async downloadSingleAsset(assetId: number, _filename?: string): Promise<Blob> {
    void _filename;
    const response = await apiClient.get(`/design-assets/${assetId}/download`, {
      responseType: 'blob',
    });
    return response.data;
  },

  /** Generate creative assets via Nano Banana / Creative Studio API. */
  async generateCreative(payload: {
    product_name: string;
    product_type: string;
    campaign_goal: string;
    target_audience: string;
    visual_style: string;
    custom_prompt: string;
    brand_colors: string[];
  }): Promise<any> {
    const response = await apiClient.post('/creative/generate', payload);
    return response.data;
  },
};

// ─── Simulation Service ─────────────────────────────────────────────────────

export const simulationService = {
  /** Initialize an enterprise pipeline simulation. */
  async createSimulation(payload: {
    product_name: string;
    product_type: string;
    campaign_objective: string;
    target_audience: string;
    budget: number;
    duration_days: number;
    platforms: string[];
    target_cac: number;
    target_roas: number;
  }): Promise<{ simulation_id: string; status: string }> {
    const response = await apiClient.post('/v1/simulations', payload);
    return response.data;
  },

  /** Trigger execution of a created simulation. */
  async runSimulation(simId: string): Promise<any> {
    const response = await apiClient.post(`/v1/simulations/${simId}/run`);
    return response.data;
  },

  /** Poll state of a simulation run. */
  async getSimulation(simId: string): Promise<any> {
    const response = await apiClient.get(`/v1/simulations/${simId}`);
    return response.data;
  },

  /** Approve simulation at Human-in-the-Loop governance gate. */
  async approveSimulation(simId: string): Promise<any> {
    const response = await apiClient.post(`/v1/simulations/${simId}/approve`);
    return response.data;
  },
};

// ─── System Health Service ──────────────────────────────────────────────────

export const systemService = {
  /** Liveness / health probe. */
  async getHealth(): Promise<{ status: string; version: string }> {
    // Attempt root /health (or /healthz) relative to API host
    const origin = API_BASE.replace(/\/api\/?$/, '');
    const response = await axios.get(`${origin}/health`, { timeout: 5000 });
    return response.data;
  },
};

export default apiClient;
