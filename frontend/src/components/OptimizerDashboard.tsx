import React from 'react';
import { 
  Zap, 
  TrendingUp, 
  Sliders, 
  Cpu, 
  Layers, 
  Activity, 
  ArrowUpRight, 
  Sparkles, 
  ShieldCheck,
  CheckCircle2,
  DollarSign
} from 'lucide-react';

export const OptimizerDashboard: React.FC = () => {
  const stateVector = [
    { label: 'LinkedIn Weight', value: '0.45', unit: 'ratio' },
    { label: 'Meta Ads Weight', value: '0.35', unit: 'ratio' },
    { label: 'Google Search Weight', value: '0.20', unit: 'ratio' },
    { label: 'Current Predicted ROAS', value: '3.84x', unit: 'mult' },
    { label: 'Target CAC', value: '$42.10', unit: 'USD' },
    { label: 'Predicted CTR', value: '4.7%', unit: 'pct' },
    { label: 'Predicted CVR', value: '6.2%', unit: 'pct' },
    { label: 'Quality Score Prior', value: '88/100', unit: 'score' },
    { label: 'Total Budget', value: '$10,000', unit: 'USD' },
    { label: 'Campaign Duration', value: '30', unit: 'days' },
    { label: 'Audience Penetration', value: '0.92', unit: 'idx' },
    { label: 'Creative Diversity Index', value: '0.85', unit: 'idx' },
  ];

  return (
    <div className="w-full space-y-6">
      {/* Header Banner */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 relative overflow-hidden backdrop-blur-3xl">
        <div className="absolute -top-10 -right-10 w-80 h-80 bg-amber-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2.5">
              <span className="p-2 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/20">
                <Zap className="w-5 h-5" />
              </span>
              <h2 className="text-xl font-bold text-slate-100">RL Policy Optimizer (PPO Continuous Actor-Critic)</h2>
            </div>
            <p className="text-xs text-slate-400 mt-1 max-w-2xl">
              Autonomous Reinforcement Learning agent continuously sampling high-dimensional state vectors (12-dim continuous state space) and emitting optimal channel budget actions bounded by strict constraint guards.
            </p>
          </div>

          <div className="flex items-center gap-3 bg-slate-950/40 border border-slate-800/60 shadow-2xl rounded-xl px-4 py-2.5 shrink-0">
            <div>
              <div className="text-[10px] uppercase font-mono text-slate-500">Policy Checkpoint</div>
              <div className="text-xs font-mono font-bold text-amber-300">ppo_policy.pt</div>
            </div>
            <div className="h-6 w-[1px] bg-slate-800" />
            <div>
              <div className="text-[10px] uppercase font-mono text-slate-500">Model Status</div>
              <div className="text-xs font-bold text-emerald-400 flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5" /> PyTorch Active
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 12-Dimensional State Vector Inspection Grid */}
      <div className="bg-slate-950/40 border border-slate-800/60 shadow-2xl rounded-2xl p-5 backdrop-blur-3xl">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Sliders className="w-4 h-4 text-cyan-400" />
            <h3 className="text-sm font-bold text-slate-200">Continuous Environment State Vector (12-Dimensional State)</h3>
          </div>
          <span className="text-[11px] font-mono text-slate-400 bg-slate-950 px-2 py-0.5 rounded border border-slate-800">
            Observation Space Dimension: 12
          </span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
          {stateVector.map((st, i) => (
            <div key={i} className="bg-slate-950/70 border border-slate-800/80 rounded-xl p-3">
              <div className="text-[10px] font-mono text-slate-500 uppercase truncate">
                {String(i + 1).padStart(2, '0')}. {st.label}
              </div>
              <div className="text-sm font-bold text-slate-100 mt-1 font-mono flex items-baseline justify-between">
                <span>{st.value}</span>
                <span className="text-[10px] text-slate-500 font-normal">{st.unit}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Action Space & Simulated Optimization Trajectory */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left: Recommended PPO Actions */}
        <div className="bg-slate-950/40 border border-slate-800/60 shadow-2xl rounded-2xl p-5 backdrop-blur-3xl">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Cpu className="w-4 h-4 text-amber-400" />
              <h3 className="text-sm font-bold text-slate-200">Recommended Action Policy (Actions)</h3>
            </div>
            <span className="text-[10px] font-mono text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20">
              Reward: +0.48 Expected
            </span>
          </div>

          <div className="space-y-3 text-xs">
            <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
              <div className="flex justify-between font-bold text-slate-200 mb-1">
                <span>LinkedIn Ads Allocation</span>
                <span className="text-emerald-400 font-mono">+12% ($4,500 â†’ $5,700)</span>
              </div>
              <div className="w-full bg-slate-900 rounded-full h-1.5 overflow-hidden mt-2">
                <div className="bg-emerald-500 h-full" style={{ width: '57%' }} />
              </div>
            </div>

            <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
              <div className="flex justify-between font-bold text-slate-200 mb-1">
                <span>Meta Ads Allocation</span>
                <span className="text-cyan-400 font-mono">0% Hold ($3,500)</span>
              </div>
              <div className="w-full bg-slate-900 rounded-full h-1.5 overflow-hidden mt-2">
                <div className="bg-cyan-500 h-full" style={{ width: '35%' }} />
              </div>
            </div>

            <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
              <div className="flex justify-between font-bold text-slate-200 mb-1">
                <span>Google Search Allocation</span>
                <span className="text-rose-400 font-mono">-12% ($2,000 â†’ $800)</span>
              </div>
              <div className="w-full bg-slate-900 rounded-full h-1.5 overflow-hidden mt-2">
                <div className="bg-rose-500 h-full" style={{ width: '8%' }} />
              </div>
            </div>
          </div>
        </div>

        {/* Right: Reward Function & Trajectory Forecast */}
        <div className="bg-slate-950/40 border border-slate-800/60 shadow-2xl rounded-2xl p-5 backdrop-blur-3xl flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-emerald-400" />
                <h3 className="text-sm font-bold text-slate-200">Simulation Trajectory & Reward Function</h3>
              </div>
            </div>

            {/* Formula Block */}
            <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 font-mono text-[11px] text-slate-300 mb-4">
              <div className="text-amber-400 font-bold mb-1">Reward Objective:</div>
              R(s, a) = wâ‚ Â· Î”ROAS - wâ‚‚ Â· Î”CAC - Î» Â· RiskPenalty
            </div>

            {/* Performance Trajectory Milestones */}
            <div className="space-y-2 text-xs font-mono">
              <div className="flex justify-between items-center p-2 rounded-lg bg-slate-950/60 border border-slate-800">
                <span className="text-slate-400">Baseline (No Optimization):</span>
                <span className="text-slate-300 font-bold">ROAS 3.2x â€¢ CAC $49.00</span>
              </div>
              <div className="flex justify-between items-center p-2 rounded-lg bg-emerald-500/10 border border-emerald-500/30">
                <span className="text-emerald-400 font-semibold">PPO Optimized Trajectory:</span>
                <span className="text-emerald-300 font-bold">ROAS 3.84x â€¢ CAC $42.10</span>
              </div>
            </div>
          </div>

          <div className="pt-4 mt-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
            <span>Constraint Guards: <strong className="text-emerald-400">0 Violations</strong></span>
            <span>Exploration Factor: <strong className="text-cyan-400">Îµ = 0.05</strong></span>
          </div>
        </div>
      </div>
    </div>
  );
};

