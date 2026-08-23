import React, { useState } from 'react';
import { 
  Compass, 
  Search, 
  Target, 
  FileText, 
  Palette, 
  Eye, 
  BarChart3, 
  Zap, 
  Wrench, 
  ShieldCheck, 
  Send, 
  Activity, 
  CheckCircle2, 
  Loader2, 
  ArrowRight,
  Info,
  Layers,
  GitBranch,
  Filter
} from 'lucide-react';
import type { AgentContract } from '../types';

interface InteractivePipelineDAGProps {
  agents: AgentContract[];
  activeAgentId?: string | null;
  onSelectAgent: (agent: AgentContract) => void;
  onInspectIO: (agent: AgentContract) => void;
  isRunning?: boolean;
}

const getAgentIcon = (id: string) => {
  switch (id) {
    case 'strategy': return <Compass className="w-4 h-4 text-cyan-400" />;
    case 'research': return <Search className="w-4 h-4 text-emerald-400" />;
    case 'competitor': return <Target className="w-4 h-4 text-amber-400" />;
    case 'content': return <FileText className="w-4 h-4 text-purple-400" />;
    case 'design': return <Palette className="w-4 h-4 text-pink-400" />;
    case 'cv': return <Eye className="w-4 h-4 text-indigo-400" />;
    case 'analytics': return <BarChart3 className="w-4 h-4 text-blue-400" />;
    case 'optimizer': return <Zap className="w-4 h-4 text-amber-400" />;
    case 'correction': return <Wrench className="w-4 h-4 text-orange-400" />;
    case 'hitl': return <ShieldCheck className="w-4 h-4 text-rose-400" />;
    case 'publishing': return <Send className="w-4 h-4 text-emerald-400" />;
    case 'monitoring': return <Activity className="w-4 h-4 text-cyan-400" />;
    case 'classifier': return <Layers className="w-4 h-4 text-cyan-400" />;
    case 'planner': return <GitBranch className="w-4 h-4 text-blue-400" />;
    default: return <Layers className="w-4 h-4 text-blue-400" />;
  }
};

const getModelBadgeColor = (type: AgentContract['modelType']) => {
  switch (type) {
    case 'LLM': return 'bg-cyan-500/15 text-cyan-300 border-cyan-500/40';
    case 'RL Neural Policy': return 'bg-amber-500/15 text-amber-300 border-amber-500/40';
    case 'Classical ML': return 'bg-blue-500/15 text-blue-300 border-blue-500/40';
    case 'Computer Vision': return 'bg-pink-500/15 text-pink-300 border-pink-500/40';
    case 'Vector Embeddings': return 'bg-emerald-500/15 text-emerald-300 border-emerald-500/40';
    default: return 'bg-slate-500/15 text-slate-300 border-slate-500/40';
  }
};

export const InteractivePipelineDAG: React.FC<InteractivePipelineDAGProps> = ({
  agents,
  activeAgentId,
  onSelectAgent,
  onInspectIO,
  isRunning = false,
}) => {
  const [filterCategory, setFilterCategory] = useState<string>('all');

  const categories = [
    { id: 'all', label: 'All 18 Stages' },
    { id: 'strategy', label: 'Strategy & Intel (1-7)' },
    { id: 'creative', label: 'Creative & CV (8-10)' },
    { id: 'ml_rl', label: 'Analytics & RL (11-13)' },
    { id: 'governance', label: 'HITL & Dispatch (14-18)' },
  ];

  const filteredAgents = agents.filter((ag, idx) => {
    if (filterCategory === 'all') return true;
    if (filterCategory === 'strategy') return idx < 7;
    if (filterCategory === 'creative') return idx >= 7 && idx < 10;
    if (filterCategory === 'ml_rl') return idx >= 10 && idx < 13;
    if (filterCategory === 'governance') return idx >= 13;
    return true;
  });

  return (
    <div className="w-full glass-panel-elevated rounded-2xl p-5 sm:p-6 shadow-2xl relative overflow-hidden">
      {/* Background Subtle Gradient */}
      <div className="absolute top-0 right-0 w-96 h-96 bg-cyan-500/10 rounded-full filter blur-[120px] pointer-events-none" />

      {/* Header Info */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-5 mb-5 border-b border-white/[0.08]">
        <div>
          <div className="flex items-center gap-2.5 flex-wrap">
            <h3 className="text-base font-black text-slate-100 flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-pulse" />
              Autonomous Master Pipeline (DAG 3.0)
            </h3>
            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold bg-cyan-500/15 text-cyan-300 border border-cyan-500/30">
              18 Sequential Stages
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Deterministic Pydantic contract graph with epistemic confidence scoring and zero-hallucination verification.
          </p>
        </div>

        {/* Live Legend */}
        <div className="flex items-center gap-3 text-xs font-mono text-slate-400 shrink-0">
          <span className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-400" /> Complete
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" /> Active
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-rose-400" /> Human Gate
          </span>
        </div>
      </div>

      {/* Category Filter Pills */}
      <div className="flex items-center gap-2 mb-5 overflow-x-auto pb-1">
        <Filter className="w-3.5 h-3.5 text-slate-500 shrink-0 hidden sm:inline" />
        {categories.map((cat) => (
          <button
            key={cat.id}
            onClick={() => setFilterCategory(cat.id)}
            className={`px-3 py-1 rounded-xl text-xs font-mono font-semibold transition-all shrink-0 ${
              filterCategory === cat.id
                ? 'bg-gradient-to-r from-cyan-500/30 to-blue-500/30 text-cyan-300 border border-cyan-400 shadow-sm'
                : 'bg-[#07090e]/80 text-slate-400 border border-white/[0.08] hover:text-slate-200 hover:border-white/[0.15]'
            }`}
          >
            {cat.label}
          </button>
        ))}
      </div>

      {/* Responsive Node Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-3.5 relative">
        {filteredAgents.map((agent, index) => {
          const isSelected = activeAgentId === agent.id;
          const isHITL = agent.id === 'hitl';

          return (
            <div
              key={agent.id}
              onClick={() => onSelectAgent(agent)}
              className={`p-4 rounded-xl border transition-all duration-200 cursor-pointer flex flex-col justify-between relative overflow-hidden group ${
                isSelected
                  ? 'bg-gradient-to-b from-slate-900/95 to-slate-950/95 border-cyan-400 shadow-xl shadow-cyan-500/20 scale-[1.02]'
                  : 'bg-[#07090e]/85 border-white/[0.08] hover:border-cyan-500/40 hover:bg-white/[0.03]'
              }`}
            >
              {/* Top Accent Line */}
              <div 
                className={`absolute top-0 left-0 right-0 h-[2.5px] ${
                  isHITL
                    ? 'bg-gradient-to-r from-rose-500 via-amber-500 to-rose-500'
                    : agent.status === 'completed'
                    ? 'bg-gradient-to-r from-emerald-400 to-cyan-400'
                    : 'bg-gradient-to-r from-cyan-400 to-blue-500'
                }`} 
              />

              <div>
                {/* Node Header */}
                <div className="flex items-start justify-between gap-2 mb-2">
                  <div className="flex items-center gap-2">
                    <div className="p-1.5 rounded-lg bg-slate-900/90 border border-white/[0.08] group-hover:border-cyan-500/40 transition-colors">
                      {getAgentIcon(agent.id)}
                    </div>
                    <span className="text-[10px] font-mono font-bold text-slate-400 uppercase tracking-wider">
                      Stage {String(index + 1).padStart(2, '0')}
                    </span>
                  </div>

                  {agent.status === 'completed' ? (
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                  ) : isRunning ? (
                    <Loader2 className="w-3.5 h-3.5 text-cyan-400 animate-spin shrink-0" />
                  ) : (
                    <span className="w-2 h-2 rounded-full bg-slate-600 shrink-0" />
                  )}
                </div>

                {/* Agent Name */}
                <h4 className="text-xs font-bold text-slate-100 group-hover:text-cyan-300 transition-colors leading-snug mb-1.5">
                  {agent.name}
                </h4>

                {/* Model Tag */}
                <div className="mb-2">
                  <span className={`inline-block px-2 py-0.5 rounded text-[10px] font-mono font-semibold border leading-tight ${getModelBadgeColor(agent.modelType)}`}>
                    {agent.model}
                  </span>
                </div>

                {/* Role Snippet */}
                <p className="text-[11px] text-slate-400 leading-relaxed line-clamp-2 mb-3">
                  {agent.role}
                </p>
              </div>

              {/* Card Footer: Metrics & Action */}
              <div className="pt-2.5 border-t border-white/[0.08] space-y-2">
                <div className="flex items-center justify-between text-[10px] font-mono">
                  <span className="text-emerald-400 font-bold">{agent.confidence}% Conf</span>
                  <span className="text-slate-400 font-semibold">{agent.latencyMs}ms</span>
                </div>

                <div className="flex items-center justify-between pt-1">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onInspectIO(agent);
                    }}
                    className="text-[10px] font-bold text-cyan-400 hover:text-cyan-300 flex items-center gap-1 hover:underline font-mono"
                  >
                    <Info className="w-3 h-3" />
                    <span>Inspect I/O</span>
                  </button>
                  <span className="text-[10px] text-slate-500 flex items-center gap-0.5 font-mono">
                    Next <ArrowRight className="w-2.5 h-2.5" />
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
