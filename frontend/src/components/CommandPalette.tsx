import React, { useState, useEffect } from 'react';
import { 
  Search, 
  Compass, 
  FileText, 
  Palette, 
  BarChart3, 
  Zap, 
  ShieldCheck, 
  Activity, 
  Box, 
  BookOpen, 
  Play, 
  X,
  Layers
} from 'lucide-react';

interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
  onNavigate: (view: string) => void;
  onStartDemo: () => void;
}

export const CommandPalette: React.FC<CommandPaletteProps> = ({
  isOpen,
  onClose,
  onNavigate,
  onStartDemo,
}) => {
  const [query, setQuery] = useState('');

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        if (isOpen) onClose();
        else setQuery('');
      }
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const actions = [
    { id: 'demo', title: '▶ Run Interactive AI Campaign Demonstration', category: 'DEMO', icon: <Play className="w-4 h-4 text-cyan-400" />, action: () => { onStartDemo(); onClose(); } },
    { id: 'pipeline', title: 'View Multi-Agent Intelligence Pipeline (DAG)', category: 'WORKSPACE', icon: <Layers className="w-4 h-4 text-purple-400" />, action: () => { onNavigate('pipeline'); onClose(); } },
    { id: 'agents', title: 'Open AI Agent Center & Contracts Observatory', category: 'WORKSPACE', icon: <Compass className="w-4 h-4 text-cyan-400" />, action: () => { onNavigate('agents'); onClose(); } },
    { id: 'optimizer', title: 'Open RL Policy Optimizer Dashboard (PPO)', category: 'WORKSPACE', icon: <Zap className="w-4 h-4 text-amber-400" />, action: () => { onNavigate('optimizer'); onClose(); } },
    { id: 'hitl', title: 'Open Human-in-the-Loop Governance Gate', category: 'OPERATIONS', icon: <ShieldCheck className="w-4 h-4 text-rose-400" />, action: () => { onNavigate('hitl'); onClose(); } },
    { id: 'models', title: 'Inspect Machine Learning Model Registry', category: 'SYSTEM', icon: <Box className="w-4 h-4 text-blue-400" />, action: () => { onNavigate('models'); onClose(); } },
    { id: 'creative', title: 'Open Nano Banana Creative Studio', category: 'WORKSPACE', icon: <Palette className="w-4 h-4 text-pink-400" />, action: () => { onNavigate('creative'); onClose(); } },
    { id: 'timeline', title: 'View Campaign Audit Event Timeline', category: 'OPERATIONS', icon: <Activity className="w-4 h-4 text-emerald-400" />, action: () => { onNavigate('timeline'); onClose(); } },
    { id: 'health', title: 'Check AI Platform System Health', category: 'SYSTEM', icon: <Activity className="w-4 h-4 text-cyan-400" />, action: () => { onNavigate('health'); onClose(); } },
    { id: 'techstack', title: 'Open Technology Stack & System Architecture Board', category: 'SYSTEM', icon: <Box className="w-4 h-4 text-cyan-400" />, action: () => { onNavigate('techstack'); onClose(); } },
    { id: 'rag', title: 'Access RAG Knowledge Base & Memory', category: 'KNOWLEDGE', icon: <BookOpen className="w-4 h-4 text-purple-400" />, action: () => { onNavigate('knowledge'); onClose(); } },
  ];

  const filtered = actions.filter(a => 
    a.title.toLowerCase().includes(query.toLowerCase()) || 
    a.category.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-16 sm:pt-24 p-3 sm:p-4">
      {/* Backdrop */}
      <div 
        onClick={onClose}
        className="absolute inset-0 bg-slate-950/80 backdrop-blur-md" 
      />

      {/* Palette Container */}
      <div className="relative z-10 w-full max-w-xl bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        {/* Search Input */}
        <div className="p-3.5 sm:p-4 border-b border-slate-800 flex items-center gap-2.5 sm:gap-3 bg-slate-950/90">
          <Search className="w-4 h-4 sm:w-5 sm:h-5 text-slate-500 shrink-0" />
          <input
            type="text"
            placeholder="Type a command (e.g. 'Optimizer', 'Demo', 'Models')..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            autoFocus
            className="w-full bg-transparent text-xs sm:text-sm text-slate-100 placeholder:text-slate-500 focus:outline-none"
          />
          <button
            onClick={onClose}
            className="p-1 rounded text-slate-400 hover:text-white"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Results List */}
        <div className="max-h-80 overflow-y-auto p-2 divide-y divide-slate-800/40">
          {filtered.length > 0 ? (
            filtered.map((item) => (
              <div
                key={item.id}
                onClick={item.action}
                className="p-3 rounded-xl hover:bg-slate-800/80 cursor-pointer flex items-center justify-between gap-3 group transition-colors"
              >
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-slate-950 border border-slate-800 group-hover:border-slate-700">
                    {item.icon}
                  </div>
                  <span className="text-xs font-semibold text-slate-200 group-hover:text-cyan-300">
                    {item.title}
                  </span>
                </div>
                <span className="text-[10px] font-mono text-slate-500 uppercase">
                  {item.category}
                </span>
              </div>
            ))
          ) : (
            <div className="p-6 text-center text-xs text-slate-500">
              No matching commands found for "{query}".
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
