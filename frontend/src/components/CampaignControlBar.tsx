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
    <div className="w-full glass-panel-elevated rounded-2xl p-3.5 sm:p-5 shadow-2xl relative overflow-hidden mb-5 sm:mb-6">
      {/* Background Subtle Cyber Mesh & Top Glowing Border */}
      <div className="absolute inset-0 bg-gradient-to-r from-cyan-900/10 via-blue-900/10 to-purple-900/10 pointer-events-none" />
      <div className="absolute top-0 left-0 right-0 h-[2.5px] bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-500" />

      <div className="relative z-10 flex flex-col xl:flex-row xl:items-center justify-between gap-4">
        {/* Left Side: Campaign Context & Metadata */}
        <div className="flex items-start sm:items-center gap-3 sm:gap-4 min-w-0">
          <div className="w-10 h-10 sm:w-11 sm:h-11 rounded-xl bg-gradient-to-br from-cyan-500/25 to-blue-600/25 border border-cyan-500/40 flex items-center justify-center text-cyan-300 shadow-lg shadow-cyan-500/20 shrink-0">
            <Cpu className="w-5 h-5 animate-pulse-slow" />
          </div>
          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-1.5 sm:gap-2 flex-wrap">
              <h2 className="text-sm sm:text-base font-black text-slate-100 truncate max-w-full">
                {campaign?.businessName || 'AI Enterprise Growth Campaign'}
              </h2>
              <span className="px-2 py-0.5 rounded-full text-[10px] sm:text-xs font-mono font-bold bg-cyan-500/15 text-cyan-300 border border-cyan-500/30 shrink-0">
                {campaign?.productName || 'AI SaaS Platform'}
              </span>
              <span className="px-2 py-0.5 rounded-full text-[10px] sm:text-xs font-mono font-medium bg-purple-500/15 text-purple-300 border border-purple-500/30 shrink-0">
                {campaign?.duration || '30 Days'}
              </span>
              <span className="px-2 py-0.5 rounded-full text-[10px] sm:text-xs font-mono font-bold bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 shrink-0">
                ${campaign?.budget?.toLocaleString() || '10,000'} USD
              </span>
            </div>
            <p className="text-[11px] sm:text-xs text-slate-400 mt-1 flex items-center gap-2 font-sans flex-wrap">
              <span>Goal: <strong className="text-slate-200">{campaign?.goals?.join(', ') || 'Lead Generation & Sales'}</strong></span>
              <span className="text-slate-600 hidden sm:inline">•</span>
              <span className="truncate max-w-xs">Audience: <strong className="text-slate-200">{campaign?.targetAudience || 'B2B Mid-Market & SaaS'}</strong></span>
            </p>
          </div>
        </div>

        {/* Middle & Right: Live Metrics & Action Controls */}
        <div className="flex flex-col sm:flex-row sm:items-center gap-3 sm:gap-4 shrink-0">
          {/* Metrics Pills: 3-column on mobile, flex on tablet/laptop */}
          <div className="grid grid-cols-3 sm:flex sm:items-center gap-2 sm:gap-4 bg-[#07090e]/90 border border-white/[0.08] rounded-xl p-2.5 sm:px-4 sm:py-2 shrink-0 shadow-inner">
            <div className="text-center sm:text-left">
              <div className="text-[9px] sm:text-[10px] text-slate-400 font-mono font-bold uppercase tracking-wider">Status</div>
              <div className="flex items-center justify-center sm:justify-start gap-1.5 mt-0.5">
                {isRunning ? (
                  <span className="inline-flex items-center gap-1 text-[11px] sm:text-xs font-bold text-cyan-300 font-mono">
                    <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-ping" />
                    Running
                  </span>
                ) : isDone ? (
                  <span className="inline-flex items-center gap-1 text-[11px] sm:text-xs font-bold text-emerald-400 font-mono">
                    <CheckCircle2 className="w-3 h-3" />
                    Ready
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-1 text-[11px] sm:text-xs font-semibold text-slate-400 font-mono">
                    <span className="w-1.5 h-1.5 rounded-full bg-slate-500" />
                    Idle
                  </span>
                )}
              </div>
            </div>

            <div className="hidden sm:block h-6 w-[1px] bg-white/[0.08]" />

            <div className="text-center sm:text-left border-x border-white/[0.08] sm:border-0 px-1">
              <div className="text-[9px] sm:text-[10px] text-slate-400 font-mono font-bold uppercase tracking-wider">Fleet</div>
              <div className="flex items-center justify-center sm:justify-start gap-1 mt-0.5 text-[11px] sm:text-xs font-bold text-slate-100 font-mono">
                <Layers className="w-3 h-3 text-purple-400 shrink-0" />
                <span>{isDone ? totalAgentsCount : activeAgentsCount}/{totalAgentsCount}</span>
              </div>
            </div>

            <div className="hidden sm:block h-6 w-[1px] bg-white/[0.08]" />

            <div className="text-center sm:text-left">
              <div className="text-[9px] sm:text-[10px] text-slate-400 font-mono font-bold uppercase tracking-wider">Confidence</div>
              <div className="flex items-center justify-center sm:justify-start gap-1 mt-0.5 text-[11px] sm:text-xs font-bold text-emerald-400 font-mono">
                <Sparkles className="w-3 h-3 shrink-0" />
                <span>{confidenceScore}%</span>
              </div>
            </div>
          </div>

          {/* Right Side: Action Buttons */}
          <div className="grid grid-cols-2 sm:flex sm:items-center gap-2">
            <button
              onClick={onOpenDemo}
              className="flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl text-xs font-semibold font-mono bg-gradient-to-r from-cyan-500/20 to-blue-500/20 hover:from-cyan-500/30 hover:to-blue-500/30 text-cyan-300 border border-cyan-500/40 transition-all shadow-sm active:scale-95 min-h-[38px]"
              title="Launch Interactive AI Simulation Demo"
            >
              <Play className="w-3.5 h-3.5 fill-cyan-400 shrink-0" />
              <span>Demo</span>
            </button>

            <button
              onClick={onOpenHITL}
              className="flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl text-xs font-semibold font-mono bg-amber-500/15 hover:bg-amber-500/25 text-amber-300 border border-amber-500/40 transition-all active:scale-95 min-h-[38px]"
              title="Open Human-in-the-Loop Governance Gate"
            >
              <ShieldCheck className="w-3.5 h-3.5 shrink-0" />
              <span>HITL Gate</span>
            </button>

            <button
              onClick={onExportReport}
              className="col-span-2 sm:col-span-1 flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl text-xs font-mono font-semibold bg-[#07090e] hover:bg-slate-800 text-slate-200 border border-white/[0.08] transition-all active:scale-95 min-h-[38px]"
              title="Export Intelligence Package"
            >
              <Download className="w-3.5 h-3.5 shrink-0" />
              <span>Export Package</span>
            </button>
          </div>
        </div>
      </div>

      {/* Real-time Progress Bar */}
      {isRunning && (
        <div className="mt-3.5 pt-3 border-t border-white/[0.08]">
          <div className="flex justify-between items-center text-xs text-slate-400 mb-1.5">
            <span className="font-mono text-cyan-400 font-bold flex items-center gap-1.5 text-[11px] sm:text-xs">
              <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" /> Autonomous Execution Stream
            </span>
            <span className="font-mono font-bold text-slate-200 text-[11px] sm:text-xs">{progress}% Complete</span>
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
