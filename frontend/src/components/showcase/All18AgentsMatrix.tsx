import React, { useState } from 'react';
import { 
  Bot, 
  Search, 
  Filter, 
  CheckCircle2, 
  ArrowRight, 
  FileCode2, 
  Terminal, 
  Sparkles, 
  Cpu, 
  Layers, 
  Zap, 
  ShieldCheck, 
  Eye, 
  BarChart3, 
  Compass, 
  FileText, 
  Palette, 
  Share2, 
  Activity, 
  Tag, 
  RefreshCw, 
  X,
  Code2,
  Check
} from 'lucide-react';
import { MASTER_AGENTS } from '../../data/agentContracts';
import type { AgentContract } from '../../types';

export const All18AgentsMatrix: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedRole, setSelectedRole] = useState<string>('ALL');
  const [selectedAgent, setSelectedAgent] = useState<AgentContract | null>(null);

  const roles = [
    { id: 'ALL', label: 'All 18 Agents', count: MASTER_AGENTS.length },
    { id: 'STRATEGY', label: 'Strategy & Research', count: MASTER_AGENTS.filter(a => ['strategy', 'research', 'audience', 'competitor'].includes(a.id)).length },
    { id: 'CREATIVE', label: 'Creative & Vision', count: MASTER_AGENTS.filter(a => ['content', 'design', 'cv', 'creative'].includes(a.id)).length },
    { id: 'OPTIMIZATION', label: 'ML, RL & Analytics', count: MASTER_AGENTS.filter(a => ['analytics', 'optimizer', 'evaluation', 'correction'].includes(a.id)).length },
    { id: 'OPERATIONS', label: 'Governance & Dispatch', count: MASTER_AGENTS.filter(a => ['hitl', 'publishing', 'monitoring', 'campaign_manager'].includes(a.id)).length },
  ];

  const filteredAgents = MASTER_AGENTS.filter(agent => {
    const matchesSearch = searchQuery === '' || 
      agent.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      agent.role.toLowerCase().includes(searchQuery.toLowerCase()) ||
      agent.model.toLowerCase().includes(searchQuery.toLowerCase());
    
    let matchesRole = true;
    if (selectedRole === 'STRATEGY') {
      matchesRole = ['strategy', 'research', 'audience', 'competitor', 'product_classifier', 'planner'].includes(agent.id);
    } else if (selectedRole === 'CREATIVE') {
      matchesRole = ['content', 'design', 'cv', 'creative'].includes(agent.id);
    } else if (selectedRole === 'OPTIMIZATION') {
      matchesRole = ['analytics', 'optimizer', 'evaluation', 'correction', 'debate'].includes(agent.id);
    } else if (selectedRole === 'OPERATIONS') {
      matchesRole = ['hitl', 'publishing', 'monitoring', 'campaign_manager'].includes(agent.id);
    }

    return matchesSearch && matchesRole;
  });

  return (
    <div className="w-full bg-slate-950/40 border border-slate-800/60 shadow-2xl rounded-2xl p-6 backdrop-blur-2xl space-y-6 shadow-2xl relative overflow-hidden">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800/80 pb-4">
        <div>
          <div className="flex items-center gap-2.5">
            <span className="p-2 rounded-xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
              <Bot className="w-5 h-5" />
            </span>
            <h3 className="text-lg font-bold text-white font-mono uppercase tracking-wider">
              18-Stage Master Agent Fleet & Contract Matrix
            </h3>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Every agent operates under strict immutable Pydantic v2 schemas with dedicated neural backbones and zero string passing.
          </p>
        </div>

        {/* Quick Filter Tabs */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1">
          {roles.map(r => (
            <button
              key={r.id}
              onClick={() => setSelectedRole(r.id)}
              className={`px-3 py-1.5 rounded-xl text-xs font-mono font-semibold whitespace-nowrap transition-all ${
                selectedRole === r.id
                  ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/50 shadow-sm'
                  : 'bg-slate-900 border border-slate-800 text-slate-400 hover:text-white'
              }`}
            >
              {r.label} ({r.count})
            </button>
          ))}
        </div>
      </div>

      {/* Search Input */}
      <div className="relative w-full">
        <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search all 18 agents by name, model (GPT-4o, Claude 3.5, PyTorch PPO), or role..."
          className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-100 placeholder:text-slate-500 focus:outline-none focus:border-cyan-500 font-mono"
        />
      </div>

      {/* Agents Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredAgents.map((agent, idx) => (
          <div
            key={agent.id}
            onClick={() => setSelectedAgent(agent)}
            className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-cyan-500/50 hover:bg-slate-900/90 transition-all cursor-pointer group flex flex-col justify-between space-y-4"
          >
            <div>
              <div className="flex items-center justify-between gap-2 mb-2">
                <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-slate-950 text-cyan-400 border border-slate-800">
                  STAGE {String(idx + 1).padStart(2, '0')}
                </span>
                <span className="flex items-center gap-1 text-[10px] font-mono font-bold text-emerald-400 px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/20">
                  <CheckCircle2 className="w-3 h-3" />
                  {agent.modelType}
                </span>
              </div>

              <h4 className="text-sm font-bold text-white group-hover:text-cyan-300 transition-colors">
                {agent.name}
              </h4>
              <p className="text-xs text-slate-400 font-mono mt-0.5 line-clamp-1">{agent.role}</p>

              <div className="mt-3 pt-3 border-t border-slate-800/80 space-y-1 font-mono text-[11px]">
                <div className="text-slate-400">
                  <span className="text-slate-500">Engine:</span> <strong className="text-purple-300">{agent.model}</strong>
                </div>
                <div className="text-slate-400">
                  <span className="text-slate-500">Latency:</span> <strong className="text-cyan-400">{agent.latencyMs}ms</strong>
                </div>
              </div>
            </div>

            <div className="pt-2 border-t border-slate-800/60 flex items-center justify-between text-[10px] font-mono text-slate-500">
              <span className="truncate max-w-[160px]">Out: {agent.outputs.join(', ')}</span>
              <span className="text-cyan-400 flex items-center gap-1 group-hover:underline shrink-0">
                <span>View Specs</span>
                <ArrowRight className="w-3 h-3" />
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* â”€â”€ Slide-Over Agent Contract Drawer â”€â”€ */}
      {selectedAgent && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-md z-50 flex items-center justify-center p-4">
          <div className="bg-slate-950 border border-slate-800 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto p-6 space-y-5 shadow-2xl relative font-sans">
            <button
              onClick={() => setSelectedAgent(null)}
              className="absolute top-5 right-5 p-2 rounded-xl bg-slate-900 text-slate-400 hover:text-white border border-slate-800"
            >
              <X className="w-4 h-4" />
            </button>

            {/* Drawer Header */}
            <div>
              <div className="flex items-center gap-2 mb-1 font-mono">
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-cyan-500/10 text-cyan-300 border border-cyan-500/30">
                  {selectedAgent.modelType}
                </span>
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 flex items-center gap-1">
                  <CheckCircle2 className="w-3 h-3" /> Active Contract
                </span>
              </div>
              <h2 className="text-xl font-bold text-white">{selectedAgent.name}</h2>
              <div className="text-xs text-slate-400 font-mono mt-0.5">{selectedAgent.role}</div>
            </div>

            {/* Specs Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs font-mono">
              <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
                <span className="text-slate-500 block text-[10px] uppercase">Engine Backbone</span>
                <span className="text-purple-300 font-bold">{selectedAgent.model}</span>
              </div>
              <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
                <span className="text-slate-500 block text-[10px] uppercase">Execution Latency</span>
                <span className="text-cyan-400 font-bold">{selectedAgent.latencyMs}ms</span>
              </div>
              <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
                <span className="text-slate-500 block text-[10px] uppercase">Input Data Contracts</span>
                <span className="text-slate-200">{selectedAgent.inputs.join(', ')}</span>
              </div>
              <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
                <span className="text-slate-500 block text-[10px] uppercase">Output Data Contracts</span>
                <span className="text-emerald-400 font-bold">{selectedAgent.outputs.join(', ')}</span>
              </div>
            </div>

            {/* Responsibility Summary */}
            <div className="p-4 rounded-xl bg-slate-900/70 border border-slate-800 text-xs text-slate-300 leading-relaxed font-mono">
              <span className="text-slate-500 block text-[10px] uppercase mb-1">Responsibility:</span>
              {selectedAgent.responsibility}
            </div>

            {/* Downstream Consumers */}
            <div>
              <h4 className="text-xs font-bold font-mono text-slate-400 uppercase tracking-wider mb-2">Downstream Consumers</h4>
              <div className="flex flex-wrap gap-1.5">
                {selectedAgent.downstream.map((down, idx) => (
                  <span key={idx} className="px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 text-[11px] font-mono text-cyan-300">
                    {down}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default All18AgentsMatrix;

