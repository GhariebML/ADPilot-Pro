import React from 'react';
import { 
  Play, 
  Pause, 
  ShieldCheck, 
  Download, 
  Sparkles, 
  Cpu, 
  Layers, 
  CheckCircle2, 
  AlertTriangle 
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
    <div className="w-full bg-slate-900/90 border border-slate-800/90 rounded-2xl p-4 sm:p-5 backdrop-blur-3xl shadow-2xl relative overflow-hidden mb-6">
      {/* Background Subtle Cyber Mesh */}
      <div className="absolute inset-0 bg-gradient-to-r from-blue-900/10 via-purple-900/10 to-emerald-900/10 pointer-events-none" />
      <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-cyan-500 via-blue-500 to-purple-500" />

      <div className="relative z-10 flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        {/* Left Side: Campaign Context & Metadata */}
        <div className="flex items-start sm:items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center text-white shadow-lg shadow-blue-500/20 shrink-0">
            <Cpu className="w-6 h-6 animate-pulse-slow" />
          </div>
          <div>
            <div className="flex items-center gap-2.5 flex-wrap">
              <h2 className="text-lg font-bold text-slate-100">
                {campaign?.businessName || 'AI Enterprise Growth Campaign'}
              </h2>
              <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-500/15 text-blue-400 border border-blue-500/30">
                {campaign?.productName || 'AI SaaS Platform'}
              </span>
              <span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-500/15 text-purple-300 border border-purple-500/30">
                {campaign?.duration || '30 Days'}
              </span>
              <span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-500/15 text-emerald-300 border border-emerald-500/30">
                ${campaign?.budget?.toLocaleString() || '10,000'} USD
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-1 flex items-center gap-2">
              <span>Goal: <strong className="text-slate-200">{campaign?.goals?.join(', ') || 'Lead Generation & Sales'}</strong></span>
              <span>â€¢</span>
              <span>Audience: <strong className="text-slate-200">{campaign?.targetAudience || 'B2B Mid-Market & SaaS Founders'}</strong></span>
            </p>
          </div>
        </div>

        {/* Middle: Live Pipeline Status Metrics */}
        <div className="flex items-center gap-4 sm:gap-6 bg-slate-950/60 border border-slate-800/80 rounded-xl px-4 py-2.5">
          <div>
            <div className="text-[11px] text-slate-400 font-medium uppercase tracking-wider">System State</div>
            <div className="flex items-center gap-2 mt-0.5">
              {isRunning ? (
                <span className="inline-flex items-center gap-1.5 text-xs font-semibold text-cyan-400">
                  <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
                  Running Pipeline
                </span>
              ) : isDone ? (
                <span className="inline-flex items-center gap-1.5 text-xs font-semibold text-emerald-400">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  Execution Ready
                </span>
              ) : (
                <span className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-400">
                  <span className="w-2 h-2 rounded-full bg-slate-500" />
                  Idle
                </span>
              )}
            </div>
          </div>

          <div className="h-7 w-[1px] bg-slate-800" />

          <div>
            <div className="text-[11px] text-slate-400 font-medium uppercase tracking-wider">Agents Active</div>
            <div className="flex items-center gap-1.5 mt-0.5 text-xs font-bold text-slate-100">
              <Layers className="w-3.5 h-3.5 text-purple-400" />
              <span>{isDone ? totalAgentsCount : activeAgentsCount}/{totalAgentsCount}</span>
            </div>
          </div>

          <div className="h-7 w-[1px] bg-slate-800" />

          <div>
            <div className="text-[11px] text-slate-400 font-medium uppercase tracking-wider">AI Confidence</div>
            <div className="flex items-center gap-1 mt-0.5 text-xs font-bold text-emerald-400">
              <Sparkles className="w-3.5 h-3.5" />
              <span>{confidenceScore}%</span>
            </div>
          </div>
        </div>

        {/* Right Side: Action Buttons */}
        <div className="flex items-center gap-2 flex-wrap sm:flex-nowrap">
          <button
            onClick={onOpenDemo}
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold bg-gradient-to-r from-cyan-500/20 to-blue-500/20 hover:from-cyan-500/30 hover:to-blue-500/30 text-cyan-300 border border-cyan-500/40 transition-all shadow-sm active:scale-95"
            title="Launch Interactive Step-by-Step AI Simulation Demo"
          >
            <Play className="w-3.5 h-3.5 fill-cyan-400" />
            <span>Interactive Demo</span>
          </button>

          <button
            onClick={onOpenHITL}
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold bg-amber-500/15 hover:bg-amber-500/25 text-amber-300 border border-amber-500/40 transition-all active:scale-95"
            title="Open Human-in-the-Loop Governance Gate"
          >
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>HITL Review</span>
          </button>

          <button
            onClick={onExportReport}
            className="flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-all active:scale-95"
            title="Export Intelligence Package"
          >
            <Download className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Export</span>
          </button>
        </div>
      </div>

      {/* Real-time Progress Bar */}
      {isRunning && (
        <div className="mt-4 pt-3 border-t border-slate-800/80">
          <div className="flex justify-between items-center text-xs text-slate-400 mb-1.5">
            <span className="font-mono text-cyan-400">Autonomous Execution Stream</span>
            <span className="font-mono">{progress}% Complete</span>
          </div>
          <div className="w-full bg-slate-950 rounded-full h-1.5 overflow-hidden">
            <div 
              className="bg-gradient-to-r from-cyan-500 via-blue-500 to-purple-500 h-full transition-all duration-500 ease-out" 
              style={{ width: `${progress}%` }} 
            />
          </div>
        </div>
      )}
    </div>
  );
};

