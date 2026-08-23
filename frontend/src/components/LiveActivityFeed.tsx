import React from 'react';
import { 
  Activity, 
  X, 
  CheckCircle2, 
  Cpu, 
  Sparkles, 
  AlertTriangle,
  Layers
} from 'lucide-react';
import type { AIActivityEvent } from '../types';

interface LiveActivityFeedProps {
  isOpen: boolean;
  onClose: () => void;
  events: AIActivityEvent[];
}

export const LiveActivityFeed: React.FC<LiveActivityFeedProps> = ({
  isOpen,
  onClose,
  events,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed top-16 right-4 z-40 w-full max-w-sm sm:max-w-md bg-slate-900/95 border border-slate-800 rounded-2xl shadow-2xl backdrop-blur-3xl overflow-hidden animate-in fade-in slide-in-from-top-4 duration-200">
      {/* Header */}
      <div className="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-950/80">
        <div className="flex items-center gap-2.5">
          <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
          <h3 className="text-xs font-bold text-slate-100 uppercase tracking-wider font-mono">
            Autonomous AI Activity Stream
          </h3>
        </div>
        <button
          onClick={onClose}
          className="p-1 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Feed List */}
      <div className="p-3 max-h-96 overflow-y-auto divide-y divide-slate-800/60 space-y-2">
        {events.map(evt => (
          <div key={evt.id} className="pt-2 text-xs font-mono">
            <div className="flex items-center justify-between text-[11px] mb-1">
              <span className="font-bold text-cyan-400">{evt.agent}</span>
              <span className="text-slate-500">{evt.timestamp}</span>
            </div>
            <p className="text-slate-300 font-sans text-xs">{evt.details}</p>
            {evt.latency && (
              <div className="text-[10px] text-slate-500 mt-1 flex justify-end">
                <span>Latency: {evt.latency}</span>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

