import React, { useState, useEffect } from 'react';
import { 
  Play, 
  Pause, 
  RotateCcw, 
  X, 
  CheckCircle2, 
  Sparkles, 
  ArrowRight, 
  Bot, 
  Cpu, 
  ShieldCheck, 
  Zap, 
  FileText, 
  Layers 
} from 'lucide-react';
import type { AgentContract } from '../types';

interface InteractiveDemoModalProps {
  isOpen: boolean;
  onClose: () => void;
  agents: AgentContract[];
}

export const InteractiveDemoModal: React.FC<InteractiveDemoModalProps> = ({
  isOpen,
  onClose,
  agents,
}) => {
  const [currentStep, setCurrentStep] = useState<number>(0);
  const [isPlaying, setIsPlaying] = useState<boolean>(true);

  useEffect(() => {
    if (!isOpen) {
      setCurrentStep(0);
      setIsPlaying(true);
      return;
    }

    if (!isPlaying) return;

    const timer = setTimeout(() => {
      if (currentStep < agents.length - 1) {
        setCurrentStep(prev => prev + 1);
      } else {
        setIsPlaying(false);
      }
    }, 2800);

    return () => clearTimeout(timer);
  }, [isOpen, isPlaying, currentStep, agents.length]);

  if (!isOpen) return null;

  const currentAgent = agents[currentStep] || agents[0];
  const progressPct = Math.round(((currentStep + 1) / agents.length) * 100);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div 
        onClick={onClose}
        className="absolute inset-0 bg-slate-950/90 backdrop-blur-lg" 
      />

      {/* Modal Container */}
      <div className="relative z-10 w-full max-w-4xl bg-slate-900 border border-slate-800 rounded-3xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="p-5 border-b border-slate-800 flex items-center justify-between bg-slate-950/80">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/20">
              <Play className="w-5 h-5 fill-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-base font-bold text-slate-100">Live Multi-Agent Pipeline Simulation</h3>
                <span className="px-2.5 py-0.5 rounded-full text-xs font-mono font-bold bg-cyan-500/15 text-cyan-400 border border-cyan-500/30">
                  Step {currentStep + 1} of {agents.length}
                </span>
              </div>
              <p className="text-xs text-slate-400 font-mono mt-0.5">
                Autonomous B2B Enterprise SaaS Campaign Ingestion → Optimization Stream
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setIsPlaying(!isPlaying)}
              className="px-3 py-1.5 rounded-xl text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 flex items-center gap-1.5 transition-colors"
            >
              {isPlaying ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
              <span>{isPlaying ? 'Pause' : 'Play'}</span>
            </button>
            <button
              onClick={() => { setCurrentStep(0); setIsPlaying(true); }}
              className="p-2 rounded-xl text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors"
              title="Restart Simulation"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
            <button
              onClick={onClose}
              className="p-2 rounded-xl text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Multi-Node Progress Strip */}
        <div className="px-6 py-4 bg-slate-950/60 border-b border-slate-800/80 overflow-x-auto">
          <div className="flex items-center justify-between min-w-[650px] gap-2">
            {agents.map((ag, idx) => {
              const isPast = idx < currentStep;
              const isCurrent = idx === currentStep;

              return (
                <div 
                  key={ag.id} 
                  onClick={() => { setCurrentStep(idx); setIsPlaying(false); }}
                  className={`flex-1 flex flex-col items-center cursor-pointer group`}
                >
                  <div className={`w-8 h-8 rounded-xl flex items-center justify-center text-xs font-bold font-mono transition-all ${
                    isCurrent
                      ? 'bg-cyan-500 text-slate-950 shadow-lg shadow-cyan-500/40 scale-110'
                      : isPast
                      ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40'
                      : 'bg-slate-900 text-slate-500 border border-slate-800'
                  }`}>
                    {isPast ? <CheckCircle2 className="w-4 h-4" /> : String(idx + 1).padStart(2, '0')}
                  </div>
                  <span className={`text-[10px] font-mono mt-1 text-center truncate max-w-[60px] ${
                    isCurrent ? 'text-cyan-300 font-bold' : isPast ? 'text-slate-400' : 'text-slate-600'
                  }`}>
                    {ag.id}
                  </span>
                </div>
              );
            })}
          </div>

          {/* Linear Bar */}
          <div className="w-full bg-slate-900 rounded-full h-1 mt-3 overflow-hidden">
            <div 
              className="bg-gradient-to-r from-cyan-500 via-blue-500 to-purple-500 h-full transition-all duration-500"
              style={{ width: `${progressPct}%` }}
            />
          </div>
        </div>

        {/* Current Active Agent Spotlight View */}
        <div className="p-6 overflow-y-auto flex-1 bg-slate-900 space-y-6">
          <div className="bg-slate-950/90 border border-slate-800 rounded-2xl p-6 relative overflow-hidden">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800/80">
              <div className="flex items-center gap-3">
                <div className="p-3 rounded-2xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                  <Bot className="w-6 h-6 animate-pulse" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono font-bold text-cyan-400 uppercase">
                      Stage {String(currentStep + 1).padStart(2, '0')} Active
                    </span>
                    <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-blue-500/10 text-blue-300 border border-blue-500/20">
                      {currentAgent.model}
                    </span>
                  </div>
                  <h3 className="text-lg font-bold text-slate-100 mt-0.5">{currentAgent.name}</h3>
                </div>
              </div>

              <div className="flex items-center gap-3 bg-slate-900/80 border border-slate-800 rounded-xl px-4 py-2 text-xs font-mono shrink-0">
                <div>
                  <div className="text-[10px] text-slate-500 uppercase">Epistemic Conf</div>
                  <div className="text-emerald-400 font-bold">{currentAgent.confidence}%</div>
                </div>
                <div className="h-6 w-[1px] bg-slate-800" />
                <div>
                  <div className="text-[10px] text-slate-500 uppercase">Latency</div>
                  <div className="text-cyan-400 font-bold">{currentAgent.latencyMs}ms</div>
                </div>
              </div>
            </div>

            {/* Responsibility Text */}
            <div className="mt-4">
              <div className="text-[11px] font-mono text-slate-500 uppercase mb-1">Autonomous Agent Objective</div>
              <p className="text-sm text-slate-300 leading-relaxed font-sans">
                {currentAgent.responsibility}
              </p>
            </div>

            {/* Live Streaming Data Contracts (Input & Output) */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-5">
              <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4">
                <div className="text-[11px] font-mono text-emerald-400 font-bold uppercase mb-2 flex items-center justify-between">
                  <span>Input Telemetry Contract</span>
                  <span className="text-slate-500 text-[10px]">Pydantic Validated</span>
                </div>
                <pre className="text-slate-300 text-xs font-mono whitespace-pre-wrap max-h-40 overflow-y-auto leading-relaxed">
                  {JSON.stringify(currentAgent.sampleInput || {}, null, 2)}
                </pre>
              </div>

              <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4">
                <div className="text-[11px] font-mono text-cyan-400 font-bold uppercase mb-2 flex items-center justify-between">
                  <span>Synthesized Output Result</span>
                  <span className="text-slate-500 text-[10px]">Deterministic Output</span>
                </div>
                <pre className="text-slate-300 text-xs font-mono whitespace-pre-wrap max-h-40 overflow-y-auto leading-relaxed">
                  {JSON.stringify(currentAgent.sampleOutput || {}, null, 2)}
                </pre>
              </div>
            </div>
          </div>
        </div>

        {/* Footer Navigation */}
        <div className="p-4 bg-slate-950 border-t border-slate-800 flex items-center justify-between">
          <button
            onClick={() => { if (currentStep > 0) setCurrentStep(prev => prev - 1); setIsPlaying(false); }}
            disabled={currentStep === 0}
            className="px-4 py-2 rounded-xl text-xs font-semibold bg-slate-800 hover:bg-slate-700 disabled:opacity-40 text-slate-200 transition-colors"
          >
            ← Previous Stage
          </button>

          <span className="text-xs text-slate-400 font-mono">
            {currentStep === agents.length - 1 ? (
              <span className="text-emerald-400 font-bold">✓ Campaign Ready for Execution</span>
            ) : (
              <span>Next Agent: <strong className="text-cyan-400">{agents[currentStep + 1]?.name}</strong></span>
            )}
          </span>

          <button
            onClick={() => { if (currentStep < agents.length - 1) setCurrentStep(prev => prev + 1); setIsPlaying(false); }}
            disabled={currentStep === agents.length - 1}
            className="px-4 py-2 rounded-xl text-xs font-bold bg-cyan-600 hover:bg-cyan-500 disabled:opacity-40 text-white transition-colors flex items-center gap-1.5"
          >
            <span>Next Stage</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>
  );
};
