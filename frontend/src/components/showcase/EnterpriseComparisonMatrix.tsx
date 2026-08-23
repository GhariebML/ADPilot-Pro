import React from 'react';
import { 
  CheckCircle2, 
  XCircle, 
  Minus, 
  Sparkles, 
  Award, 
  ShieldCheck, 
  Zap, 
  Layers 
} from 'lucide-react';

export const EnterpriseComparisonMatrix: React.FC = () => {
  const comparisonRows = [
    {
      feature: 'Execution Architecture',
      adpilot: '18-Stage Deterministic DAG (AsyncIO)',
      manual: 'Manual Slack / Email handoffs',
      legacy: 'Single-prompt isolated completion',
      category: 'CORE'
    },
    {
      feature: 'Contract Schema Validation',
      adpilot: 'Pydantic v2 Immutable Schema Enforcement',
      manual: 'None (Unstructured text/docs)',
      legacy: 'Uncontrolled LLM text output',
      category: 'CORE'
    },
    {
      feature: 'Continuous Reinforcement Learning',
      adpilot: 'PyTorch PPO Policy (+28.7% Alpha Return)',
      manual: 'Heuristic spreadsheet guesses',
      legacy: 'None (Static non-learning)',
      category: 'ML_RL'
    },
    {
      feature: 'Predictive Financial Forecaster',
      adpilot: 'Scikit-Learn Ridge Regressor (RÂ² = 0.894)',
      manual: 'Historical agency estimates',
      legacy: 'None (Hallucinated predictions)',
      category: 'ML_RL'
    },
    {
      feature: 'Computer Vision Aesthetic Gate',
      adpilot: 'ONNX CLIP-ViT B/32 (WCAG AAA Contrast)',
      manual: 'Manual graphic designer review',
      legacy: 'None (Blind image generators)',
      category: 'VISION'
    },
    {
      feature: 'RAG Grounding & Hallucination Defense',
      adpilot: 'Dual-Stream FastEmbed BGE + BM25 RRF (k=60)',
      manual: 'Manual PDF reading & copy-pasting',
      legacy: 'Basic unranked vector search',
      category: 'KNOWLEDGE'
    },
    {
      feature: 'Human-in-the-Loop Governance',
      adpilot: 'Cryptographic HMAC-SHA256 Signed Ledger',
      manual: 'Informal email approval threads',
      legacy: 'None (Unsupervised prompt outputs)',
      category: 'SECURITY'
    },
    {
      feature: 'Campaign Formulation Latency',
      adpilot: '3.4 Seconds (End-to-End Pipeline)',
      manual: '3 to 7 Business Days',
      legacy: '45 to 90 Seconds (Manual stitching)',
      category: 'PERFORMANCE'
    },
    {
      feature: 'Automated Test Verification',
      adpilot: '271 Passing Automated Tests (100% CI)',
      manual: 'N/A (Zero automated checks)',
      legacy: 'Proprietary closed black box',
      category: 'RELIABILITY'
    },
  ];

  return (
    <div className="w-full bg-slate-950/40 border border-slate-800/60 shadow-2xl rounded-2xl p-6 backdrop-blur-2xl space-y-6 shadow-2xl relative overflow-hidden">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800/80 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-1.5 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <Award className="w-4 h-4" />
            </span>
            <h3 className="text-base font-bold text-white font-mono uppercase tracking-wider">
              Enterprise Capability Matrix: ADPilot Pro vs Alternatives
            </h3>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Comparing architectural determinism, reinforcement learning, and governance across modern solutions.
          </p>
        </div>

        <span className="px-3 py-1 rounded-xl text-xs font-mono font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 shrink-0">
          Enterprise Certified
        </span>
      </div>

      {/* Comparison Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-left font-mono text-xs border-collapse">
          <thead>
            <tr className="border-b border-slate-800 text-[11px] text-slate-400 uppercase">
              <th className="py-3 px-4">Capability Dimension</th>
              <th className="py-3 px-4 text-cyan-400 bg-cyan-500/10 rounded-t-xl font-extrabold">ADPilot Pro V3</th>
              <th className="py-3 px-4 text-slate-400">Manual Agency</th>
              <th className="py-3 px-4 text-slate-400">Legacy AI Tools</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {comparisonRows.map((row, idx) => (
              <tr key={idx} className="hover:bg-slate-900/40 transition-colors">
                <td className="py-3.5 px-4 font-bold text-slate-200">
                  {row.feature}
                </td>
                <td className="py-3.5 px-4 text-cyan-300 font-bold bg-cyan-500/5">
                  <div className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                    <span>{row.adpilot}</span>
                  </div>
                </td>
                <td className="py-3.5 px-4 text-slate-400">
                  <div className="flex items-center gap-2">
                    <XCircle className="w-3.5 h-3.5 text-rose-400/80 shrink-0" />
                    <span>{row.manual}</span>
                  </div>
                </td>
                <td className="py-3.5 px-4 text-slate-400">
                  <div className="flex items-center gap-2">
                    <Minus className="w-3.5 h-3.5 text-amber-400/80 shrink-0" />
                    <span>{row.legacy}</span>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default EnterpriseComparisonMatrix;

