import React, { useState } from 'react';
import { 
  Bot, 
  Cpu, 
  Search, 
  CheckCircle2, 
  Terminal, 
  Filter,
  ShieldCheck,
  Zap
} from 'lucide-react';
import type { AgentContract } from '../types';

interface AgentObservatoryProps {
  agents: AgentContract[];
  onSelectAgent: (agent: AgentContract) => void;
  onInspectIO: (agent: AgentContract) => void;
}

export const AgentObservatory: React.FC<AgentObservatoryProps> = ({
  agents,
  onSelectAgent,
  onInspectIO,
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedFilter, setSelectedFilter] = useState<'ALL' | 'LLM' | 'ML' | 'RL' | 'VISION'>('ALL');

  const filteredAgents = agents.filter(agent => {
    const matchesSearch = 
      agent.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      agent.role.toLowerCase().includes(searchTerm.toLowerCase()) ||
      agent.model.toLowerCase().includes(searchTerm.toLowerCase());

    if (selectedFilter === 'ALL') return matchesSearch;
    if (selectedFilter === 'LLM') return matchesSearch && agent.modelType === 'LLM';
    if (selectedFilter === 'ML') return matchesSearch && agent.modelType === 'Classical ML';
    if (selectedFilter === 'RL') return matchesSearch && agent.modelType === 'RL Neural Policy';
    if (selectedFilter === 'VISION') return matchesSearch && agent.modelType === 'Computer Vision';
    return matchesSearch;
  });

  return (
    <div className="w-full space-y-6">
      {/* Header Banner */}
      <div className="glass-panel-elevated rounded-2xl p-6 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl pointer-events-none" />
        
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-3">
              <span className="p-2.5 rounded-xl bg-gradient-to-br from-cyan-500 via-blue-600 to-indigo-600 text-white shadow-lg shadow-cyan-500/20">
                <Bot className="w-5 h-5" />
              </span>
              <div>
                <h2 className="text-xl font-black text-slate-100 flex items-center gap-2">
                  AI Agent Center & Contract Observatory
                  <span className="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-cyan-500/15 text-cyan-300 border border-cyan-500/30">
                    Epistemic Contracts
                  </span>
                </h2>
                <p className="text-xs text-slate-400 mt-0.5 max-w-2xl">
                  Every agent operates under deterministic Pydantic v2 schemas, explicit data provenance, and dedicated neural policy models.
                </p>
              </div>
            </div>
          </div>

          {/* Quick Stats Pill */}
          <div className="flex items-center gap-4 bg-[#07090e]/90 border border-white/[0.08] rounded-xl px-4 py-2.5 shrink-0 shadow-inner">
            <div>
              <div className="text-[10px] uppercase font-mono text-slate-400">Registered Agents</div>
              <div className="text-sm font-bold text-slate-100 font-mono">{agents.length} Active</div>
            </div>
            <div className="h-6 w-[1px] bg-white/[0.08]" />
            <div>
              <div className="text-[10px] uppercase font-mono text-slate-400">Pipeline Integrity</div>
              <div className="text-sm font-bold text-emerald-400 flex items-center gap-1 font-mono">
                <CheckCircle2 className="w-3.5 h-3.5" /> 100% Certified
              </div>
            </div>
          </div>
        </div>

        {/* Filter & Search Bar */}
        <div className="mt-6 pt-5 border-t border-white/[0.08] flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="relative w-full sm:w-80">
            <Search className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search agent, model or responsibility..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-[#07090e]/90 border border-white/[0.08] rounded-xl pl-9 pr-3 py-2 text-xs text-slate-200 placeholder:text-slate-500 focus:outline-none focus:border-cyan-400 transition-colors shadow-inner"
            />
          </div>

          <div className="flex items-center gap-1.5 w-full sm:w-auto overflow-x-auto pb-1 sm:pb-0">
            <Filter className="w-3.5 h-3.5 text-slate-500 mr-1 hidden sm:inline" />
            {(['ALL', 'LLM', 'ML', 'RL', 'VISION'] as const).map(filter => (
              <button
                key={filter}
                onClick={() => setSelectedFilter(filter)}
                className={`px-3 py-1.5 rounded-lg text-xs font-mono font-bold transition-all shrink-0 ${
                  selectedFilter === filter
                    ? 'bg-gradient-to-r from-cyan-500/25 to-blue-500/25 text-cyan-300 border border-cyan-400 shadow-sm'
                    : 'bg-[#07090e]/80 text-slate-400 border border-white/[0.08] hover:text-slate-200 hover:border-white/[0.15]'
                }`}
              >
                {filter}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Agents Table / Grid */}
      <div className="glass-panel-elevated rounded-2xl overflow-hidden shadow-2xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-[#07090e]/90 border-b border-white/[0.08] text-[11px] font-mono text-slate-400 uppercase tracking-wider">
              <tr>
                <th className="py-3.5 px-4">Agent Name & Role</th>
                <th className="py-3.5 px-4">Model Architecture</th>
                <th className="py-3.5 px-4">Contract Inputs</th>
                <th className="py-3.5 px-4">Contract Outputs</th>
                <th className="py-3.5 px-4">Tools & RAG</th>
                <th className="py-3.5 px-4 text-right">Confidence / Latency</th>
                <th className="py-3.5 px-4 text-center">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/[0.06]">
              {filteredAgents.map((agent) => (
                <tr 
                  key={agent.id}
                  onClick={() => onSelectAgent(agent)}
                  className="hover:bg-white/[0.03] transition-colors cursor-pointer group"
                >
                  {/* Name & Role */}
                  <td className="py-4 px-4">
                    <div className="flex items-start gap-3">
                      <div className="p-2 rounded-lg bg-slate-950 border border-white/[0.08] group-hover:border-cyan-400/50 transition-colors shrink-0 text-cyan-400">
                        <Cpu className="w-4 h-4" />
                      </div>
                      <div>
                        <div className="font-bold text-slate-100 group-hover:text-cyan-300 transition-colors">
                          {agent.name}
                        </div>
                        <div className="text-[11px] text-slate-400 line-clamp-1 mt-0.5">
                          {agent.role}
                        </div>
                      </div>
                    </div>
                  </td>

                  {/* Model */}
                  <td className="py-4 px-4">
                    <span className="inline-block px-2.5 py-1 rounded-md text-[11px] font-semibold bg-[#07090e] text-slate-200 border border-white/[0.08] font-mono">
                      {agent.model}
                    </span>
                  </td>

                  {/* Inputs */}
                  <td className="py-4 px-4">
                    <div className="flex flex-wrap gap-1 max-w-xs">
                      {agent.inputs.map((inp, idx) => (
                        <span key={idx} className="px-1.5 py-0.5 rounded text-[10px] bg-[#07090e] text-slate-300 border border-white/[0.08] font-mono">
                          {inp}
                        </span>
                      ))}
                    </div>
                  </td>

                  {/* Outputs */}
                  <td className="py-4 px-4">
                    <div className="flex flex-wrap gap-1 max-w-xs">
                      {agent.outputs.map((out, idx) => (
                        <span key={idx} className="px-1.5 py-0.5 rounded text-[10px] bg-cyan-500/10 text-cyan-300 border border-cyan-500/20 font-mono">
                          {out}
                        </span>
                      ))}
                    </div>
                  </td>

                  {/* Tools */}
                  <td className="py-4 px-4">
                    <div className="flex flex-wrap gap-1 max-w-xs">
                      {agent.tools.map((t, idx) => (
                        <span key={idx} className="px-1.5 py-0.5 rounded text-[10px] bg-purple-500/10 text-purple-300 border border-purple-500/20 font-mono">
                          {t}
                        </span>
                      ))}
                    </div>
                  </td>

                  {/* Confidence / Latency */}
                  <td className="py-4 px-4 text-right">
                    <div className="font-bold text-emerald-400 font-mono">
                      {agent.confidence}%
                    </div>
                    <div className="text-[10px] text-slate-400 font-mono">
                      {agent.latencyMs}ms
                    </div>
                  </td>

                  {/* Actions */}
                  <td className="py-4 px-4 text-center">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onInspectIO(agent);
                      }}
                      className="p-2 rounded-lg bg-[#07090e] hover:bg-cyan-500/20 text-slate-400 hover:text-cyan-300 border border-white/[0.08] hover:border-cyan-400/40 transition-all"
                      title="Inspect Raw Input / Output JSON"
                    >
                      <Terminal className="w-3.5 h-3.5" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
