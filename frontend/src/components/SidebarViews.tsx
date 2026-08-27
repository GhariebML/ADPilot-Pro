import React from 'react';
import {
  Target, Search, LayoutDashboard, Settings, Lock,
  BookOpen, TrendingUp, Users, Lightbulb, Clock,
  Palette, BarChart2, Bookmark, Trash2, Download,
  Sun, Moon, Globe, Shield, Activity, DollarSign,
  MousePointerClick, Megaphone, Zap, Sparkles
} from 'lucide-react';
import { ExecutiveDashboardView } from './ExecutiveDashboardView';

/* ─────────────────────────────────────
   Reusable Components
───────────────────────────────────── */

const PhaseBadge = () => (
  <span className="px-2 py-0.5 text-[9px] font-bold rounded-full border border-cyan-500/30 bg-cyan-500/10 text-cyan-300 font-mono uppercase tracking-widest">
    v3.0 Certified
  </span>
);

const ComingSoonCard: React.FC<{ icon: React.ElementType; label: string; description: string; color: string }> = ({
  icon: Icon, label, description, color,
}) => (
  <div className="glass-card-premium p-3.5 sm:p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3 sm:gap-4 hover:border-cyan-500/40 transition-all duration-200 group">
    <div className="flex items-center gap-3 min-w-0">
      <div className={`w-9 h-9 sm:w-10 sm:h-10 rounded-xl flex items-center justify-center border ${color} group-hover:scale-105 transition-transform shrink-0`}>
        <Icon size={18} />
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-xs font-bold text-slate-100 group-hover:text-cyan-300 transition-colors truncate">{label}</p>
        <p className="text-[11px] sm:text-xs text-slate-400 leading-snug transition-colors">{description}</p>
      </div>
    </div>
    <div className="self-start sm:self-auto shrink-0">
      <PhaseBadge />
    </div>
  </div>
);

const SectionHeader: React.FC<{ icon: React.ElementType; title: string; subtitle: string; color: string }> = ({
  icon: Icon, title, subtitle, color,
}) => (
  <div className="mb-4 sm:mb-6 pb-3 sm:pb-4 border-b border-white/[0.08]">
    <div className="flex items-center gap-2.5 sm:gap-3 mb-1.5 sm:mb-2">
      <div className="p-1.5 sm:p-2 rounded-xl bg-white/[0.05] border border-white/[0.08] shrink-0">
        <Icon size={18} className={color} />
      </div>
      <h2 className="text-base sm:text-lg font-black text-slate-100">{title}</h2>
    </div>
    <p className="text-[11px] sm:text-xs text-slate-400 ml-9 sm:ml-11">{subtitle}</p>
  </div>
);

/* ─────────────────────────────────────
   Dashboard Overview View (Top Tab)
───────────────────────────────────── */
export const DashboardView: React.FC = () => (
  <div className="w-full">
    <ExecutiveDashboardView />
  </div>
);

/* ─────────────────────────────────────
   Analytics View (Top Tab)
───────────────────────────────────── */
export const AnalyticsView: React.FC = () => (
  <div className="w-full space-y-5 max-w-4xl mx-auto animate-in fade-in duration-300">
    <SectionHeader
      icon={BarChart2}
      title="Campaign Analytics & Attribution"
      subtitle="Deep dive into individual channel performance, budget allocation and ROAS"
      color="text-amber-400"
    />
    <div className="glass-panel-elevated p-6 border-l-4 border-l-amber-500 rounded-2xl mb-6 shadow-2xl">
      <div className="flex items-start gap-3 mb-4">
        <BarChart2 size={18} className="text-amber-400 mt-0.5 shrink-0" />
        <div>
          <p className="text-xs font-bold text-amber-300 mb-1 font-mono uppercase tracking-wider">Analytics Agent Telemetry</p>
          <p className="text-xs text-slate-300 leading-relaxed">
            The Analytics Agent forecasts multi-channel performance metrics, recommends dynamic PPO budget reallocations based on real-time ROAS feedback, and generates A/B test variations to maximize campaign ROI.
          </p>
        </div>
      </div>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-2.5 mt-4">
        {['ROI Forecasting', 'Budget Optimization', 'A/B Test Analysis', 'Channel Attribution', 'CAC Tracking', 'LTV Projections'].map((item) => (
          <div key={item} className="flex items-center gap-2 p-2.5 rounded-xl bg-[#07090e]/80 border border-white/[0.08] hover:border-amber-500/30 transition-colors">
            <div className="w-1.5 h-1.5 rounded-full bg-amber-400 shrink-0" />
            <p className="text-xs text-slate-300 font-mono font-medium">{item}</p>
          </div>
        ))}
      </div>
    </div>
    <div className="space-y-4">
      <ComingSoonCard icon={LayoutDashboard} label="Real-Time Custom Dashboards" description="Build custom multi-tenant reporting views and automated executive digests" color="bg-amber-500/15 border-amber-500/30 text-amber-400" />
      <ComingSoonCard icon={Target} label="Autonomous Milestone Alerts" description="Instant webhook and Slack notifications when campaigns exceed ROAS thresholds" color="bg-amber-500/15 border-amber-500/30 text-amber-400" />
    </div>
  </div>
);

/* ─────────────────────────────────────
   Strategy Insights View
───────────────────────────────────── */
export const StrategyView: React.FC = () => (
  <div className="w-full space-y-5">
    <SectionHeader
      icon={Target}
      title="Strategy Insights & Positioning"
      subtitle="Campaign positioning, strategic objectives, and tactical multi-channel roadmap"
      color="text-cyan-400"
    />
    <div className="glass-panel-elevated p-6 border-l-4 border-l-cyan-500 rounded-2xl shadow-2xl">
      <div className="flex items-start gap-3 mb-5">
        <Target size={18} className="text-cyan-400 mt-0.5 shrink-0" />
        <div>
          <p className="text-xs font-bold text-cyan-300 mb-1 font-mono uppercase tracking-wider">Strategy Agent Directives</p>
          <p className="text-xs text-slate-300 leading-relaxed">
            The Strategy Agent decomposes raw marketing briefs into comprehensive go-to-market strategies: positioning statements, competitive differentiation axes, ICP psychological purchase drivers, and tactical channel allocation plans.
          </p>
        </div>
      </div>
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5 mt-4">
        {['Brand Positioning', 'Market Segmentation', 'Channel Mix', 'Budget Allocation', 'Timeline Planning', 'KPI Definition'].map((item) => (
          <div key={item} className="flex items-center gap-2 p-2.5 rounded-xl bg-[#07090e]/80 border border-white/[0.08] hover:border-cyan-500/40 transition-all cursor-pointer group">
            <div className="w-1.5 h-1.5 rounded-full bg-cyan-400 shrink-0 group-hover:scale-125 transition-transform" />
            <p className="text-xs text-slate-300 group-hover:text-cyan-200 transition-colors font-medium font-mono">{item}</p>
          </div>
        ))}
      </div>
    </div>
    <ComingSoonCard icon={TrendingUp} label="Automated SWOT Matrix" description="AI-synthesized strengths, weaknesses, opportunities, and competitive vulnerabilities" color="bg-cyan-500/15 border-cyan-500/30 text-cyan-400" />
    <ComingSoonCard icon={Lightbulb} label="Strategic Tactical Playbooks" description="Data-driven execution blueprints with confidence-scored priority rankings" color="bg-blue-500/15 border-blue-500/30 text-blue-400" />
    <ComingSoonCard icon={BookOpen} label="Enterprise Playbook PDF Export" description="Full high-resolution marketing playbook and executive summary export" color="bg-purple-500/15 border-purple-500/30 text-purple-400" />
  </div>
);

/* ─────────────────────────────────────
   Audience Research View
───────────────────────────────────── */
export const ResearchView: React.FC = () => (
  <div className="w-full space-y-5">
    <SectionHeader
      icon={Search}
      title="Audience & Market Intelligence"
      subtitle="Competitor intelligence, psychographic mapping, and live market signals"
      color="text-purple-400"
    />
    <div className="glass-panel-elevated p-6 border-l-4 border-l-purple-500 rounded-2xl shadow-2xl">
      <div className="flex items-start gap-3 mb-5">
        <Search size={18} className="text-purple-400 mt-0.5 shrink-0" />
        <div>
          <p className="text-xs font-bold text-purple-300 mb-1 font-mono uppercase tracking-wider">Research Agent Knowledge Space</p>
          <p className="text-xs text-slate-300 leading-relaxed">
            The Research Agent aggregates real-time market data via SerpAPI and multi-tier vector RAG, maps competitor ad messaging strategies, extracts ICP pain points, and calibrates copy tone for maximum resonance.
          </p>
        </div>
      </div>
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5 mt-4">
        {['Competitor Mapping', 'Audience Personas', 'Trend Analysis', 'Keyword Research', 'Pain Point ID', 'Market Sizing'].map((item) => (
          <div key={item} className="flex items-center gap-2 p-2.5 rounded-xl bg-[#07090e]/80 border border-white/[0.08] hover:border-purple-500/40 transition-all cursor-pointer group">
            <div className="w-1.5 h-1.5 rounded-full bg-purple-400 shrink-0 group-hover:scale-125 transition-transform" />
            <p className="text-xs text-slate-300 group-hover:text-purple-200 transition-colors font-medium font-mono">{item}</p>
          </div>
        ))}
      </div>
    </div>
    <ComingSoonCard icon={Users} label="Dynamic Persona Simulator" description="Interactive buyer persona simulator with psychographic sensitivity dials" color="bg-purple-500/15 border-purple-500/30 text-purple-400" />
    <ComingSoonCard icon={Globe} label="Live SERP & Social Radar" description="Real-time market sentiment and competitor ad spend trajectory tracking" color="bg-cyan-500/15 border-cyan-500/30 text-cyan-400" />
  </div>
);

/* ─────────────────────────────────────
   Saved Content View
───────────────────────────────────── */
const mockSaved = [
  { name: 'VisionGuard AI — Enterprise Launch', date: '2026-08-20', status: 'Completed', color: 'text-emerald-400' },
  { name: 'AeroPulse Audio — D2C Blitz', date: '2026-08-18', status: 'Completed', color: 'text-emerald-400' },
  { name: 'Skyline Residences — Penthouse Scale', date: '2026-08-15', status: 'Active Live', color: 'text-cyan-400' },
];

export const SavedView: React.FC = () => (
  <div className="w-full space-y-5">
    <SectionHeader
      icon={LayoutDashboard}
      title="Saved Campaign Portfolio"
      subtitle="History of previous autonomous campaign packages and contracts"
      color="text-slate-300"
    />
    <div className="space-y-3">
      {mockSaved.map((item, idx) => (
        <div key={idx} className="glass-card-premium p-4 flex items-center justify-between group hover:border-cyan-500/40 transition-all">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center shrink-0 text-cyan-400">
              <Bookmark size={15} />
            </div>
            <div>
              <p className="text-xs font-bold text-slate-100 group-hover:text-cyan-300 transition-colors">{item.name}</p>
              <div className="flex items-center gap-2 mt-0.5">
                <Clock size={11} className="text-slate-500" />
                <p className="text-[10px] text-slate-400 font-mono">{item.date}</p>
                <span className={`text-[9px] font-bold font-mono uppercase tracking-wider ${item.color}`}>{item.status}</span>
              </div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button className="p-2 rounded-lg bg-[#07090e] border border-white/[0.08] hover:bg-slate-800 text-slate-400 hover:text-cyan-300 transition-colors">
              <Download size={13} />
            </button>
            <button className="p-2 rounded-lg bg-[#07090e] border border-white/[0.08] hover:bg-rose-500/20 text-slate-400 hover:text-rose-400 transition-colors">
              <Trash2 size={13} />
            </button>
          </div>
        </div>
      ))}
    </div>
  </div>
);

/* ─────────────────────────────────────
   Settings View
───────────────────────────────────── */
export const SettingsView: React.FC<{ theme: string; toggleTheme: () => void }> = ({ theme, toggleTheme }) => (
  <div className="w-full space-y-5">
    <SectionHeader
      icon={Settings}
      title="System Settings & Configuration"
      subtitle="Manage workspace preferences, API credentials, and agent model backends"
      color="text-slate-300"
    />

    {/* Theme Preference */}
    <div className="glass-panel-elevated rounded-2xl p-5 space-y-4 shadow-2xl">
      <div className="flex items-center justify-between">
        <p className="text-[10px] font-mono font-bold text-slate-400 uppercase tracking-widest">Interface Appearance</p>
        <span className="text-[10px] font-mono text-cyan-400">Active: {theme.toUpperCase()}</span>
      </div>
      
      <div className="grid grid-cols-2 gap-3">
        {/* Dark Mode Tile */}
        <button
          type="button"
          onClick={() => theme !== 'dark' && toggleTheme()}
          className={`p-3.5 rounded-xl border text-left flex items-center justify-between transition-all ${
            theme === 'dark'
              ? 'bg-gradient-to-r from-blue-600/25 to-cyan-500/25 border-cyan-400 text-white shadow-lg shadow-cyan-500/10'
              : 'bg-[#07090e]/80 border-white/[0.08] text-slate-400 hover:text-slate-200'
          }`}
        >
          <div className="flex items-center gap-3">
            <Moon size={16} className="text-cyan-400" />
            <div>
              <p className="text-xs font-bold">Obsidian Cyber Dark</p>
              <p className="text-[10px] text-slate-400 font-mono mt-0.5">Deep space cyberpunk palette</p>
            </div>
          </div>
        </button>

        {/* Light Mode Tile */}
        <button
          type="button"
          onClick={() => theme !== 'light' && toggleTheme()}
          className={`p-3.5 rounded-xl border text-left flex items-center justify-between transition-all ${
            theme === 'light'
              ? 'bg-gradient-to-r from-amber-500/25 to-yellow-500/25 border-amber-400 text-white shadow-lg shadow-amber-500/10'
              : 'bg-[#07090e]/80 border-white/[0.08] text-slate-400 hover:text-slate-200'
          }`}
        >
          <div className="flex items-center gap-3">
            <Sun size={16} className="text-amber-400" />
            <div>
              <p className="text-xs font-bold">Daylight Mode</p>
              <p className="text-[10px] text-slate-400 font-mono mt-0.5">High readability bright theme</p>
            </div>
          </div>
        </button>
      </div>
    </div>

    {/* API Keys */}
    <div className="glass-panel-elevated rounded-2xl p-5 space-y-4 shadow-2xl">
      <p className="text-[10px] font-mono font-bold text-slate-400 uppercase tracking-widest">API Configuration & Providers</p>
      {[
        { label: 'Google Gemini / OpenAI Key', placeholder: 'sk-••••••••••••••••••••••••', icon: Lock },
        { label: 'SerpAPI Search Engine Key', placeholder: 'serp-••••••••••••••••••••••', icon: Globe },
      ].map((field) => (
        <div key={field.label}>
          <label className="block text-[10px] font-mono font-bold text-slate-400 uppercase tracking-wider mb-1.5">{field.label}</label>
          <div className="relative">
            <field.icon size={14} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
            <input
              type="password"
              placeholder={field.placeholder}
              className="w-full bg-[#07090e] border border-white/[0.08] rounded-xl pl-9 pr-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-cyan-400 placeholder:text-slate-600 font-mono shadow-inner"
            />
          </div>
        </div>
      ))}
      <button className="w-full py-2.5 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white text-xs font-mono font-bold rounded-xl shadow-lg shadow-cyan-500/20 transition-all active:scale-98">
        Save API Configurations
      </button>
    </div>

    {/* About */}
    <div className="glass-card-premium p-4 rounded-xl text-center space-y-2 flex flex-col items-center">
      <div className="w-12 h-12 rounded-xl bg-slate-900/90 border border-cyan-500/30 p-1.5 flex items-center justify-center shadow-lg shadow-cyan-500/10">
        <img src="/logo.png" alt="ADPilot Logo" className="w-full h-full object-contain filter drop-shadow-[0_0_8px_rgba(6,182,212,0.6)]" />
      </div>
      <div>
        <p className="text-xs font-bold text-white">ADPilot Pro v3.0 Enterprise</p>
        <p className="text-[10px] text-slate-400 font-mono">18-Stage Autonomous Multi-Agent Campaign Operating System</p>
        <p className="text-[10px] text-cyan-400 font-mono font-semibold mt-1">Built with Precision & Deterministic Epistemic Contracts</p>
      </div>
    </div>
  </div>
);
