import React from 'react';
import { 
  Clock, 
  CheckCircle2, 
  Bot, 
  Cpu, 
  ShieldCheck, 
  Sparkles, 
  Layers, 
  ArrowRight,
  Database
} from 'lucide-react';

export const CampaignTimelineView: React.FC = () => {
  const events = [
    {
      time: '18:39:13.201',
      stage: 'Stage 01 — User Input Ingestion',
      agent: 'Campaign Context Builder',
      status: 'SUCCESS',
      latency: '2.1ms',
      detail: 'Validated B2B SaaS campaign brief schema (Pydantic-V2). Extracted budget: $10,000, 30-day timeline.'
    },
    {
      time: '18:39:13.245',
      stage: 'Stage 05 — Strategy Planning',
      agent: 'Strategy Agent (GPT-4o Router)',
      status: 'SUCCESS',
      latency: '1,420ms',
      detail: 'Synthesized cross-channel roadmap: LinkedIn (45%), Meta Ads (35%), Google Search (20%).'
    },
    {
      time: '18:39:14.670',
      stage: 'Stage 06 — Audience & Market Research',
      agent: 'Research Agent (FastEmbed BGE)',
      status: 'SUCCESS',
      latency: '820ms',
      detail: 'Hybrid RRF retrieval executed on Qdrant vector store. HitRate: 1.0, MRR: 1.0. Identified 3 core pain points.'
    },
    {
      time: '18:39:15.510',
      stage: 'Stage 07 — Competitor Intelligence',
      agent: 'Competitor Agent',
      status: 'SUCCESS',
      latency: '650ms',
      detail: 'Benchmarked 12 category rivals. Discovered whitespace positioning in mid-market agility.'
    },
    {
      time: '18:39:16.180',
      stage: 'Stage 08 — Content Copywriting',
      agent: 'Content Agent (ML Ridge Scorer)',
      status: 'SUCCESS',
      latency: '1,980ms',
      detail: 'Generated 8 multi-channel ad variants + 4-stage email nurture sequence. Copy quality score: 5.43.'
    },
    {
      time: '18:39:18.190',
      stage: 'Stage 09 — Visual Creative Studio',
      agent: 'Design Agent (Nano Banana Studio)',
      status: 'SUCCESS',
      latency: '2,450ms',
      detail: 'Generated multi-format visual prompts and rendered 4 cross-platform banner assets.'
    },
    {
      time: '18:39:20.660',
      stage: 'Stage 10 — Computer Vision Inspection',
      agent: 'Computer Vision Agent (CLIP-ViT)',
      status: 'SUCCESS',
      latency: '410ms',
      detail: 'Zero-shot CLIP aesthetic scoring passed (8.7/10). Safe zone margin and contrast check: 100% compliant.'
    },
    {
      time: '18:39:21.080',
      stage: 'Stage 11 — Analytics Forecasting',
      agent: 'Analytics Agent (Sklearn Forecaster)',
      status: 'SUCCESS',
      latency: '310ms',
      detail: 'Computed econometric forecast: ROAS 3.84x, CAC $42.10, Composite Health Score: 87.5/100.'
    },
    {
      time: '18:39:21.410',
      stage: 'Stage 12 — Reinforcement Learning Optimizer',
      agent: 'RL Optimizer (PyTorch PPO Policy)',
      status: 'SUCCESS',
      latency: '290ms',
      detail: 'PPO Actor-Critic policy sampled continuous state vector s_t. Emitted budget action (+12% LinkedIn).'
    },
    {
      time: '18:39:21.720',
      stage: 'Stage 14 — Human-in-the-Loop Governance',
      agent: 'HITL Review Manager',
      status: 'APPROVED',
      latency: '50ms',
      detail: 'Campaign Director confirmed strategy and budget allocation. Audit record cryptographically signed.'
    },
    {
      time: '18:39:21.800',
      stage: 'Stage 15 — Publishing Dispatch',
      agent: 'Publishing Agent (Dry-Run Mode)',
      status: 'DISPATCHED',
      latency: '120ms',
      detail: 'Safe dry-run publishing executed across 3 provider adapters (Meta, Google, LinkedIn). Idempotency key verified.'
    }
  ];

  return (
    <div className="w-full space-y-6">
      {/* Header Banner */}
      <div className="glass-panel-elevated rounded-2xl p-6 relative overflow-hidden shadow-2xl">
        <div className="flex items-center gap-3">
          <span className="p-2.5 rounded-xl bg-gradient-to-br from-blue-500/25 to-cyan-500/25 text-cyan-400 border border-cyan-500/40 shadow-[0_0_20px_rgba(6,182,212,0.25)]">
            <Clock className="w-6 h-6" />
          </span>
          <div>
            <h2 className="text-xl font-black text-slate-100 flex items-center gap-2">
              Campaign Execution Event Timeline
              <span className="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-cyan-500/15 text-cyan-300 border border-cyan-500/30">
                Deterministic DAG
              </span>
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Millisecond-accurate audit trail of all deterministic agent invocations, neural inferences, and human gates.
            </p>
          </div>
        </div>
      </div>

      {/* Timeline Stream */}
      <div className="glass-panel-elevated rounded-2xl p-6 shadow-2xl relative">
        <div className="absolute top-10 bottom-10 left-[27px] w-[2px] bg-white/[0.08] pointer-events-none" />

        <div className="space-y-6 relative z-10">
          {events.map((evt, idx) => (
            <div key={idx} className="flex items-start gap-4 text-xs font-mono group">
              {/* Dot Icon */}
              <div className="w-6 h-6 rounded-full bg-[#07090e] border-2 border-cyan-400 flex items-center justify-center text-cyan-400 shrink-0 group-hover:scale-110 transition-transform shadow-[0_0_10px_rgba(6,182,212,0.3)]">
                <CheckCircle2 className="w-3.5 h-3.5" />
              </div>

              {/* Event Content Card */}
              <div className="flex-1 glass-card-premium p-4 group-hover:border-cyan-500/40 transition-colors shadow-lg">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 mb-1.5">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="font-bold text-slate-100">{evt.stage}</span>
                    <span className="text-cyan-400 font-semibold">• {evt.agent}</span>
                  </div>
                  <div className="flex items-center gap-2 text-[11px] text-slate-400">
                    <span>{evt.time}</span>
                    <span>({evt.latency})</span>
                  </div>
                </div>

                <p className="text-slate-300 font-sans text-xs mt-1 leading-relaxed">
                  {evt.detail}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
