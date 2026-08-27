import React, { useState } from 'react';
import { 
  BarChart3, 
  TrendingUp, 
  DollarSign, 
  Users, 
  Zap, 
  ArrowUpRight, 
  ArrowDownRight, 
  CheckCircle2, 
  Bot, 
  Layers, 
  PieChart,
  Sparkles,
  ShieldCheck,
  ChevronRight
} from 'lucide-react';

export const ExecutiveDashboardView: React.FC = () => {
  const [timeRange, setTimeRange] = useState<'7d' | '30d' | '90d'>('30d');

  const kpis = [
    {
      label: 'Managed Ad Spend',
      value: '$148,500',
      change: '+14.8%',
      trend: 'up',
      detail: 'Across 4 active networks',
      icon: DollarSign,
      color: 'text-emerald-400',
      bg: 'bg-emerald-500/10 border-emerald-500/30',
      sparkline: 'M0,25 Q15,18 30,22 T60,10 T90,14 T120,4',
      accentGlow: 'from-emerald-500/20 to-transparent',
    },
    {
      label: 'Blended AI ROAS',
      value: '4.12x',
      change: '+28.7%',
      trend: 'up',
      detail: 'vs 3.20x human baseline',
      icon: TrendingUp,
      color: 'text-cyan-400',
      bg: 'bg-cyan-500/10 border-cyan-500/30',
      sparkline: 'M0,28 Q15,22 30,16 T60,18 T90,8 T120,2',
      accentGlow: 'from-cyan-500/20 to-transparent',
    },
    {
      label: 'Average Blended CAC',
      value: '$38.40',
      change: '-26.3%',
      trend: 'down',
      detail: 'Benchmark: $52.10',
      icon: Users,
      color: 'text-purple-400',
      bg: 'bg-purple-500/10 border-purple-500/30',
      sparkline: 'M0,4 Q15,10 30,12 T60,20 T90,22 T120,28',
      accentGlow: 'from-purple-500/20 to-transparent',
    },
    {
      label: 'Autonomous Decisions',
      value: '1,482',
      change: '100% Certified',
      trend: 'up',
      detail: 'Continuous PPO Safe Guards',
      icon: Zap,
      color: 'text-amber-400',
      bg: 'bg-amber-500/10 border-amber-500/30',
      sparkline: 'M0,26 Q15,20 30,15 T60,12 T90,6 T120,2',
      accentGlow: 'from-amber-500/20 to-transparent',
    }
  ];

  const channels = [
    { name: 'LinkedIn Sponsored Ads', spend: '$65,400', share: 44, roas: '4.82x', conversions: '1,420', cpa: '$46.05', status: 'Optimal', color: 'from-cyan-500 to-blue-600' },
    { name: 'Meta Advantage+ Ads', spend: '$48,200', share: 32, roas: '3.95x', conversions: '1,280', cpa: '$37.65', status: 'Scaling', color: 'from-purple-500 to-pink-600' },
    { name: 'Google Search & GDN', spend: '$34,900', share: 24, roas: '3.65x', conversions: '960', cpa: '$36.35', status: 'Stable', color: 'from-emerald-500 to-teal-600' },
  ];

  const campaigns = [
    {
      id: 'cmp-01',
      name: 'VisionGuard AI — Q3 Enterprise SaaS Launch',
      status: 'OPTIMIZING',
      budget: '$10,000',
      spent: '$4,280',
      roas: '3.84x',
      activeAgents: '18 Agents Active',
      confidence: 94,
    },
    {
      id: 'cmp-02',
      name: 'CloudFlow Metrics — High Growth Tech Scale',
      status: 'ACTIVE_LIVE',
      budget: '$25,000',
      spent: '$19,450',
      roas: '4.60x',
      activeAgents: 'Continuous RL',
      confidence: 98,
    },
    {
      id: 'cmp-03',
      name: 'OmniRetail Pro — Multi-Format Creative Blitz',
      status: 'ACTIVE_LIVE',
      budget: '$50,000',
      spent: '$42,100',
      roas: '4.15x',
      activeAgents: 'Nano Banana + CV',
      confidence: 92,
    },
    {
      id: 'cmp-04',
      name: 'HealthPulse Enterprise — Lead Gen Sequence',
      status: 'PENDING_HITL',
      budget: '$15,000',
      spent: '$0',
      roas: '3.90x (Est)',
      activeAgents: 'Review Queue',
      confidence: 95,
    }
  ];

  const recentActions = [
    { time: '12m ago', agent: 'RL Policy Optimizer', desc: 'Shifted +12% budget into LinkedIn Sponsored Ads based on 4.82x ROAS signal.', badge: 'Budget Rebalance', color: 'text-amber-400 bg-amber-500/10 border-amber-500/30' },
    { time: '28m ago', agent: 'Computer Vision Agent', desc: 'Passed 4 new creative variations through CLIP-ViT aesthetic & safe zone filter.', badge: 'Creative Gate', color: 'text-pink-400 bg-pink-500/10 border-pink-500/30' },
    { time: '1h ago', agent: 'Analytics Agent', desc: 'Calibrated Ridge Revenue Forecaster with 2,400 new conversion datapoints.', badge: 'Model Retrain', color: 'text-cyan-400 bg-cyan-500/10 border-cyan-500/30' },
    { time: '2h ago', agent: 'Human Review Gate', desc: 'Campaign Director authorized live multi-channel deployment under constraint checks.', badge: 'Governance', color: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30' },
  ];

  return (
    <div className="w-full space-y-4 sm:space-y-6">
      {/* Header Banner */}
      <div className="glass-panel-elevated rounded-2xl p-4 sm:p-6 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />
        
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-3 sm:gap-4">
          <div>
            <div className="flex items-center gap-2.5 sm:gap-3">
              <span className="p-2 sm:p-2.5 rounded-xl bg-gradient-to-br from-cyan-500 via-blue-600 to-indigo-600 text-white shadow-lg shadow-cyan-500/25 shrink-0">
                <BarChart3 className="w-4 h-4 sm:w-5 sm:h-5" />
              </span>
              <div>
                <h2 className="text-base sm:text-xl font-black text-slate-100 flex items-center gap-2 flex-wrap">
                  Executive Intelligence & Attribution
                  <span className="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-cyan-500/10 text-cyan-300 border border-cyan-500/30">
                    Live Telemetry
                  </span>
                </h2>
                <p className="text-[11px] sm:text-xs text-slate-400 mt-0.5">
                  Macro financial attribution, multi-agent fleet operations, and autonomous ROAS policy optimization.
                </p>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-1 bg-[#07090e]/90 border border-white/[0.08] rounded-xl p-1 shrink-0 shadow-inner overflow-x-auto no-scrollbar">
            {(['7d', '30d', '90d'] as const).map((r) => (
              <button
                key={r}
                onClick={() => setTimeRange(r)}
                className={`px-2.5 sm:px-3.5 py-1.5 rounded-lg text-xs font-semibold font-mono transition-all duration-200 shrink-0 ${
                  timeRange === r
                    ? 'bg-gradient-to-r from-cyan-500/30 to-blue-500/30 text-cyan-300 border border-cyan-500/40 shadow-sm'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {r === '7d' ? '7 Days' : r === '30d' ? '30 Days' : 'Quarter'}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-3 sm:gap-4">
        {kpis.map((kpi, idx) => (
          <div 
            key={idx} 
            className="glass-card-premium p-5 flex flex-col justify-between relative overflow-hidden group hover:border-cyan-500/40"
          >
            {/* Ambient Corner Glow */}
            <div className={`absolute top-0 right-0 w-32 h-32 bg-gradient-to-bl ${kpi.accentGlow} rounded-full blur-2xl opacity-40 pointer-events-none group-hover:opacity-70 transition-opacity`} />

            <div className="flex items-center justify-between mb-4 relative z-10">
              <div className={`p-2.5 rounded-xl border ${kpi.bg} shadow-md`}>
                <kpi.icon className={`w-5 h-5 ${kpi.color}`} />
              </div>
              <span className={`flex items-center gap-0.5 text-xs font-mono font-bold px-2.5 py-1 rounded-full border ${
                kpi.trend === 'up' 
                  ? 'text-emerald-300 bg-emerald-500/15 border-emerald-500/30' 
                  : 'text-cyan-300 bg-cyan-500/15 border-cyan-500/30'
              }`}>
                {kpi.change}
                {kpi.trend === 'up' ? <ArrowUpRight className="w-3.5 h-3.5" /> : <ArrowDownRight className="w-3.5 h-3.5" />}
              </span>
            </div>

            <div className="relative z-10">
              <div className="text-3xl font-black font-mono text-slate-100 group-hover:text-cyan-300 transition-colors tracking-tight">
                {kpi.value}
              </div>
              <div className="text-xs font-bold text-slate-300 mt-1 uppercase tracking-wider font-mono">
                {kpi.label}
              </div>
              <div className="text-[11px] text-slate-400 mt-1 flex items-center justify-between">
                <span>{kpi.detail}</span>
                {/* Mini Sparkline */}
                <svg className="w-14 h-5 overflow-visible" viewBox="0 0 120 30">
                  <path
                    d={kpi.sparkline}
                    fill="none"
                    stroke={kpi.trend === 'up' ? '#10b981' : '#06b6d4'}
                    strokeWidth="2.5"
                    strokeLinecap="round"
                  />
                </svg>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Trajectory Graph & Channel Attribution Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Trajectory Curve (SVG Chart) */}
        <div className="lg:col-span-2 glass-card-premium p-6 flex flex-col justify-between shadow-2xl">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-cyan-400" />
                Autonomous ROAS Trajectory vs. Human Baseline
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">
                Continuous PPO reinforcement policy generated +28.7% alpha over standard human target.
              </p>
            </div>

            <div className="flex items-center gap-3 text-[11px] font-mono shrink-0">
              <span className="flex items-center gap-1.5 text-cyan-400 font-bold">
                <span className="w-2.5 h-2.5 rounded-full bg-cyan-400 shadow-sm shadow-cyan-400" /> AI Optimized (4.12x)
              </span>
              <span className="flex items-center gap-1.5 text-slate-500 font-medium">
                <span className="w-2.5 h-2.5 rounded-full bg-slate-600" /> Baseline (3.20x)
              </span>
            </div>
          </div>

          {/* SVG Visual Chart */}
          <div className="w-full h-56 relative bg-[#07090e]/80 border border-white/[0.08] rounded-xl p-4 flex flex-col justify-between overflow-hidden shadow-inner">
            {/* Grid Lines */}
            <div className="absolute inset-0 flex flex-col justify-between p-4 pointer-events-none opacity-15">
              <div className="border-b border-cyan-500 w-full" />
              <div className="border-b border-cyan-500 w-full" />
              <div className="border-b border-cyan-500 w-full" />
              <div className="border-b border-cyan-500 w-full" />
            </div>

            <svg className="w-full h-full overflow-visible" viewBox="0 0 500 160" preserveAspectRatio="none">
              {/* Baseline Curve */}
              <path
                d="M 0 130 Q 120 120, 250 115 T 500 110"
                fill="none"
                stroke="#64748b"
                strokeWidth="2"
                strokeDasharray="4 4"
              />

              {/* AI Optimized Area & Line */}
              <defs>
                <linearGradient id="aiGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" stopColor="#00f0ff" stopOpacity="0.35" />
                  <stop offset="100%" stopColor="#00f0ff" stopOpacity="0.0" />
                </linearGradient>
              </defs>
              
              <path
                d="M 0 130 Q 120 90, 250 60 T 500 20 L 500 160 L 0 160 Z"
                fill="url(#aiGradient)"
              />

              <path
                d="M 0 130 Q 120 90, 250 60 T 500 20"
                fill="none"
                stroke="#00f0ff"
                strokeWidth="3"
                className="drop-shadow-[0_0_12px_rgba(0,240,255,0.6)]"
              />

              {/* Peak Indicator Point */}
              <circle cx="500" cy="20" r="6" fill="#00f0ff" className="animate-pulse" />
              <circle cx="250" cy="60" r="4" fill="#38bdf8" />
              <circle cx="120" cy="90" r="4" fill="#818cf8" />
            </svg>

            <div className="flex justify-between text-[10px] font-mono text-slate-400 pt-2 border-t border-white/[0.08]">
              <span>Day 01 (Launch)</span>
              <span>Day 07 (Calibration)</span>
              <span>Day 15 (PPO Convergence)</span>
              <span>Day 22 (Scale)</span>
              <span className="text-cyan-400 font-bold">Day 30 (Current 4.12x)</span>
            </div>
          </div>
        </div>

        {/* Channel Attribution Breakdown */}
        <div className="glass-card-premium p-6 flex flex-col justify-between shadow-2xl">
          <div>
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
                <PieChart className="w-4 h-4 text-purple-400" />
                Channel Allocation
              </h3>
              <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-white/[0.06] text-slate-300 border border-white/[0.08]">
                Total $148.5k
              </span>
            </div>

            <div className="space-y-3 mt-4">
              {channels.map((ch, idx) => (
                <div key={idx} className="p-3 rounded-xl bg-[#07090e]/80 border border-white/[0.08] space-y-2 hover:border-white/[0.15] transition-colors">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-bold text-slate-200">{ch.name}</span>
                    <span className="text-emerald-400 font-mono font-bold">{ch.roas} ROAS</span>
                  </div>

                  <div className="w-full bg-slate-900 rounded-full h-2 overflow-hidden p-0.5 border border-white/[0.05]">
                    <div 
                      className={`h-full rounded-full bg-gradient-to-r ${ch.color}`}
                      style={{ width: `${ch.share}%` }}
                    />
                  </div>

                  <div className="flex justify-between text-[10px] font-mono text-slate-400">
                    <span>{ch.spend} ({ch.share}%)</span>
                    <span className="text-slate-300">CPA: {ch.cpa}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="pt-3 mt-3 border-t border-white/[0.08] text-[11px] font-mono text-slate-400 flex justify-between items-center">
            <span>Optimization Mode:</span>
            <span className="text-cyan-400 font-bold flex items-center gap-1">
              <ShieldCheck className="w-3.5 h-3.5" /> PPO Constraint Guarded
            </span>
          </div>
        </div>
      </div>

      {/* Active Campaign Portfolio Table */}
      <div className="glass-card-premium p-6 shadow-2xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
          <div>
            <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
              <Layers className="w-4 h-4 text-cyan-400" />
              Active Campaign Portfolio & Multi-Agent Fleet Status
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Live enterprise campaigns running through the autonomous 18-stage intelligence graph.
            </p>
          </div>

          <span className="text-[11px] font-mono text-cyan-300 bg-cyan-500/10 px-3 py-1 rounded-xl border border-cyan-500/30 self-start sm:self-auto font-bold">
            {campaigns.length} Campaigns Active
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead>
              <tr className="border-b border-white/[0.08] text-[10px] uppercase text-slate-400 bg-[#07090e]/60">
                <th className="py-3 px-4 rounded-l-lg">Campaign Name</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4">Budget</th>
                <th className="py-3 px-4">Spent</th>
                <th className="py-3 px-4">Current ROAS</th>
                <th className="py-3 px-4">Agent Fleet</th>
                <th className="py-3 px-4 rounded-r-lg">Confidence</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/[0.06]">
              {campaigns.map((cmp) => (
                <tr key={cmp.id} className="hover:bg-white/[0.03] transition-colors group">
                  <td className="py-3.5 px-4 font-sans font-semibold text-slate-200 group-hover:text-cyan-300 transition-colors">
                    {cmp.name}
                  </td>
                  <td className="py-3.5 px-4">
                    <span className={`px-2.5 py-1 rounded-md text-[10px] font-bold inline-flex items-center gap-1.5 ${
                      cmp.status === 'ACTIVE_LIVE'
                        ? 'bg-emerald-500/15 text-emerald-300 border border-emerald-500/30'
                        : cmp.status === 'OPTIMIZING'
                        ? 'bg-cyan-500/15 text-cyan-300 border border-cyan-500/30'
                        : 'bg-rose-500/15 text-rose-300 border border-rose-500/30'
                    }`}>
                      <span className={`w-1.5 h-1.5 rounded-full ${cmp.status === 'ACTIVE_LIVE' ? 'bg-emerald-400 animate-ping' : 'bg-cyan-400'}`} />
                      {cmp.status}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-slate-200 font-bold">{cmp.budget}</td>
                  <td className="py-3.5 px-4 text-slate-400">{cmp.spent}</td>
                  <td className="py-3.5 px-4 text-emerald-400 font-bold">{cmp.roas}</td>
                  <td className="py-3.5 px-4 text-cyan-300 font-medium">{cmp.activeAgents}</td>
                  <td className="py-3.5 px-4">
                    <div className="flex items-center gap-2">
                      <span className="text-slate-200 font-bold">{cmp.confidence}%</span>
                      <div className="w-16 bg-slate-900 rounded-full h-1.5 overflow-hidden border border-white/[0.08]">
                        <div className="bg-gradient-to-r from-cyan-500 to-blue-500 h-full rounded-full" style={{ width: `${cmp.confidence}%` }} />
                      </div>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Autonomous Action Stream */}
      <div className="glass-card-premium p-6 shadow-2xl">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Bot className="w-4 h-4 text-purple-400" />
            <h3 className="text-sm font-bold text-slate-100">Live Autonomous Action Log & Value Added</h3>
          </div>
          <span className="text-[11px] font-mono text-cyan-400 flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" /> Auto-streaming live
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {recentActions.map((act, i) => (
            <div key={i} className="p-3.5 rounded-xl bg-[#07090e]/80 border border-white/[0.08] flex items-start gap-3 hover:border-cyan-500/30 transition-all">
              <div className="p-2 rounded-lg bg-cyan-500/10 border border-cyan-500/20 shrink-0 mt-0.5 text-cyan-400">
                <CheckCircle2 className="w-4 h-4" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between gap-2 mb-1">
                  <span className="text-xs font-bold text-slate-200 font-mono">{act.agent}</span>
                  <span className="text-[10px] text-slate-500 font-mono">{act.time}</span>
                </div>
                <p className="text-xs text-slate-400 font-sans leading-relaxed">
                  {act.desc}
                </p>
                <div className="mt-2">
                  <span className={`inline-block px-2 py-0.5 rounded text-[9px] font-mono font-bold border ${act.color}`}>
                    {act.badge}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
