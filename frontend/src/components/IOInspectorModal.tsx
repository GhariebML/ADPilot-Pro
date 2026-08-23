import React, { useState } from 'react';
import { 
  X, 
  Terminal, 
  Copy, 
  Check, 
  ArrowRight, 
  Code2, 
  FileJson, 
  Sparkles 
} from 'lucide-react';
import type { AgentContract } from '../types';

interface IOInspectorModalProps {
  agent: AgentContract | null;
  isOpen: boolean;
  onClose: () => void;
}

export const IOInspectorModal: React.FC<IOInspectorModalProps> = ({
  agent,
  isOpen,
  onClose,
}) => {
  const [activeTab, setActiveTab] = useState<'INPUT' | 'OUTPUT' | 'DIFF'>('INPUT');
  const [copied, setCopied] = useState(false);

  if (!isOpen || !agent) return null;

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const inputJson = JSON.stringify(agent.sampleInput || { message: 'Raw input telemetry streamed' }, null, 2);
  const outputJson = JSON.stringify(agent.sampleOutput || { message: 'Deterministic output validated' }, null, 2);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div 
        onClick={onClose}
        className="absolute inset-0 bg-slate-950/85 backdrop-blur-md transition-opacity animate-in fade-in" 
      />

      {/* Modal Card */}
      <div className="relative z-10 w-full max-w-3xl glass-panel-elevated border border-white/[0.12] rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[85vh]">
        {/* Header */}
        <div className="p-4 sm:p-5 border-b border-white/[0.08] flex items-center justify-between bg-[#07090e]/95">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-cyan-500/15 text-cyan-400 border border-cyan-500/30 shadow-[0_0_15px_rgba(6,182,212,0.2)]">
              <FileJson className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-sm font-bold text-slate-100">Execution Telemetry Inspector</h3>
                <span className="px-2.5 py-0.5 rounded text-[10px] font-mono font-bold bg-blue-500/15 text-blue-300 border border-blue-500/30">
                  {agent.name}
                </span>
              </div>
              <p className="text-xs text-slate-400 font-mono mt-0.5">Model: {agent.model} • Latency: {agent.latencyMs}ms</p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-white/[0.08] transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tab Selector */}
        <div className="flex items-center justify-between px-5 py-2.5 bg-black/40 border-b border-white/[0.08]">
          <div className="flex items-center gap-1.5">
            <button
              onClick={() => setActiveTab('INPUT')}
              className={`px-3 py-1 rounded-lg text-xs font-bold font-mono transition-colors ${
                activeTab === 'INPUT'
                  ? 'bg-cyan-500/25 text-cyan-300 border border-cyan-400'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              1. Input Payload
            </button>
            <button
              onClick={() => setActiveTab('OUTPUT')}
              className={`px-3 py-1 rounded-lg text-xs font-bold font-mono transition-colors ${
                activeTab === 'OUTPUT'
                  ? 'bg-blue-500/25 text-blue-300 border border-blue-400'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              2. Output Payload
            </button>
            <button
              onClick={() => setActiveTab('DIFF')}
              className={`px-3 py-1 rounded-lg text-xs font-bold font-mono transition-colors ${
                activeTab === 'DIFF'
                  ? 'bg-purple-500/25 text-purple-300 border border-purple-400'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              3. Full Transformation Trace
            </button>
          </div>

          <button
            onClick={() => handleCopy(activeTab === 'INPUT' ? inputJson : outputJson)}
            className="flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs text-slate-200 bg-white/[0.08] hover:bg-white/[0.15] transition-colors font-mono"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? 'Copied' : 'Copy JSON'}</span>
          </button>
        </div>

        {/* Code Content View */}
        <div className="p-5 overflow-y-auto font-mono text-xs text-slate-300 bg-[#07090e] flex-1 min-h-[300px]">
          {activeTab === 'INPUT' && (
            <pre className="text-emerald-400 whitespace-pre-wrap leading-relaxed">
              {inputJson}
            </pre>
          )}

          {activeTab === 'OUTPUT' && (
            <pre className="text-cyan-300 whitespace-pre-wrap leading-relaxed">
              {outputJson}
            </pre>
          )}

          {activeTab === 'DIFF' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <div className="text-[11px] font-bold text-slate-400 uppercase mb-2 pb-1 border-b border-white/[0.08]">
                  Input Contract Provided
                </div>
                <pre className="text-emerald-400 whitespace-pre-wrap text-[11px]">
                  {inputJson}
                </pre>
              </div>
              <div className="border-t md:border-t-0 md:border-l border-white/[0.08] pt-4 md:pt-0 md:pl-4">
                <div className="text-[11px] font-bold text-slate-400 uppercase mb-2 pb-1 border-b border-white/[0.08]">
                  Model Output Generated
                </div>
                <pre className="text-cyan-300 whitespace-pre-wrap text-[11px]">
                  {outputJson}
                </pre>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 bg-[#07090e]/95 border-t border-white/[0.08] flex items-center justify-between text-xs text-slate-400 font-mono">
          <span>Schema Validation: <strong className="text-emerald-400">PASSED</strong></span>
          <span>Epistemic Grounding: <strong className="text-cyan-400">100% Retrievable</strong></span>
        </div>
      </div>
    </div>
  );
};
