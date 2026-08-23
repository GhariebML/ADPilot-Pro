import React, { useState, useEffect } from 'react';
import { Play, Pause, RefreshCw, CheckCircle, AlertTriangle, ChevronRight, Activity, Target, Brain, Database, PenTool, Image, BarChart3, ShieldCheck, UploadCloud, Eye } from 'lucide-react';

export const CampaignSimulationView = () => {
  const [simulation, setSimulation] = useState<any>(null);
  const [simId, setSimId] = useState<string | null>(null);
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null);

  const startDemo = async () => {
    const res = await fetch('http://localhost:8001/api/v1/simulations', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        product_name: 'AI Marketing SaaS',
        product_type: 'saas',
        campaign_objective: 'Lead Generation',
        target_audience: 'SMB Founders',
        budget: 10000,
        duration_days: 30,
        platforms: ['Meta', 'Google', 'LinkedIn'],
        target_cac: 45,
        target_roas: 3.5
      })
    });
    const data = await res.json();
    setSimId(data.simulation_id);
    await fetch('http://localhost:8001/api/v1/simulations/' + data.simulation_id + '/run', { method: 'POST' });
  };

  useEffect(() => {
    if (!simId) return;
    const interval = setInterval(async () => {
      try {
        const res = await fetch('http://localhost:8001/api/v1/simulations/' + simId);
        if (!res.ok) {
          if (res.status === 404) { clearInterval(interval); setSimId(null); setSimulation(null); }
          return;
        }
        const data = await res.json();
        setSimulation(data);
        if (data.status === 'COMPLETED' || data.status === 'FAILED') {
          clearInterval(interval);
        }
      } catch (e) { /* network error, ignore */ }
    }, 1500);
    return () => clearInterval(interval);
  }, [simId]);

  const approve = async () => {
    if (!simId) return;
    await fetch('http://localhost:8001/api/v1/simulations/' + simId + '/approve', { method: 'POST' });
  };

  if (!simulation) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-slate-500 space-y-6">
        <Activity className="w-16 h-16 opacity-20" />
        <h2 className="text-xl font-bold tracking-widest text-slate-400">ENTERPRISE PIPELINE IDLE</h2>
        <div className="flex gap-4">
          <button onClick={startDemo} className="flex items-center gap-2 px-6 py-3 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg font-bold transition-all shadow-[0_0_15px_rgba(6,182,212,0.3)]">
            <Play className="w-5 h-5" /> INITIALIZE FULL PIPELINE
          </button>
        </div>
      </div>
    );
  }

  const phases = [
    {
      name: 'Phase 1: Ingestion',
      agents: [
        { id: 'Campaign Manager Agent', icon: Database },
        { id: 'Product Classifier Agent', icon: Target },
        { id: 'Audience Agent', icon: Brain },
        { id: 'Competitor Agent', icon: Activity }
      ]
    },
    {
      name: 'Phase 2: Strategy',
      agents: [
        { id: 'Strategy Agent', icon: Brain },
        { id: 'Research Agent', icon: Activity }
      ]
    },
    {
      name: 'Phase 3: Creative Factory',
      agents: [
        { id: 'Content Agent', icon: PenTool },
        { id: 'Design Agent', icon: Image },
        { id: 'Creative Agent', icon: Image },
        { id: 'CV Agent', icon: Eye }
      ]
    },
    {
      name: 'Phase 4: Optimization',
      agents: [
        { id: 'Analytics Agent', icon: BarChart3 },
        { id: 'RL / PPO Optimizer', icon: Brain }
      ]
    },
    {
      name: 'Phase 5: Deployment',
      agents: [
        { id: 'Correction Agent', icon: ShieldCheck },
        { id: 'Publishing Agent', icon: UploadCloud },
        { id: 'Monitoring Agent', icon: Activity }
      ]
    }
  ];

  return (
    <div className="flex flex-col h-screen bg-slate-950 text-white p-6 gap-6 font-sans">
      <header className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-2xl font-bold flex items-center gap-2"><Activity className="text-cyan-400"/> Enterprise AI Control Center</h1>
          <span className="text-xs font-mono text-slate-500">SIMULATION MODE ACTIVE</span>
        </div>
        <div className="flex items-center gap-4">
          <div className={`px-3 py-1 rounded font-bold font-mono text-xs ${simulation.status === 'RUNNING' ? 'bg-cyan-500/20 text-cyan-400' : simulation.status === 'FAILED' ? 'bg-red-500/20 text-red-400' : 'bg-emerald-500/20 text-emerald-400'}`}>
            STATUS: {simulation.status}
          </div>
        </div>
      </header>

      <div className="flex flex-1 gap-6 min-h-0 overflow-hidden">
        {/* Pipeline Column */}
        <div className="w-1/3 bg-slate-900/50 border border-slate-800 rounded-xl p-4 overflow-y-auto space-y-6 relative backdrop-blur-xl custom-scrollbar">
          <h2 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-2 sticky top-0 bg-slate-900/90 py-2 z-10 backdrop-blur">Execution Pipeline DAG</h2>
          
          <div className="space-y-6">
            {phases.map((phase, pIdx) => (
              <div key={pIdx} className="space-y-3">
                <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest border-l-2 border-slate-700 pl-2">{phase.name}</h3>
                <div className="space-y-2 pl-4 border-l border-slate-800/50">
                  {phase.agents.map((agent, aIdx) => {
                    const exec = simulation.agent_executions?.[agent.id];
                    const isCurrent = simulation.current_stage === agent.id;
                    const AgentIcon = agent.icon;
                    return (
                      <div key={aIdx} onClick={() => setSelectedAgent(agent.id)} className={`p-3 rounded-lg cursor-pointer border transition-all flex items-center justify-between ${isCurrent ? 'bg-cyan-900/30 border-cyan-500/50 shadow-[0_0_15px_rgba(6,182,212,0.2)]' : exec ? 'bg-slate-800/40 border-slate-700/50 hover:bg-slate-800' : 'bg-slate-900/50 border-slate-800/50 opacity-60'}`}>
                        <div className="flex items-center gap-3">
                          <div className={`p-2 rounded flex items-center justify-center ${isCurrent ? 'bg-cyan-500/20 text-cyan-400' : exec ? 'bg-emerald-500/10 text-emerald-500' : 'bg-slate-800 text-slate-600'}`}>
                            <AgentIcon className="w-4 h-4" />
                          </div>
                          <div>
                            <h4 className="font-bold text-xs">{agent.id}</h4>
                            {exec && <div className="text-[10px] text-slate-500 font-mono mt-0.5">{exec.model_used}</div>}
                          </div>
                        </div>
                        <div>
                          {exec ? <CheckCircle className="w-4 h-4 text-emerald-400" /> : isCurrent ? <RefreshCw className="w-4 h-4 text-cyan-400 animate-spin" /> : null}
                        </div>
                      </div>
                    )
                  })}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Agent Inspector Column */}
        <div className="flex-1 bg-slate-900/50 border border-slate-800 rounded-xl p-6 overflow-y-auto backdrop-blur-xl space-y-6">
          {!selectedAgent ? (
            <div className="h-full flex flex-col items-center justify-center text-slate-500 space-y-4">
              <Activity className="w-12 h-12 opacity-20" />
              <p>Select a pipeline node to inspect deep execution telemetry.</p>
            </div>
          ) : (
            <div>
               {simulation.agent_executions?.[selectedAgent] ? (
                 <div className="space-y-6">
                   <div className="border-b border-slate-800 pb-4">
                     <div className="flex items-center justify-between mb-2">
                       <h2 className="text-xl font-bold text-cyan-400">{selectedAgent}</h2>
                       <div className="px-2 py-1 bg-slate-800 rounded text-xs font-mono text-slate-400">Latency: {simulation.agent_executions[selectedAgent].execution_time}s</div>
                     </div>
                     <p className="text-sm text-slate-400">{simulation.agent_executions[selectedAgent].purpose}</p>
                     
                     <div className="flex gap-4 mt-4">
                        <div className="px-3 py-1 bg-slate-950 border border-slate-800 rounded text-xs text-slate-400 font-mono">
                          <span className="text-slate-500 mr-2">Model:</span>{simulation.agent_executions[selectedAgent].model_used}
                        </div>
                        <div className="px-3 py-1 bg-slate-950 border border-slate-800 rounded text-xs text-slate-400 font-mono">
                          <span className="text-slate-500 mr-2">Tool:</span>{simulation.agent_executions[selectedAgent].tools_used?.[0] || 'None'}
                        </div>
                     </div>
                   </div>
                   
                   <div className="grid grid-cols-1 gap-6">
                     <div className="space-y-2">
                       <h4 className="text-xs font-bold text-slate-500 uppercase tracking-widest flex items-center gap-2"><ChevronRight className="w-3 h-3"/> Input Context Payload</h4>
                       <pre className="text-xs font-mono bg-[#0d1117] p-4 rounded-lg border border-slate-800 overflow-x-auto text-emerald-300">
                         {JSON.stringify(simulation.agent_executions[selectedAgent].input, null, 2)}
                       </pre>
                     </div>
                     <div className="space-y-2">
                       <h4 className="text-xs font-bold text-slate-500 uppercase tracking-widest flex items-center gap-2"><ChevronRight className="w-3 h-3"/> Agent Output Trace</h4>
                       <pre className="text-xs font-mono bg-[#0d1117] p-4 rounded-lg border border-slate-800 overflow-x-auto text-cyan-300">
                         {JSON.stringify(simulation.agent_executions[selectedAgent].output, null, 2)}
                       </pre>
                     </div>
                   </div>
                 </div>
               ) : (
                 <div className="h-full flex flex-col items-center justify-center text-slate-500 space-y-4">
                   <RefreshCw className="w-8 h-8 opacity-20 animate-spin" />
                   <p className="text-sm">Agent has not executed in this simulation yet.</p>
                 </div>
               )}
            </div>
          )}
        </div>
        
        {/* Results / HITL Column */}
        <div className="w-1/4 space-y-6">
          <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-4 backdrop-blur-xl h-full flex flex-col">
            <h2 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-4">Human-in-the-Loop</h2>
            {simulation.status === 'REVIEW_REQUIRED' ? (
              <div className="space-y-4">
                <div className="p-4 bg-amber-500/10 border border-amber-500/30 rounded-lg">
                  <h3 className="font-bold text-amber-400 mb-2 flex items-center gap-2"><AlertTriangle className="w-4 h-4" /> Action Required</h3>
                  <p className="text-xs text-amber-200/70 mb-4">The PPO Agent has proposed a channel reallocation. Please review and approve the strategy.</p>
                  <button onClick={approve} className="w-full py-2 bg-emerald-500 hover:bg-emerald-600 text-white rounded font-bold text-sm transition-all shadow-[0_0_10px_rgba(16,185,129,0.3)]">APPROVE ACTION</button>
                </div>
              </div>
            ) : simulation.status === 'COMPLETED' ? (
              <div className="space-y-4">
                <div className="p-4 bg-emerald-500/10 border border-emerald-500/30 rounded-lg">
                  <h3 className="font-bold text-emerald-400 flex items-center gap-2"><CheckCircle className="w-4 h-4" /> Simulation Complete</h3>
                  <div className="text-xs text-emerald-200/70 mt-2">Approved by human. Final state reached.</div>
                </div>
                {simulation.final_result && (
                  <div className="space-y-3 mt-6">
                    <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest border-b border-slate-800 pb-2">Simulated Performance</h3>
                    <div className="bg-[#0d1117] p-3 rounded-lg border border-slate-800 text-sm font-mono flex justify-between items-center">
                      <span className="text-slate-400">ROAS</span>
                      <span className="text-white">{simulation.final_result.roas_before}x &rarr; <span className="text-emerald-400 font-bold">{simulation.final_result.roas_after}x</span></span>
                    </div>
                    <div className="bg-[#0d1117] p-3 rounded-lg border border-slate-800 text-sm font-mono flex justify-between items-center">
                      <span className="text-slate-400">CAC</span>
                      <span className="text-white"> &rarr; <span className="text-emerald-400 font-bold"></span></span>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center h-48 opacity-50">
                 <div className="w-2 h-2 bg-cyan-500 rounded-full animate-ping mb-4"></div>
                 <div className="text-xs text-slate-500 text-center font-mono">AWAITING PIPELINE COMPLETION</div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
