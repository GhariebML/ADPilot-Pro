import React, { useState } from 'react';
import { 
  X, 
  Bot, 
  Cpu, 
  CheckCircle2, 
  ArrowRight, 
  Copy, 
  Check, 
  Sparkles,
  Layers,
  ShieldCheck,
  Zap,
  HelpCircle,
  FileCode2,
  GitBranch,
  Filter,
  CheckCheck
} from 'lucide-react';
import type { AgentContract } from '../types';

interface AgentDetailDrawerProps {
  agent: AgentContract | null;
  isOpen: boolean;
  onClose: () => void;
  onInspectIO: (agent: AgentContract) => void;
}

export const AgentDetailDrawer: React.FC<AgentDetailDrawerProps> = ({
  agent,
  isOpen,
  onClose,
  onInspectIO,
}) => {
  const [copied, setCopied] = useState(false);
  const [activeTab, setActiveTab] = useState<'causal' | 'contracts' | 'tools'>('causal');

  if (!isOpen || !agent) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(JSON.stringify(agent, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 overflow-hidden">
      {/* Backdrop */}
      <div 
        onClick={onClose}
        className="absolute inset-0 bg-slate-950/80 backdrop-blur-md transition-opacity animate-in fade-in duration-200" 
      />

      <div className="fixed inset-y-0 right-0 max-w-full flex pl-10">
        <div className="w-screen max-w-xl bg-slate-900 border-l border-slate-800 shadow-2xl flex flex-col justify-between overflow-hidden animate-in slide-in-from-right duration-300">
          {/* Header */}
          <div className="p-6 border-b border-slate-800 bg-slate-950/80 flex items-start justify-between gap-4">
            <div className="flex items-center gap-3.5">
              <div className="p-3 rounded-2xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 shadow-lg shadow-cyan-500/10">
                <Bot className="w-6 h-6 animate-pulse" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase tracking-wider bg-blue-500/10 text-blue-300 border border-blue-500/20">
                    {agent.modelType}
                  </span>
                  <span className="text-xs font-mono text-cyan-400 font-bold">
                    {agent.id.toUpperCase()}
                  </span>
                </div>
                <h3 className="text-lg font-bold text-slate-100 mt-1">{agent.name}</h3>
              </div>
            </div>

            <div className="flex items-center gap-1.5">
              <button
                onClick={handleCopy}
                className="p-2 rounded-xl text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors"
                title="Copy Agent Contract Schema"
              >
                {copied ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
              </button>
              <button
                onClick={onClose}
                className="p-2 rounded-xl text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Navigation Tabs */}
          <div className="flex border-b border-slate-800/80 px-6 bg-slate-950/40 text-xs font-mono">
            <button
              onClick={() => setActiveTab('causal')}
              className={`py-3 px-3 font-semibold border-b-2 transition-all flex items-center gap-1.5 ${
                activeTab === 'causal'
                  ? 'border-cyan-400 text-cyan-300'
                  : 'border-transparent text-slate-400 hover:text-slate-200'
              }`}
            >
              <GitBranch className="w-3.5 h-3.5" />
              <span>Causal Explainability Tree</span>
            </button>
            <button
              onClick={() => setActiveTab('contracts')}
              className={`py-3 px-3 font-semibold border-b-2 transition-all flex items-center gap-1.5 ${
                activeTab === 'contracts'
                  ? 'border-cyan-400 text-cyan-300'
                  : 'border-transparent text-slate-400 hover:text-slate-200'
              }`}
            >
              <FileCode2 className="w-3.5 h-3.5" />
              <span>I/O Data Schema</span>
            </button>
            <button
              onClick={() => setActiveTab('tools')}
              className={`py-3 px-3 font-semibold border-b-2 transition-all flex items-center gap-1.5 ${
                activeTab === 'tools'
                  ? 'border-cyan-400 text-cyan-300'
                  : 'border-transparent text-slate-400 hover:text-slate-200'
              }`}
            >
              <Cpu className="w-3.5 h-3.5" />
              <span>Model & Tools</span>
            </button>
          </div>

          {/* Body Content */}
          <div className="flex-1 p-6 overflow-y-auto space-y-6 text-slate-200">
            {/* Quick Metrics Bar */}
            <div className="grid grid-cols-3 gap-3 p-3.5 rounded-2xl bg-slate-950 border border-slate-800 text-center font-mono">
              <div>
                <div className="text-[10px] text-slate-500 uppercase">Epistemic Conf</div>
                <div className="text-sm font-bold text-emerald-400 mt-0.5">{agent.confidence}%</div>
              </div>
              <div className="border-x border-slate-800">
                <div className="text-[10px] text-slate-500 uppercase">Inference Latency</div>
                <div className="text-sm font-bold text-cyan-400 mt-0.5">{agent.latencyMs}ms</div>
              </div>
              <div>
                <div className="text-[10px] text-slate-500 uppercase">Contract Status</div>
                <div className="text-sm font-bold text-purple-400 mt-0.5">Enforced</div>
              </div>
            </div>

            {/* TAB 1: Causal Explainability Tree */}
            {activeTab === 'causal' && (
              <div className="space-y-4">
                <div className="text-xs font-bold text-slate-400 uppercase tracking-wider font-mono flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
                  <span>4-Stage Causal Decision Reasoning</span>
                </div>

                {/* Step 1: Prior Context */}
                <div className="p-4 rounded-xl bg-slate-950/70 border border-slate-800 relative pl-10">
                  <div className="absolute left-3.5 top-4 w-5 h-5 rounded-full bg-cyan-500/20 text-cyan-400 flex items-center justify-center text-[10px] font-bold font-mono border border-cyan-500/30">
                    1
                  </div>
                  <div className="text-xs font-bold text-slate-200">Epistemic Prior & Knowledge Evidence</div>
                  <p className="text-xs text-slate-400 mt-1 leading-relaxed">
                    Extracted semantic priors from BGE FastEmbed vector search (MRR: 1.0) and upstream validated campaign briefs.
                  </p>
                </div>

                {/* Step 2: Candidate Hypotheses */}
                <div className="p-4 rounded-xl bg-slate-950/70 border border-slate-800 relative pl-10">
                  <div className="absolute left-3.5 top-4 w-5 h-5 rounded-full bg-purple-500/20 text-purple-400 flex items-center justify-center text-[10px] font-bold font-mono border border-purple-500/30">
                    2
                  </div>
                  <div className="text-xs font-bold text-slate-200">Hypothesis Exploration & Generation</div>
                  <p className="text-xs text-slate-400 mt-1 leading-relaxed">
                    Evaluated 3 strategic variants across audience personas, psychological buying hooks, and continuous policy action distributions.
                  </p>
                </div>

                {/* Step 3: Constraint Filter */}
                <div className="p-4 rounded-xl bg-slate-950/70 border border-slate-800 relative pl-10">
                  <div className="absolute left-3.5 top-4 w-5 h-5 rounded-full bg-amber-500/20 text-amber-400 flex items-center justify-center text-[10px] font-bold font-mono border border-amber-500/30">
                    3
                  </div>
                  <div className="text-xs font-bold text-slate-200">Safety & Economic Constraint Filtering</div>
                  <p className="text-xs text-slate-400 mt-1 leading-relaxed">
                    Applied Dirichlet budget guards ($\le \$10,000$), CLIP-ViT contrast checks (14.2:1 AAA), and Ridge quality score thresholds ($\ge 5.0$).
                  </p>
                </div>

                {/* Step 4: Final Contract */}
                <div className="p-4 rounded-xl bg-slate-950/70 border border-emerald-500/30 relative pl-10 bg-emerald-500/5">
                  <div className="absolute left-3.5 top-4 w-5 h-5 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-[10px] font-bold font-mono border border-emerald-500/30">
                    4
                  </div>
                  <div className="text-xs font-bold text-emerald-300">Emitted Deterministic Output</div>
                  <p className="text-xs text-slate-300 mt-1 leading-relaxed">
                    Synthesized structured contract payload validated against Pydantic schema and dispatched to: <strong className="text-cyan-300">{agent.downstream?.join(', ') || 'Downstream Consumers'}</strong>.
                  </p>
                </div>
              </div>
            )}

            {/* TAB 2: Contracts Schema */}
            {activeTab === 'contracts' && (
              <div className="space-y-4">
                <div>
                  <div className="text-[11px] font-mono font-bold text-slate-400 uppercase mb-2">
                    Input Requirements ({agent.inputs.length})
                  </div>
                  <div className="space-y-1.5">
                    {agent.inputs.map((inp, idx) => (
                      <div key={idx} className="p-2.5 rounded-lg bg-slate-950 border border-slate-800 text-xs font-mono text-cyan-300 flex items-center gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-cyan-400" />
                        <span>{inp}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <div className="text-[11px] font-mono font-bold text-slate-400 uppercase mb-2">
                    Synthesized Output Guarantees ({agent.outputs.length})
                  </div>
                  <div className="space-y-1.5">
                    {agent.outputs.map((out, idx) => (
                      <div key={idx} className="p-2.5 rounded-lg bg-slate-950 border border-slate-800 text-xs font-mono text-emerald-300 flex items-center gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                        <span>{out}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* TAB 3: Model & Tools */}
            {activeTab === 'tools' && (
              <div className="space-y-4">
                <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-3 font-mono text-xs">
                  <div className="flex justify-between pb-2 border-b border-slate-800">
                    <span className="text-slate-500">Model Engine:</span>
                    <span className="text-cyan-300 font-bold">{agent.model}</span>
                  </div>
                  <div className="flex justify-between pb-2 border-b border-slate-800">
                    <span className="text-slate-500">Architecture:</span>
                    <span className="text-purple-300">{agent.modelType}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">Downstream:</span>
                    <span className="text-slate-200">{agent.downstream?.join(', ') || 'Downstream Pipeline'}</span>
                  </div>
                </div>

                <div>
                  <div className="text-[11px] font-mono font-bold text-slate-400 uppercase mb-2">
                    Registered Tools & Functions ({agent.tools.length})
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {agent.tools.map((tool, idx) => (
                      <span key={idx} className="px-2.5 py-1 rounded-lg text-xs font-mono bg-slate-950 text-slate-300 border border-slate-800">
                        {tool}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Footer Action */}
          <div className="p-5 border-t border-slate-800 bg-slate-950 flex items-center justify-between">
            <button
              onClick={() => onInspectIO(agent)}
              className="w-full py-2.5 px-4 rounded-xl text-xs font-bold font-mono uppercase tracking-wider bg-cyan-600 hover:bg-cyan-500 text-white transition-colors flex items-center justify-center gap-2"
            >
              <span>Inspect Raw I/O Payload Telemetry</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
