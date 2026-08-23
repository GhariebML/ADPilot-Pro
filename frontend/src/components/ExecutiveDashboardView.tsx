import React, { useState } from 'react';
import { 
  BarChart3, 
  TrendingUp, 
  DollarSign, 
  Users, 
  Zap, 
  Activity, 
  Sparkles, 
  ArrowUpRight, 
  ArrowDownRight, 
  ShieldCheck, 
  CheckCircle2, 
  Bot, 
  Cpu, 
  Layers, 
  Clock, 
  ArrowRight,
  PieChart,
  Eye
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
      bg: 'bg-emerald-500/10 border-emerald-500/20'
    },
    {
      label: 'Blended AI ROAS',
      value: '4.12x',
      change: '+28.7%',
      trend: 'up',
      detail: 'vs 3.20x human baseline',
      icon: TrendingUp,
      color: 'text-cyan-400',
      bg: 'bg-cyan-500/10 border-cyan-500/20'
    },
    {
      label: 'Average Blended CAC',
      value: '$38.40',
      change: '-26.3%',
      trend: 'down',
      detail: 'Industry benchmark: $52.10',
      icon: Users,
      color: 'text-purple-400',
      bg: 'bg-purple-500/10 border-purple-500/20'
    },
    {
      label: 'Autonomous Decisions',
      value: '1,482',
      change: '100% Verified',
      trend: 'up',
      detail: 'PPO & Constraint Guarded',
      icon: Zap,
      color: 'text-amber-400',
      bg: 'bg-amber-500/10 border-amber-500/20'
    }
  ];

  const channels = [
    { name: 'LinkedIn Sponsored Ads', spend: '$65,400', share: 44, roas: '4.82x', conversions: '1,420', cpa: '$46.05', status: 'Optimal' },
    { name: 'Meta Advantage+ Ads', spend: '$48,200', share: 32, roas: '3.95x', conversions: '1,280', cpa: '$37.65', status: 'Scaling' },
    { name: 'Google Search & GDN', spend: '$34,900', share: 24, roas: '3.65x', conversions: '960', cpa: '$36.35', status: 'Stable' },
  ];

  const campaigns = [
    {
      id: 'cmp-01',
      name: 'VisionGuard AI â€” Q3 Enterprise SaaS Launch',
      status: 'OPTIMIZING',
      budget: '$10,000',
      spent: '$4,280',
      roas: '3.84x',
      activeAgents: '10 Agents Active',
      confidence: 94,
    },
    {
      id: 'cmp-02',
      name: 'CloudFlow Metrics â€” High Growth Tech Scale',
      status: 'ACTIVE_LIVE',
      budget: '$25,000',
      spent: '$19,450',
      roas: '4.60x',
      activeAgents: 'Continuous RL',
      confidence: 98,
    },
    {
      id: 'cmp-03',
      name: 'OmniRetail Pro â€” Multi-Format Creative Blitz',
      status: 'ACTIVE_LIVE',
      budget: '$50,000',
      spent: '$42,100',
      roas: '4.15x',
      activeAgents: 'Nano Banana + CV',
      confidence: 92,
    },
    {
      id: 'cmp-04',
      name: 'HealthPulse Enterprise â€” Lead Gen Sequence',
      status: 'PENDING_HITL',
      budget: '$15,000',
      spent: '$0',
      roas: '3.90x (Est)',
      activeAgents: 'Review Queue',
      confidence: 95,
    }
  ];

  const recentActions = [
    { time: '12m ago', agent: 'RL Policy Optimizer', desc: 'Shifted +12% budget into LinkedIn Sponsored Ads based on 4.82x ROAS signal.', badge: 'Budget Rebalance', color: 'text-amber-400 bg-amber-500/10 border-amber-500/20' },
    { time: '28m ago', agent: 'Computer Vision Agent', desc: 'Passed 4 new creative variations through CLIP-ViT aesthetic & safe zone filter.', badge: 'Creative Gate', color: 'text-pink-400 bg-pink-500/10 border-pink-500/20' },
    { time: '1h ago', agent: 'Analytics Agent', desc: 'Calibrated Ridge Revenue Forecaster with 2,400 new conversion datapoints.', badge: 'Model Retrain', color: 'text-cyan-400 bg-cyan-500/10 border-cyan-500/20' },
    { time: '2h ago', agent: 'Human Review Gate', desc: 'Campaign Director approved live Meta Ads creative set deployment.', badge: 'Governance', color: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20' },
  ];

  return (
    <div className="w-full space-y-6">
      {/* Header Banner */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 relative overflow-hidden backdrop-blur-3xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2.5">
              <span className="p-2 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/20">
                <BarChart3 className="w-5 h-5" />
              </span>
              <div>
                <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
                  Executive Intelligence & Attribution Dashboard
                </h2>
                <p className="text-xs text-slate-400 mt-0.5">
                  Macro-level financial attribution, multi-agent fleet operations, and autonomous ROAS optimization telemetry.
                </p>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2 bg-slate-950/40 border border-slate-800/60 shadow-2xl rounded-xl p-1.5 shrink-0">
            {(['7d', '30d', '90d'] as const).map((r) => (
              <button
                key={r}
                onClick={() => setTimeRange(r)}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold font-mono transition-all ${
                  timeRange === r
                    ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {r === '7d' ? 'Last 7 Days' : r === '30d' ? 'Last 30 Days' : 'Last Quarter'}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
        {kpis.map((kpi, idx) => (
          <div key={idx} className="bg-slate-950/40 border border-slate-800/60 rounded-2xl p-6 backdrop-blur-3xl flex flex-col justify-between hover:border-slate-700/80 hover:-translate-y-1 hover:shadow-2xl hover:shadow-black/40 transition-all duration-300 ease-out group">
            <div className="flex items-center justify-between mb-3">
              <div className={`p-2.5 rounded-xl border ${kpi.bg}`}>
                <kpi.icon className={`w-5 h-5 ${kpi.color}`} />
              </div>
              <span className={`flex items-center gap-0.5 text-xs font-mono font-bold px-2 py-0.5 rounded-full ${
                kpi.trend === 'up' ? 'text-emerald-400 bg-emerald-500/10' : 'text-cyan-400 bg-cyan-500/10'
              }`}>
                {kpi.change}
                {kpi.trend === 'up' ? <ArrowUpRight className="w-3.5 h-3.5" /> : <ArrowDownRight className="w-3.5 h-3.5" />}
              </span>
            </div>

            <div>
              <div className="text-2xl font-black font-mono text-slate-100 group-hover:text-cyan-300 transition-colors">
                {kpi.value}
              </div>
              <div className="text-xs font-bold text-slate-400 mt-1 uppercase tracking-wider font-mono">
                {kpi.label}
              </div>
              <div className="text-[11px] text-slate-500 mt-1">
                {kpi.detail}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Trajectory Graph & Channel Attribution Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Trajectory Curve (SVG Chart) */}
        <div className="lg:col-span-2 bg-slate-950/40 border border-slate-800/60 rounded-2xl p-6 backdrop-blur-3xl shadow-2xl flex flex-col justify-between">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-cyan-400" />
                Autonomous ROAS Trajectory vs. Human Baseline
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">
                Continuous PPO reinforcement policy generated +28.7% alpha over standard target baseline.
              </p>
            </div>

            <div className="flex items-center gap-3 text-[11px] font-mono shrink-0">
              <span className="flex items-center gap-1.5 text-cyan-400">
                <span className="w-2.5 h-2.5 rounded-full bg-cyan-400" /> AI Optimized (4.12x)
              </span>
              <span className="flex items-center gap-1.5 text-slate-500">
                <span className="w-2.5 h-2.5 rounded-full bg-slate-600" /> Human Baseline (3.20x)
              </span>
            </div>
          </div>

          {/* SVG Visual Chart */}
          <div className="w-full h-56 relative bg-slate-950/70 border border-slate-800/80 rounded-xl p-4 flex flex-col justify-between overflow-hidden">
            {/* Grid Lines */}
            <div className="absolute inset-0 flex flex-col justify-between p-4 pointer-events-none opacity-20">
              <div className="border-b border-slate-700 w-full" />
              <div className="border-b border-slate-700 w-full" />
              <div className="border-b border-slate-700 w-full" />
              <div className="border-b border-slate-700 w-full" />
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
                  <stop offset="0%" stopColor="#06b6d4" stopOpacity="0.3" />
                  <stop offset="100%" stopColor="#06b6d4" stopOpacity="0.0" />
                </linearGradient>
              </defs>
              
              <path
                d="M 0 130 Q 120 90, 250 60 T 500 20 L 500 160 L 0 160 Z"
                fill="url(#aiGradient)"
              />

              <path
                d="M 0 130 Q 120 90, 250 60 T 500 20"
                fill="none"
                stroke="#22d3ee"
                strokeWidth="3"
                className="drop-shadow-[0_0_8px_rgba(34,211,238,0.5)]"
              />

              {/* Peak Indicator Point */}
              <circle cx="500" cy="20" r="5" fill="#22d3ee" className="animate-pulse" />
            </svg>

            <div className="flex justify-between text-[10px] font-mono text-slate-500 pt-2 border-t border-slate-800/80">
              <span>Day 01</span>
              <span>Day 07</span>
              <span>Day 15</span>
              <span>Day 22</span>
              <span>Day 30 (Current)</span>
            </div>
          </div>
        </div>

        {/* Channel Attribution Breakdown */}
        <div className="bg-slate-950/40 border border-slate-800/60 rounded-2xl p-6 backdrop-blur-3xl shadow-2xl flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
                <PieChart className="w-4 h-4 text-purple-400" />
                Channel Allocation
              </h3>
              <span className="text-[10px] font-mono text-slate-400">Total $148.5k</span>
            </div>

            <div className="space-y-3 mt-4">
              {channels.map((ch, idx) => (
                <div key={idx} className="p-3 rounded-xl bg-slate-950/70 border border-slate-800/80 space-y-2">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-bold text-slate-200">{ch.name}</span>
                    <span className="text-emerald-400 font-mono font-bold">{ch.roas} ROAS</span>
                  </div>

                  <div className="w-full bg-slate-900 rounded-full h-1.5 overflow-hidden">
                    <div 
                      className={`h-full ${
                        idx === 0 ? 'bg-cyan-500' : idx === 1 ? 'bg-purple-500' : 'bg-blue-500'
                      }`}
                      style={{ width: `${ch.share}%` }}
                    />
                  </div>

                  <div className="flex justify-between text-[10px] font-mono text-slate-500">
                    <span>{ch.spend} ({ch.share}%)</span>
                    <span>CPA: {ch.cpa}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="pt-3 mt-3 border-t border-slate-800/80 text-[11px] font-mono text-slate-400 flex justify-between">
            <span>Optimization Mode:</span>
            <span className="text-cyan-400 font-bold">Dynamic PPO Balancing</span>
          </div>
        </div>
      </div>

      {/* Active Campaign Portfolio Table */}
      <div className="bg-slate-950/40 border border-slate-800/60 rounded-2xl p-6 backdrop-blur-3xl shadow-2xl">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
              <Layers className="w-4 h-4 text-cyan-400" />
              Active Campaign Portfolio & Multi-Agent State
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Real-time campaign contracts running through the 18-stage intelligence pipeline.
            </p>
          </div>

          <span className="text-[11px] font-mono text-slate-400 bg-slate-950 px-3 py-1 rounded-xl border border-slate-800">
            {campaigns.length} Campaigns Managed
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead>
              <tr className="border-b border-slate-800 text-[10px] uppercase text-slate-500 bg-slate-950/60">
                <th className="py-3 px-4 rounded-l-lg">Campaign Name</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4">Budget</th>
                <th className="py-3 px-4">Spent</th>
                <th className="py-3 px-4">Current ROAS</th>
                <th className="py-3 px-4">Agent Fleet</th>
                <th className="py-3 px-4 rounded-r-lg">Confidence</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {campaigns.map((cmp) => (
                <tr key={cmp.id} className="hover:bg-slate-800/40 transition-colors group">
                  <td className="py-3 px-4 font-sans font-semibold text-slate-200 group-hover:text-cyan-300">
                    {cmp.name}
                  </td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                      cmp.status === 'ACTIVE_LIVE'
                        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                        : cmp.status === 'OPTIMIZING'
                        ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/30'
                        : 'bg-rose-500/10 text-rose-400 border border-rose-500/30'
                    }`}>
                      {cmp.status}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-slate-300 font-bold">{cmp.budget}</td>
                  <td className="py-3 px-4 text-slate-400">{cmp.spent}</td>
                  <td className="py-3 px-4 text-emerald-400 font-bold">{cmp.roas}</td>
                  <td className="py-3 px-4 text-cyan-300">{cmp.activeAgents}</td>
                  <td className="py-3 px-4">
                    <div className="flex items-center gap-2">
                      <span className="text-slate-200">{cmp.confidence}%</span>
                      <div className="w-12 bg-slate-950 rounded-full h-1 overflow-hidden">
                        <div className="bg-cyan-500 h-full" style={{ width: `${cmp.confidence}%` }} />
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
      <div className="bg-slate-950/40 border border-slate-800/60 rounded-2xl p-6 backdrop-blur-3xl shadow-2xl">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Bot className="w-4 h-4 text-purple-400" />
            <h3 className="text-sm font-bold text-slate-100">Live Autonomous Action Log & Value Added</h3>
          </div>
          <span className="text-[11px] font-mono text-slate-500">Auto-streaming live</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {recentActions.map((act, i) => (
            <div key={i} className="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800/80 flex items-start gap-3">
              <div className="p-2 rounded-lg bg-slate-900 border border-slate-800 shrink-0 mt-0.5">
                <CheckCircle2 className="w-4 h-4 text-cyan-400" />
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

