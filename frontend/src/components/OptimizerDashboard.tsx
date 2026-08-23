import React from 'react';
import { 
  Zap, 
  TrendingUp, 
  Sliders, 
  Cpu, 
  Layers, 
  ShieldCheck,
  CheckCircle2,
  DollarSign,
  Sparkles,
  ArrowRight
} from 'lucide-react';

export const OptimizerDashboard: React.FC = () => {
  const stateVector = [
    { label: 'LinkedIn Weight', value: '0.45', unit: 'ratio', pct: 45 },
    { label: 'Meta Ads Weight', value: '0.35', unit: 'ratio', pct: 35 },
    { label: 'Google Search Weight', value: '0.20', unit: 'ratio', pct: 20 },
    { label: 'Current Predicted ROAS', value: '3.84x', unit: 'mult', pct: 76 },
    { label: 'Target CAC', value: '$42.10', unit: 'USD', pct: 60 },
    { label: 'Predicted CTR', value: '4.7%', unit: 'pct', pct: 47 },
    { label: 'Predicted CVR', value: '6.2%', unit: 'pct', pct: 62 },
    { label: 'Quality Score Prior', value: '88/100', unit: 'score', pct: 88 },
    { label: 'Total Budget', value: '$10,000', unit: 'USD', pct: 100 },
    { label: 'Campaign Duration', value: '30', unit: 'days', pct: 50 },
    { label: 'Audience Penetration', value: '0.92', unit: 'idx', pct: 92 },
    { label: 'Creative Diversity Index', value: '0.85', unit: 'idx', pct: 85 },
  ];

  return (
    <div className="w-full space-y-6">
      {/* Header Banner */}
      <div className="glass-panel-elevated rounded-2xl p-6 relative overflow-hidden shadow-2xl">
        <div className="absolute -top-10 -right-10 w-80 h-80 bg-amber-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-3">
              <span className="p-2.5 rounded-xl bg-gradient-to-br from-amber-500/25 to-orange-500/25 text-amber-400 border border-amber-500/40 shadow-[0_0_20px_rgba(245,158,11,0.25)]">
                <Zap className="w-6 h-6" />
              </span>
              <div>
                <h2 className="text-xl font-black text-slate-100 flex items-center gap-2">
                  RL Policy Optimizer (PPO Continuous Actor-Critic)
                  <span className="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-amber-500/15 text-amber-300 border border-amber-500/30">
                    PyTorch Core
                  </span>
                </h2>
                <p className="text-xs text-slate-400 mt-0.5 max-w-2xl">
                  Continuous Reinforcement Learning policy sampling 12-dimensional state spaces and emitting safety-bounded budget actions.
                </p>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-4 bg-[#07090e]/90 border border-white/[0.08] rounded-xl px-4 py-2.5 shrink-0 shadow-inner">
            <div>
              <div className="text-[10px] uppercase font-mono text-slate-400">Policy Checkpoint</div>
              <div className="text-xs font-mono font-bold text-amber-300">ppo_policy_v3.pt</div>
            </div>
            <div className="h-6 w-[1px] bg-white/[0.08]" />
            <div>
              <div className="text-[10px] uppercase font-mono text-slate-400">Model Status</div>
              <div className="text-xs font-bold text-emerald-400 flex items-center gap-1 font-mono">
                <CheckCircle2 className="w-3.5 h-3.5" /> PyTorch Active
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 12-Dimensional State Vector Inspection Grid */}
      <div className="glass-panel-elevated rounded-2xl p-5 shadow-2xl">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Sliders className="w-4 h-4 text-cyan-400" />
            <h3 className="text-sm font-bold text-slate-100">Continuous Environment State Vector (12-Dimensional Observation Space)</h3>
          </div>
          <span className="text-[11px] font-mono text-cyan-300 bg-cyan-500/10 px-2.5 py-0.5 rounded-lg border border-cyan-500/30 font-semibold">
            Dim: 12 Cont
          </span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
          {stateVector.map((st, i) => (
            <div key={i} className="bg-[#07090e]/85 border border-white/[0.08] rounded-xl p-3 hover:border-cyan-500/30 transition-colors">
              <div className="text-[10px] font-mono text-slate-400 uppercase truncate font-semibold">
                {String(i + 1).padStart(2, '0')}. {st.label}
              </div>
              <div className="text-sm font-bold text-slate-100 mt-1 font-mono flex items-baseline justify-between">
                <span className="text-cyan-300">{st.value}</span>
                <span className="text-[10px] text-slate-400 font-normal">{st.unit}</span>
              </div>
              <div className="w-full bg-slate-900 rounded-full h-1 overflow-hidden mt-2 border border-white/[0.04]">
                <div className="bg-gradient-to-r from-cyan-500 to-blue-500 h-full rounded-full" style={{ width: `${st.pct}%` }} />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Action Space & Simulated Optimization Trajectory */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left: Recommended PPO Actions */}
        <div className="glass-card-premium p-6 shadow-2xl">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Cpu className="w-4 h-4 text-amber-400" />
              <h3 className="text-sm font-bold text-slate-100">Recommended Action Policy (Actions)</h3>
            </div>
            <span className="text-[10px] font-mono text-amber-300 bg-amber-500/15 px-2.5 py-0.5 rounded-lg border border-amber-500/30 font-bold">
              Reward: +0.48 Expected
            </span>
          </div>

          <div className="space-y-3 text-xs">
            <div className="p-3.5 rounded-xl bg-[#07090e]/85 border border-white/[0.08]">
              <div className="flex justify-between font-bold text-slate-200 mb-1">
                <span>LinkedIn Ads Allocation</span>
                <span className="text-emerald-400 font-mono">+12% ($4,500 → $5,700)</span>
              </div>
              <div className="w-full bg-slate-900 rounded-full h-2 overflow-hidden mt-2 p-0.5 border border-white/[0.05]">
                <div className="bg-gradient-to-r from-emerald-500 to-teal-400 h-full rounded-full" style={{ width: '57%' }} />
              </div>
            </div>

            <div className="p-3.5 rounded-xl bg-[#07090e]/85 border border-white/[0.08]">
              <div className="flex justify-between font-bold text-slate-200 mb-1">
                <span>Meta Ads Allocation</span>
                <span className="text-cyan-400 font-mono">0% Hold ($3,500)</span>
              </div>
              <div className="w-full bg-slate-900 rounded-full h-2 overflow-hidden mt-2 p-0.5 border border-white/[0.05]">
                <div className="bg-gradient-to-r from-cyan-500 to-blue-400 h-full rounded-full" style={{ width: '35%' }} />
              </div>
            </div>

            <div className="p-3.5 rounded-xl bg-[#07090e]/85 border border-white/[0.08]">
              <div className="flex justify-between font-bold text-slate-200 mb-1">
                <span>Google Search Allocation</span>
                <span className="text-rose-400 font-mono">-12% ($2,000 → $800)</span>
              </div>
              <div className="w-full bg-slate-900 rounded-full h-2 overflow-hidden mt-2 p-0.5 border border-white/[0.05]">
                <div className="bg-gradient-to-r from-rose-500 to-pink-500 h-full rounded-full" style={{ width: '8%' }} />
              </div>
            </div>
          </div>
        </div>

        {/* Right: Reward Function & Trajectory Forecast */}
        <div className="glass-card-premium p-6 flex flex-col justify-between shadow-2xl">
          <div>
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-emerald-400" />
                <h3 className="text-sm font-bold text-slate-100">Simulation Trajectory & Reward Function</h3>
              </div>
            </div>

            {/* Formula Block */}
            <div className="p-3.5 rounded-xl bg-[#07090e]/90 border border-white/[0.08] font-mono text-[11px] text-slate-300 mb-4 shadow-inner">
              <div className="text-amber-400 font-bold mb-1">Reward Objective:</div>
              <span className="text-cyan-300 font-bold">R(s, a)</span> = w₁ · ΔROAS - w₂ · ΔCAC - λ · RiskPenalty
            </div>

            {/* Performance Trajectory Milestones */}
            <div className="space-y-2 text-xs font-mono">
              <div className="flex justify-between items-center p-2.5 rounded-lg bg-[#07090e]/80 border border-white/[0.08]">
                <span className="text-slate-400">Baseline (Static Budget):</span>
                <span className="text-slate-300 font-bold">ROAS 3.20x • CAC $49.00</span>
              </div>
              <div className="flex justify-between items-center p-2.5 rounded-lg bg-emerald-500/15 border border-emerald-500/30">
                <span className="text-emerald-300 font-semibold">PPO Optimized Policy:</span>
                <span className="text-emerald-400 font-bold">ROAS 3.84x • CAC $42.10</span>
              </div>
            </div>
          </div>

          <div className="pt-4 mt-4 border-t border-white/[0.08] flex items-center justify-between text-xs text-slate-400 font-mono">
            <span>Constraint Guards: <strong className="text-emerald-400">0 Violations</strong></span>
            <span>Exploration: <strong className="text-cyan-400">ε = 0.05</strong></span>
          </div>
        </div>
      </div>
    </div>
  );
};
