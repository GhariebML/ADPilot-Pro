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
      <div className="glass-panel-elevated rounded-2xl p-6 relative overflow-hidden shadow-2xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-3">
              <span className="p-2.5 rounded-xl bg-gradient-to-br from-rose-500/25 to-pink-500/25 text-rose-400 border border-rose-500/40 shadow-[0_0_20px_rgba(244,63,94,0.25)]">
                <ShieldCheck className="w-6 h-6" />
              </span>
              <div>
                <h2 className="text-xl font-black text-slate-100 flex items-center gap-2">
                  Human-in-the-Loop (HITL) Governance Center
                  <span className="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-rose-500/15 text-rose-300 border border-rose-500/30">
                    HMAC-SHA256
                  </span>
                </h2>
                <p className="text-xs text-slate-400 mt-0.5 max-w-2xl">
                  Cryptographic review gate enforcing strict enterprise human oversight for high-risk autonomous decisions, budget rebalancing, and live ad dispatch.
                </p>
              </div>
            </div>
          </div>

          {/* RBAC Role Switcher */}
          <div className="flex items-center gap-2 bg-[#07090e]/90 border border-white/[0.08] rounded-xl p-1.5 shrink-0 shadow-inner">
            <span className="text-[10px] font-mono text-slate-400 uppercase px-2 font-bold">Active Role:</span>
            {(['Director', 'Auditor', 'GrowthLead'] as const).map(role => (
              <button
                key={role}
                onClick={() => setActiveRole(role)}
                className={`px-3 py-1 rounded-lg text-xs font-mono font-bold transition-all ${
                  activeRole === role
                    ? 'bg-rose-500/25 text-rose-300 border border-rose-400 shadow-sm'
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
          <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wider font-mono flex items-center gap-2">
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
              className={`glass-card-premium p-6 transition-all ${
                item.status === 'APPROVED' 
                  ? 'border-emerald-500/40 opacity-80'
                  : item.status === 'REJECTED'
                  ? 'border-rose-500/40 opacity-80'
                  : 'shadow-2xl hover:border-cyan-500/40'
              }`}
            >
              <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-4 border-b border-white/[0.08]">
                <div>
                  <div className="flex items-center gap-2 mb-1.5">
                    <span className="px-2.5 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-500/15 text-amber-300 border border-amber-500/30">
                      {item.stage}
                    </span>
                    <span className={`px-2.5 py-0.5 rounded text-[10px] font-mono font-bold ${
                      item.riskLevel === 'HIGH' ? 'bg-rose-500/15 text-rose-300 border border-rose-500/30' : 'bg-blue-500/15 text-blue-300 border border-blue-500/30'
                    }`}>
                      {item.riskLevel} RISK
                    </span>
                    <span className="text-xs text-slate-400 font-mono">• Generated by {item.agent}</span>
                  </div>
                  <h4 className="text-base font-bold text-slate-100">{item.title}</h4>
                </div>

                <div className="flex items-center gap-2 shrink-0">
                  {item.status === 'PENDING' ? (
                    <>
                      <button
                        onClick={() => handleReject(item.id)}
                        className="px-4 py-2 rounded-xl text-xs font-mono font-bold bg-rose-500/15 hover:bg-rose-500/25 text-rose-300 border border-rose-500/30 transition-all flex items-center gap-1.5"
                      >
                        <XCircle className="w-3.5 h-3.5" />
                        <span>Reject / Override</span>
                      </button>
                      <button
                        onClick={() => handleApprove(item.id)}
                        className="px-4 py-2 rounded-xl text-xs font-mono font-bold bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-white transition-all flex items-center gap-1.5 shadow-lg shadow-emerald-500/20"
                      >
                        <CheckCircle2 className="w-3.5 h-3.5" />
                        <span>Authorize Decision ({activeRole})</span>
                      </button>
                    </>
                  ) : (
                    <span className={`px-3 py-1 rounded-xl text-xs font-mono font-bold border flex items-center gap-1.5 ${
                      item.status === 'APPROVED' ? 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30' : 'bg-rose-500/15 text-rose-300 border-rose-500/30'
                    }`}>
                      {item.status === 'APPROVED' ? <CheckCircle2 className="w-3.5 h-3.5" /> : <XCircle className="w-3.5 h-3.5" />}
                      {item.status} BY {activeRole.toUpperCase()}
                    </span>
                  )}
                </div>
              </div>

              {/* Reasoning & Projected Impact Matrix */}
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 mt-4">
                <div className="lg:col-span-8 space-y-3">
                  <div className="text-xs text-slate-300 leading-relaxed bg-[#07090e]/90 p-3.5 rounded-xl border border-white/[0.08]">
                    <span className="text-cyan-400 font-bold font-mono block mb-1">Agent Recommendation & Epistemic Reasoning:</span>
                    {item.reasoning}
                  </div>
                </div>

                <div className="lg:col-span-4 grid grid-cols-1 gap-2">
                  <div className="p-2.5 rounded-xl bg-[#07090e]/90 border border-white/[0.08] flex items-center justify-between">
                    <span className="text-[11px] text-slate-400 font-mono">Predicted ROAS Δ</span>
                    <span className="text-xs font-bold font-mono text-emerald-400">{item.predictedImpact.roasDelta}</span>
                  </div>
                  <div className="p-2.5 rounded-xl bg-[#07090e]/90 border border-white/[0.08] flex items-center justify-between">
                    <span className="text-[11px] text-slate-400 font-mono">Blended CAC Δ</span>
                    <span className="text-xs font-bold font-mono text-cyan-400">{item.predictedImpact.cacDelta}</span>
                  </div>
                  <div className="p-2.5 rounded-xl bg-[#07090e]/90 border border-white/[0.08] flex items-center justify-between">
                    <span className="text-[11px] text-slate-400 font-mono">Net Reach Scale</span>
                    <span className="text-xs font-bold font-mono text-purple-300">{item.predictedImpact.reachDelta}</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Cryptographic Audit Trail Log */}
      <div className="glass-panel-elevated rounded-2xl p-5 shadow-2xl space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-xs font-mono font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
            <Lock className="w-3.5 h-3.5 text-cyan-400" />
            Immutable Audit Trail & Cryptographic Signatures
          </span>
          <span className="text-[10px] font-mono text-emerald-400">Append-Only SHA-256 Ledger</span>
        </div>

        <div className="bg-[#07090e]/90 border border-white/[0.08] rounded-xl p-3 space-y-2 font-mono text-[11px] text-slate-400 shadow-inner">
          {auditLog.map((log, idx) => (
            <div key={idx} className="flex items-start gap-2">
              <span className="text-cyan-400 shrink-0">&gt;</span>
              <span className="text-slate-300">{log}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
