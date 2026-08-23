import React from 'react';
import { 
  Play, 
  ShieldCheck, 
  Download, 
  Sparkles, 
  Cpu, 
  Layers, 
  CheckCircle2
} from 'lucide-react';
import type { CampaignBrief } from '../types';

interface CampaignControlBarProps {
  campaign: CampaignBrief | null;
  activeTaskId?: string | null;
  progress: number;
  status: 'idle' | 'pending' | 'in_progress' | 'completed' | 'failed';
  activeAgentsCount: number;
  totalAgentsCount: number;
  confidenceScore?: number;
  onPauseResume?: () => void;
  onOpenHITL?: () => void;
  onExportReport?: () => void;
  onOpenDemo?: () => void;
}

export const CampaignControlBar: React.FC<CampaignControlBarProps> = ({
  campaign,
  progress,
  status,
  activeAgentsCount,
  totalAgentsCount,
  confidenceScore = 94,
  onOpenHITL,
  onExportReport,
  onOpenDemo,
}) => {
  const isRunning = status === 'in_progress' || status === 'pending';
  const isDone = status === 'completed';

  return (
    <div className="w-full glass-panel-elevated rounded-2xl p-4 sm:p-5 shadow-2xl relative overflow-hidden mb-6">
      {/* Background Subtle Cyber Mesh & Top Glowing Border */}
      <div className="absolute inset-0 bg-gradient-to-r from-cyan-900/10 via-blue-900/10 to-purple-900/10 pointer-events-none" />
      <div className="absolute top-0 left-0 right-0 h-[2.5px] bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-500" />

      <div className="relative z-10 flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        {/* Left Side: Campaign Context & Metadata */}
        <div className="flex items-start sm:items-center gap-4">
          <div className="w-11 h-11 rounded-xl bg-gradient-to-br from-cyan-500/25 to-blue-600/25 border border-cyan-500/40 flex items-center justify-center text-cyan-300 shadow-lg shadow-cyan-500/20 shrink-0">
            <Cpu className="w-5 h-5 animate-pulse-slow" />
          </div>
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <h2 className="text-base font-black text-slate-100">
                {campaign?.businessName || 'AI Enterprise Growth Campaign'}
              </h2>
              <span className="px-2.5 py-0.5 rounded-full text-xs font-mono font-bold bg-cyan-500/15 text-cyan-300 border border-cyan-500/30">
                {campaign?.productName || 'AI SaaS Platform'}
              </span>
              <span className="px-2.5 py-0.5 rounded-full text-xs font-mono font-medium bg-purple-500/15 text-purple-300 border border-purple-500/30">
                {campaign?.duration || '30 Days'}
              </span>
              <span className="px-2.5 py-0.5 rounded-full text-xs font-mono font-bold bg-emerald-500/15 text-emerald-300 border border-emerald-500/30">
                ${campaign?.budget?.toLocaleString() || '10,000'} USD
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-1 flex items-center gap-2 font-sans">
              <span>Goal: <strong className="text-slate-200">{campaign?.goals?.join(', ') || 'Lead Generation & Sales'}</strong></span>
              <span className="text-slate-600">•</span>
              <span>Audience: <strong className="text-slate-200 truncate max-w-xs">{campaign?.targetAudience || 'B2B Mid-Market & SaaS Founders'}</strong></span>
            </p>
          </div>
        </div>

        {/* Middle: Live Pipeline Status Metrics */}
        <div className="flex items-center gap-4 sm:gap-6 bg-[#07090e]/90 border border-white/[0.08] rounded-xl px-4 py-2 shrink-0 shadow-inner">
          <div>
            <div className="text-[10px] text-slate-400 font-mono font-bold uppercase tracking-wider">System State</div>
            <div className="flex items-center gap-2 mt-0.5">
              {isRunning ? (
                <span className="inline-flex items-center gap-1.5 text-xs font-bold text-cyan-300 font-mono">
                  <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
                  Running Pipeline
                </span>
              ) : isDone ? (
                <span className="inline-flex items-center gap-1.5 text-xs font-bold text-emerald-400 font-mono">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  Execution Ready
                </span>
              ) : (
                <span className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-400 font-mono">
                  <span className="w-2 h-2 rounded-full bg-slate-500" />
                  Idle
                </span>
              )}
            </div>
          </div>

          <div className="h-6 w-[1px] bg-white/[0.08]" />

          <div>
            <div className="text-[10px] text-slate-400 font-mono font-bold uppercase tracking-wider">Active Fleet</div>
            <div className="flex items-center gap-1.5 mt-0.5 text-xs font-bold text-slate-100 font-mono">
              <Layers className="w-3.5 h-3.5 text-purple-400" />
              <span>{isDone ? totalAgentsCount : activeAgentsCount}/{totalAgentsCount} Agents</span>
            </div>
          </div>

          <div className="h-6 w-[1px] bg-white/[0.08]" />

          <div>
            <div className="text-[10px] text-slate-400 font-mono font-bold uppercase tracking-wider">Confidence</div>
            <div className="flex items-center gap-1 mt-0.5 text-xs font-bold text-emerald-400 font-mono">
              <Sparkles className="w-3.5 h-3.5" />
              <span>{confidenceScore}%</span>
            </div>
          </div>
        </div>

        {/* Right Side: Action Buttons */}
        <div className="flex items-center gap-2 flex-wrap sm:flex-nowrap">
          <button
            onClick={onOpenDemo}
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold font-mono bg-gradient-to-r from-cyan-500/20 to-blue-500/20 hover:from-cyan-500/30 hover:to-blue-500/30 text-cyan-300 border border-cyan-500/40 transition-all shadow-sm active:scale-95"
            title="Launch Interactive Step-by-Step AI Simulation Demo"
          >
            <Play className="w-3.5 h-3.5 fill-cyan-400" />
            <span>Interactive Demo</span>
          </button>

          <button
            onClick={onOpenHITL}
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold font-mono bg-amber-500/15 hover:bg-amber-500/25 text-amber-300 border border-amber-500/40 transition-all active:scale-95"
            title="Open Human-in-the-Loop Governance Gate"
          >
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>HITL Review</span>
          </button>

          <button
            onClick={onExportReport}
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-mono font-semibold bg-[#07090e] hover:bg-slate-800 text-slate-200 border border-white/[0.08] transition-all active:scale-95"
            title="Export Intelligence Package"
          >
            <Download className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Export</span>
          </button>
        </div>
      </div>

      {/* Real-time Progress Bar */}
      {isRunning && (
        <div className="mt-4 pt-3 border-t border-white/[0.08]">
          <div className="flex justify-between items-center text-xs text-slate-400 mb-1.5">
            <span className="font-mono text-cyan-400 font-bold flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" /> Autonomous Execution Stream
            </span>
            <span className="font-mono font-bold text-slate-200">{progress}% Complete</span>
          </div>
          <div className="w-full bg-[#07090e] rounded-full h-2 overflow-hidden p-0.5 border border-white/[0.08]">
            <div 
              className="bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-500 h-full rounded-full transition-all duration-500 ease-out" 
              style={{ width: `${progress}%` }} 
            />
          </div>
        </div>
      )}
    </div>
  );
};
