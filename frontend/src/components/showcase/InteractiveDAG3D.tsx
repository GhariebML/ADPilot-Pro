import React, { useState, useEffect } from 'react';
import { 
  ArrowRight, 
  CheckCircle2, 
  Play, 
  Terminal, 
  Cpu, 
  Sparkles, 
  Zap, 
  ShieldCheck, 
  Eye, 
  RotateCcw,
  Activity,
  Layers,
  Database
} from 'lucide-react';

interface StageNode {
  id: string;
  stageNum: string;
  name: string;
  model: string;
  role: string;
  latency: string;
  tokens: string;
  status: 'PENDING' | 'RUNNING' | 'COMPLETED';
  log: string;
  color: string;
}

export const InteractiveDAG3D: React.FC = () => {
  const [activeStageId, setActiveStageId] = useState<string>('stage-3');
  const [isSimulating, setIsSimulating] = useState<boolean>(false);
  const [simulationIndex, setSimulationIndex] = useState<number>(2);

  const stages: StageNode[] = [
    {
      id: 'stage-1',
      stageNum: '01',
      name: 'Business Ingestion',
      model: 'FastAPI + Pydantic v2',
      role: 'Parses objective, brand voice rules, seed budget & audience criteria.',
      latency: '2.4ms',
      tokens: '412 B',
      status: simulationIndex >= 0 ? 'COMPLETED' : 'PENDING',
      log: 'INGESTION_VALIDATED: CampaignContext validated against strict Pydantic v2 schema. Budget constraints initialized ($15,000 blended).',
      color: 'from-cyan-500/20 to-blue-500/20 border-cyan-500/50 text-cyan-300'
    },
    {
      id: 'stage-2',
      stageNum: '02',
      name: 'Strategy Formulation',
      model: 'GPT-4o Router',
      role: 'Synthesizes multi-channel budget roadmap, TOFU/MOFU/BOFU funnels & KPI gates.',
      latency: '1,420ms',
      tokens: '1,840 toks',
      status: simulationIndex >= 1 ? 'COMPLETED' : 'PENDING',
      log: 'STRATEGY_GENERATED: LinkedIn (45%), Meta (30%), Google Search (25%). 3 Persona cohorts synthesized: Enterprise CTO, VP Growth, FinOps Lead.',
      color: 'from-blue-500/20 to-indigo-500/20 border-blue-500/50 text-blue-300'
    },
    {
      id: 'stage-3',
      stageNum: '03',
      name: 'Hybrid RAG Grounding',
      model: 'FastEmbed BGE + BM25',
      role: 'Dual-stream semantic retrieval in Qdrant with Reciprocal Rank Fusion (k=60).',
      latency: '28.5ms',
      tokens: '384-dim',
      status: simulationIndex >= 2 ? 'COMPLETED' : 'PENDING',
      log: 'RAG_RETRIEVAL_COMPLETE: Retrieved 6 top document chunks (Dense cosine: 0.94, Sparse BM25: 14.8). Zero factual hallucinations detected.',
      color: 'from-purple-500/20 to-pink-500/20 border-purple-500/50 text-purple-300'
    },
    {
      id: 'stage-4',
      stageNum: '04',
      name: 'Creative Synthesis',
      model: 'Claude 3.5 Sonnet',
      role: 'Multi-variant ad copy, 3-tier email nurture sequences & banner directives.',
      latency: '1,980ms',
      tokens: '3,120 toks',
      status: simulationIndex >= 3 ? 'COMPLETED' : 'PENDING',
      log: 'CREATIVE_SYNTHESIZED: Generated 4 headline variants (A/B testing enabled), 3 email nurture triggers, and 4 canvas aspect-ratio directives.',
      color: 'from-pink-500/20 to-rose-500/20 border-pink-500/50 text-pink-300'
    },
    {
      id: 'stage-5',
      stageNum: '05',
      name: 'CLIP-ViT Vision Gate',
      model: 'ONNX ViT-B/32',
      role: 'Zero-shot aesthetic regressor, WCAG AAA text contrast & safe margin auditor.',
      latency: '4.8ms',
      tokens: '512-dim',
      status: simulationIndex >= 4 ? 'COMPLETED' : 'PENDING',
      log: 'CV_QUALITY_PASSED: Aesthetic Score = 9.14/10. Contrast Ratio = 9.4:1 (WCAG AAA Pass). Margins within safe 8% boundary. 0 violations.',
      color: 'from-indigo-500/20 to-cyan-500/20 border-indigo-500/50 text-indigo-300'
    },
    {
      id: 'stage-6',
      stageNum: '06',
      name: 'PPO Policy Optimizer',
      model: 'PyTorch Actor-Critic',
      role: 'Dirichlet continuous action projection maximizing blended ROAS alpha.',
      latency: '15.8ms',
      tokens: '12-dim State',
      status: simulationIndex >= 5 ? 'COMPLETED' : 'PENDING',
      log: 'PPO_OPTIMIZATION_EMITTED: Shifted +12% budget to LinkedIn based on predicted CAC ($38.40 vs $54.20). Mean return alpha = +28.7%.',
      color: 'from-amber-500/20 to-emerald-500/20 border-amber-500/50 text-amber-300'
    },
    {
      id: 'stage-7',
      stageNum: '07',
      name: 'HMAC Cryptographic Gate',
      model: 'HMAC-SHA256 Ledger',
      role: 'Human Director signs tamper-proof cryptographic receipt for dispatch.',
      latency: '1.2ms',
      tokens: '256-bit Key',
      status: simulationIndex >= 6 ? 'COMPLETED' : 'PENDING',
      log: 'HITL_SIGNATURE_RECORDED: Receipt HMAC-SHA256(e9f4c081...a3d) signed by Campaign Director. Dispatched to Meta & LinkedIn API sandboxes.',
      color: 'from-emerald-500/20 to-cyan-500/20 border-emerald-500/50 text-emerald-300'
    }
  ];

  const activeStage = stages.find(s => s.id === activeStageId) || stages[0];

  const triggerLiveRun = () => {
    setIsSimulating(true);
    setSimulationIndex(0);
    setActiveStageId(stages[0].id);

    let current = 0;
    const interval = setInterval(() => {
      current++;
      if (current < stages.length) {
        setSimulationIndex(current);
        setActiveStageId(stages[current].id);
      } else {
        clearInterval(interval);
        setIsSimulating(false);
      }
    }, 900);
  };

  return (
    <div className="w-full bg-slate-950/40 border border-slate-800/60 shadow-2xl rounded-2xl p-6 backdrop-blur-2xl space-y-6 shadow-2xl relative overflow-hidden">
      {/* Background Laser Scan */}
      <div className="absolute inset-0 cyber-grid-3d opacity-30 pointer-events-none" />

      {/* Top Header & Simulation Trigger */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 relative z-10 border-b border-slate-800/80 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-1.5 rounded-lg bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
              <Layers className="w-4 h-4" />
            </span>
            <h3 className="text-base font-bold text-white font-mono uppercase tracking-wider">
              Interactive 3D Multi-Agent Pipeline Flow (DAG)
            </h3>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Click any node or trigger the live simulation to trace deterministic state passing across all 7 layers.
          </p>
        </div>

        <button
          onClick={triggerLiveRun}
          disabled={isSimulating}
          className="px-4 py-2 rounded-xl text-xs font-mono font-bold bg-gradient-to-r from-cyan-500 via-blue-600 to-purple-600 hover:from-cyan-400 hover:to-purple-500 text-white shadow-lg shadow-cyan-500/20 flex items-center gap-2 transition-all active:scale-95 disabled:opacity-50 shrink-0"
        >
          {isSimulating ? (
            <>
              <Activity className="w-4 h-4 animate-spin" />
              <span>Simulating DAG Execution...</span>
            </>
          ) : (
            <>
              <Play className="w-4 h-4 fill-white" />
              <span>Simulate Full DAG Execution</span>
            </>
          )}
        </button>
      </div>

      {/* 3D DAG Pipeline Nodes */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-2.5 relative z-10">
        {stages.map((stage, idx) => {
          const isSelected = activeStageId === stage.id;
          const isDone = stage.status === 'COMPLETED';

          return (
            <div
              key={stage.id}
              onClick={() => setActiveStageId(stage.id)}
              className={`p-3.5 rounded-xl border bg-gradient-to-b ${stage.color} backdrop-blur-md cursor-pointer transition-all duration-300 flex flex-col justify-between space-y-2 relative group hover:scale-[1.03] ${
                isSelected
                  ? 'ring-2 ring-cyan-400 shadow-lg shadow-cyan-500/20 scale-[1.02]'
                  : 'opacity-85 hover:opacity-100'
              }`}
            >
              <div className="flex items-center justify-between text-[10px] font-mono font-bold">
                <span className="text-slate-400">STAGE {stage.stageNum}</span>
                {isDone ? (
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                ) : (
                  <span className="w-2 h-2 rounded-full bg-slate-600 animate-pulse" />
                )}
              </div>

              <div>
                <div className="text-xs font-bold text-white truncate group-hover:text-cyan-200">
                  {stage.name}
                </div>
                <div className="text-[10px] text-slate-300 font-mono truncate mt-0.5">
                  {stage.model}
                </div>
              </div>

              <div className="text-[9px] font-mono text-slate-400 flex items-center justify-between pt-1 border-t border-slate-700/40">
                <span>{stage.latency}</span>
                <span className="text-cyan-300">{stage.tokens}</span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Interactive Active Node Console */}
      <div className="p-4 rounded-xl bg-slate-900/90 border border-slate-800 space-y-3 relative z-10 font-mono text-xs">
        <div className="flex items-center justify-between border-b border-slate-800 pb-2">
          <div className="flex items-center gap-2 text-cyan-400 font-bold">
            <Terminal className="w-4 h-4" />
            <span>STAGE {activeStage.stageNum}: {activeStage.name.toUpperCase()} (ACTIVE TRACE)</span>
          </div>
          <div className="flex items-center gap-3 text-[11px] text-slate-400">
            <span>Model: <strong className="text-purple-300">{activeStage.model}</strong></span>
            <span>Latency: <strong className="text-emerald-400">{activeStage.latency}</strong></span>
          </div>
        </div>

        <p className="text-xs text-slate-300">
          {activeStage.role}
        </p>

        <div className="p-3 rounded-lg bg-slate-950 border border-slate-800 text-[11px] text-emerald-400 overflow-x-auto">
          <code>&gt; {activeStage.log}</code>
        </div>
      </div>
    </div>
  );
};

export default InteractiveDAG3D;

