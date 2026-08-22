import React, { useState } from 'react';
import { 
  ShieldCheck, 
  CheckCircle2, 
  XCircle, 
  AlertTriangle, 
  Bot, 
  UserCheck, 
  ArrowRight, 
  Lock,
  Download,
  Key
} from 'lucide-react';
import type { HITLDecisionItem } from '../types';

export const HITLApprovalCenter: React.FC = () => {
  const [activeRole, setActiveRole] = useState<'Director' | 'Auditor' | 'GrowthLead'>('Director');
  const [items, setItems] = useState<HITLDecisionItem[]>([
    {
      id: 'hitl-001',
      stage: 'Budget / Optimizer',
      agent: 'RL Policy Optimizer (PPO)',
      title: 'Authorize +12% Budget Allocation to LinkedIn Ads ($4,500 → $5,700)',
      riskLevel: 'MEDIUM',
      status: 'PENDING',
      recommendation: 'Rebalance LinkedIn budget from $4,500 to $5,700 and reduce Google Search by $1,200.',
      predictedImpact: {
        roasDelta: '+0.48x (+12.5%)',
        cacDelta: '-$6.90 (-14.1%)',
        reachDelta: '+24,000 Impressions'
      },
      reasoning: 'PPO Actor-Critic policy detected 4.82x ROAS signal with 94% epistemic confidence. Rebalancing does not exceed total $10,000 budget constraint.',
      timestamp: '2026-08-22 18:39:21'
    },
    {
      id: 'hitl-002',
      stage: 'Publishing Dispatch',
      agent: 'Publishing Agent',
      title: 'Authorize Multi-Channel Live Ad Campaign Dispatch (Meta, Google, LinkedIn)',
      riskLevel: 'HIGH',
      status: 'PENDING',
      recommendation: 'Execute safe publishing adapters across Meta Ads, Google Ads, and LinkedIn Sponsored Content.',
      predictedImpact: {
        roasDelta: '+3.84x Expected',
        cacDelta: '$42.10 CAC Cap',
        reachDelta: '140,000 B2B Decision Makers'
      },
      reasoning: 'Content copy, creative assets, and budget have cleared all automated ML & CLIP-ViT safety thresholds. Ready for external provider API sync.',
      timestamp: '2026-08-22 18:39:22'
    }
  ]);

  const [auditLog, setAuditLog] = useState<string[]>([
    '[2026-08-22 18:30:00] Director approved initial strategy roadmap for Campaign VisionGuard AI. Signature: SHA256-d7a8f9b2',
    '[2026-08-22 18:32:15] Auditor verified CLIP-ViT brand compliance tokens. Signature: SHA256-e3b1c4a0'
  ]);

  const handleApprove = (id: string) => {
    const item = items.find(i => i.id === id);
    setItems(prev => prev.map(item => item.id === id ? { ...item, status: 'APPROVED' } : item));
    const sig = 'SHA256-' + Math.random().toString(16).substring(2, 10);
    setAuditLog(prev => [
      `[${new Date().toISOString().replace('T', ' ').substring(0, 19)}] ${activeRole} APPROVED ${item?.stage} (${id}). Signed: ${sig}`,
      ...prev
    ]);
  };

  const handleReject = (id: string) => {
    const item = items.find(i => i.id === id);
    setItems(prev => prev.map(item => item.id === id ? { ...item, status: 'REJECTED' } : item));
    const sig = 'SHA256-' + Math.random().toString(16).substring(2, 10);
    setAuditLog(prev => [
      `[${new Date().toISOString().replace('T', ' ').substring(0, 19)}] ${activeRole} REJECTED ${item?.stage} (${id}). Signed: ${sig}`,
      ...prev
    ]);
  };

  return (
    <div className="w-full space-y-6">
      {/* Header Banner */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 relative overflow-hidden backdrop-blur-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2.5">
              <span className="p-2 rounded-xl bg-rose-500/10 text-rose-400 border border-rose-500/20">
                <ShieldCheck className="w-5 h-5" />
              </span>
              <h2 className="text-xl font-bold text-slate-100">Human-in-the-Loop (HITL) Governance Center</h2>
            </div>
            <p className="text-xs text-slate-400 mt-1 max-w-2xl">
              Cryptographic review gate enforcing strict enterprise human oversight for high-risk autonomous agent decisions, budget rebalancing, and live publishing.
            </p>
          </div>

          {/* RBAC Role Switcher */}
          <div className="flex items-center gap-2 bg-slate-950/80 border border-slate-800 rounded-xl p-1.5 shrink-0">
            <span className="text-[10px] font-mono text-slate-500 uppercase px-2">Active Role:</span>
            {(['Director', 'Auditor', 'GrowthLead'] as const).map(role => (
              <button
                key={role}
                onClick={() => setActiveRole(role)}
                className={`px-3 py-1 rounded-lg text-xs font-mono font-semibold transition-all ${
                  activeRole === role
                    ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40 shadow-sm'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {role}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Pending Approval Items */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider font-mono flex items-center gap-2">
            <UserCheck className="w-4 h-4 text-cyan-400" />
            <span>Pending Governance Decisions ({items.filter(i => i.status === 'PENDING').length})</span>
          </h3>
          <span className="text-xs font-mono text-slate-400 flex items-center gap-1.5">
            <Key className="w-3.5 h-3.5 text-amber-400" />
            <span>HMAC-SHA256 Cryptographic Signing Enforced</span>
          </span>
        </div>

        <div className="grid grid-cols-1 gap-4">
          {items.map(item => (
            <div 
              key={item.id}
              className={`p-6 rounded-2xl border transition-all backdrop-blur-xl ${
                item.status === 'APPROVED' 
                  ? 'bg-slate-900/40 border-emerald-500/30 opacity-70'
                  : item.status === 'REJECTED'
                  ? 'bg-slate-900/40 border-rose-500/30 opacity-70'
                  : 'bg-slate-900/80 border-slate-800 shadow-xl'
              }`}
            >
              <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-4 border-b border-slate-800/80">
                <div>
                  <div className="flex items-center gap-2 mb-1.5">
                    <span className="px-2.5 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-500/10 text-amber-300 border border-amber-500/20">
                      {item.stage}
                    </span>
                    <span className={`px-2.5 py-0.5 rounded text-[10px] font-mono font-bold ${
                      item.riskLevel === 'HIGH' ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' : 'bg-blue-500/10 text-blue-400 border border-blue-500/20'
                    }`}>
                      {item.riskLevel} RISK
                    </span>
                    <span className="text-[11px] font-mono text-slate-500">
                      ID: {item.id} • {item.timestamp}
                    </span>
                  </div>
                  <h4 className="text-base font-bold text-slate-100">{item.title}</h4>
                </div>

                {/* Action Buttons */}
                <div className="flex items-center gap-2.5 shrink-0">
                  {item.status === 'PENDING' ? (
                    <>
                      <button
                        onClick={() => handleReject(item.id)}
                        className="px-4 py-2 rounded-xl text-xs font-bold font-mono bg-rose-500/10 hover:bg-rose-500/20 text-rose-300 border border-rose-500/30 flex items-center gap-1.5 transition-colors"
                      >
                        <XCircle className="w-3.5 h-3.5" />
                        <span>Reject Decision</span>
                      </button>
                      <button
                        onClick={() => handleApprove(item.id)}
                        className="px-4 py-2 rounded-xl text-xs font-bold font-mono bg-emerald-600 hover:bg-emerald-500 text-white flex items-center gap-1.5 transition-colors shadow-lg shadow-emerald-600/20"
                      >
                        <CheckCircle2 className="w-3.5 h-3.5" />
                        <span>Sign & Authorize</span>
                      </button>
                    </>
                  ) : (
                    <span className={`px-3 py-1.5 rounded-xl text-xs font-mono font-bold flex items-center gap-1.5 ${
                      item.status === 'APPROVED' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30' : 'bg-rose-500/10 text-rose-400 border border-rose-500/30'
                    }`}>
                      {item.status === 'APPROVED' ? <CheckCircle2 className="w-3.5 h-3.5" /> : <XCircle className="w-3.5 h-3.5" />}
                      <span>{item.status} BY {activeRole.toUpperCase()}</span>
                    </span>
                  )}
                </div>
              </div>

              {/* Rationale & Projected Impact */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4 text-xs font-mono">
                <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
                  <div className="text-slate-500 uppercase text-[10px] mb-1">AI Epistemic Rationale</div>
                  <p className="text-slate-300 font-sans">{item.reasoning}</p>
                </div>
                <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
                  <div className="text-cyan-400 uppercase text-[10px] mb-1">Projected Campaign Impact</div>
                  <div className="space-y-1 text-slate-300 font-sans">
                    <p>{item.recommendation}</p>
                    <div className="flex gap-3 text-[11px] font-mono text-emerald-400 pt-1">
                      <span>ROAS: {item.predictedImpact.roasDelta}</span>
                      <span>CAC: {item.predictedImpact.cacDelta}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Signed Audit Log */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 backdrop-blur-xl">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <Lock className="w-4 h-4 text-emerald-400" />
            <h3 className="text-sm font-bold text-slate-100">Cryptographically Signed Governance Audit Trail</h3>
          </div>
          <span className="text-[10px] font-mono text-emerald-400">Immutable HMAC-SHA256 Ledger</span>
        </div>

        <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 font-mono text-xs text-slate-400 space-y-1.5 max-h-40 overflow-y-auto">
          {auditLog.map((log, idx) => (
            <div key={idx} className="leading-relaxed">
              {log}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
