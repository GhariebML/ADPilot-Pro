import React, { useState, useEffect } from 'react';
import { resolveApiBaseUrl, systemService } from '../services/api';
import { Server, CheckCircle2, AlertCircle, RefreshCw, Save } from 'lucide-react';

export const SettingsForm: React.FC = () => {
  const [backendUrl, setBackendUrl] = useState(resolveApiBaseUrl());
  const [testStatus, setTestStatus] = useState<'idle' | 'testing' | 'success' | 'error'>('idle');
  const [testMessage, setTestMessage] = useState('');
  const [openaiKey, setOpenaiKey] = useState('');
  const [cloudinaryKey, setCloudinaryKey] = useState('');

  useEffect(() => {
    const saved = localStorage.getItem('adpilot_backend_url');
    if (saved) setBackendUrl(saved);
    const key = localStorage.getItem('OPENAI_API_KEY') || '';
    setOpenaiKey(key);
    const cKey = localStorage.getItem('CLOUDINARY_API_KEY') || '';
    setCloudinaryKey(cKey);
  }, []);

  const handleTestConnection = async () => {
    setTestStatus('testing');
    try {
      let url = backendUrl.trim().replace(/\/+$/, '');
      if (!url.endsWith('/api') && !url.endsWith('/api/v1')) {
        url = `${url}/api`;
      }
      const origin = url.replace(/\/api\/?$/, '');
      const res = await fetch(`${origin}/health`, { method: 'GET', headers: { 'Accept': 'application/json' } });
      if (res.ok) {
        const data = await res.json();
        setTestStatus('success');
        setTestMessage(`Connected to ADPilot Backend (${data.status || 'OK'}, v${data.version || '3.0.0'})`);
      } else {
        setTestStatus('error');
        setTestMessage(`HTTP ${res.status}: Backend responded with error`);
      }
    } catch (err: any) {
      setTestStatus('error');
      setTestMessage(err?.message || 'Failed to reach backend');
    }
  };

  const handleSave = () => {
    localStorage.setItem('adpilot_backend_url', backendUrl.trim());
    localStorage.setItem('OPENAI_API_KEY', openaiKey);
    localStorage.setItem('CLOUDINARY_API_KEY', cloudinaryKey);
    alert('Settings saved. Reloading page to apply changes...');
    window.location.reload();
  };

  const handleResetDefault = () => {
    localStorage.removeItem('adpilot_backend_url');
    setBackendUrl('https://adpilot-pro.onrender.com/api');
  };

  return (
    <div className="p-6 bg-slate-900/90 border border-slate-800 rounded-2xl max-w-2xl space-y-6">
      {/* Backend API Settings */}
      <div className="space-y-3 pb-6 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <Server className="w-5 h-5 text-cyan-400" />
          <h3 className="font-bold text-base text-white">FastAPI Backend API Connection</h3>
        </div>
        <p className="text-xs text-slate-400">
          The endpoint of your production Render or local FastAPI backend server.
        </p>

        <div className="space-y-2">
          <label className="text-xs font-mono text-slate-300">Backend API URL</label>
          <div className="flex gap-2">
            <input
              type="text"
              value={backendUrl}
              onChange={(e) => setBackendUrl(e.target.value)}
              placeholder="https://adpilot-pro.onrender.com/api"
              className="flex-1 p-2.5 rounded-xl bg-slate-950 border border-slate-800 font-mono text-xs text-cyan-300 focus:border-cyan-500 focus:outline-none"
            />
            <button
              onClick={handleTestConnection}
              disabled={testStatus === 'testing'}
              className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold rounded-xl flex items-center gap-1.5 transition-all"
            >
              {testStatus === 'testing' ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <RefreshCw className="w-3.5 h-3.5" />}
              <span>Test</span>
            </button>
          </div>

          {testStatus === 'success' && (
            <div className="flex items-center gap-2 text-xs text-emerald-400 p-2.5 rounded-lg bg-emerald-500/10 border border-emerald-500/30">
              <CheckCircle2 className="w-4 h-4 shrink-0" />
              <span>{testMessage}</span>
            </div>
          )}

          {testStatus === 'error' && (
            <div className="flex items-center gap-2 text-xs text-rose-400 p-2.5 rounded-lg bg-rose-500/10 border border-rose-500/30">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{testMessage}</span>
            </div>
          )}

          <div className="flex items-center justify-between pt-1 text-[11px] text-slate-500">
            <span>Default: <code className="text-slate-400 font-mono">https://adpilot-pro.onrender.com/api</code></span>
            <button onClick={handleResetDefault} className="text-cyan-400 hover:underline">
              Reset to Default
            </button>
          </div>
        </div>
      </div>

      {/* Model & Storage Integrations */}
      <div className="space-y-4">
        <h3 className="font-bold text-base text-white">Client Integrations</h3>
        <div>
          <label className="text-xs text-slate-400 block mb-1">OpenAI API Key (Optional Client Override)</label>
          <input
            type="password"
            value={openaiKey}
            onChange={(e) => setOpenaiKey(e.target.value)}
            placeholder="sk-..."
            className="w-full p-2.5 rounded-xl bg-slate-950 border border-slate-800 font-mono text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
          />
        </div>
        <div>
          <label className="text-xs text-slate-400 block mb-1">Cloudinary API Key (Optional)</label>
          <input
            type="password"
            value={cloudinaryKey}
            onChange={(e) => setCloudinaryKey(e.target.value)}
            placeholder="Optional Cloudinary Key"
            className="w-full p-2.5 rounded-xl bg-slate-950 border border-slate-800 font-mono text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
          />
        </div>
      </div>

      {/* Action Buttons */}
      <div className="pt-4 border-t border-slate-800 flex items-center justify-end gap-3">
        <button
          onClick={handleSave}
          className="px-5 py-2.5 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white text-xs font-bold rounded-xl flex items-center gap-2 shadow-lg shadow-cyan-500/20 active:scale-95 transition-all"
        >
          <Save className="w-4 h-4" />
          <span>Save Configuration</span>
        </button>
      </div>
    </div>
  );
};

export default SettingsForm;
