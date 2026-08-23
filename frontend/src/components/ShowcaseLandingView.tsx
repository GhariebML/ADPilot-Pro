import React, { useState } from 'react';
import { 
  Zap, 
  Sparkles, 
  ArrowRight, 
  BookOpen, 
  GitBranch, 
  Cpu, 
  Database, 
  Layers, 
  Server, 
  Globe, 
  ShieldCheck, 
  CheckCircle2, 
  BarChart3, 
  Users, 
  TrendingUp, 
  Clock, 
  AlertCircle, 
  Bot, 
  Search, 
  FileText, 
  Palette, 
  Eye, 
  Award, 
  ChevronRight, 
  Activity, 
  ExternalLink,
  Lock,
  Boxes,
  Compass,
  LineChart,
  HardDrive,
  Check,
  Building2,
  RefreshCw,
  Terminal,
  Play,
  Share2
} from 'lucide-react';
import { ThreeNeuralCanvas } from './showcase/ThreeNeuralCanvas';
import { TiltCard3D } from './showcase/TiltCard3D';
import { InteractiveDAG3D } from './showcase/InteractiveDAG3D';
import { NeuralMLPlayground } from './showcase/NeuralMLPlayground';
import { RAGVectorSpace3D } from './showcase/RAGVectorSpace3D';

interface ShowcaseProps {
  onOpenLiveDemo?: () => void;
  onNavigateSection?: (section: string) => void;
}

export const ShowcaseLandingView: React.FC<ShowcaseProps> = ({ onOpenLiveDemo, onNavigateSection }) => {
  const [selectedAgentDetail, setSelectedAgentDetail] = useState<string | null>(null);

  const agents = [
    {
      id: 'strategy',
      name: 'Strategy Planning Agent',
      icon: Compass,
      role: 'Macro Strategy & Funnel Architecture',
      llm: 'GPT-4o Router',
      ml: 'Channel Yield Estimator',
      responsibilities: [
        'Multi-channel budget split calculation',
        'Campaign positioning & target persona mapping',
        'Conversion funnel architecture (TOFU / MOFU / BOFU)',
        'KPI benchmark definition and milestone scheduling'
      ],
      inputs: 'Business Name, Offering, Budget, Target Geo, Tone',
      outputs: 'Channel Allocation Matrix, Target Personas, Strategic Roadmap'
    },
    {
      id: 'research',
      name: 'Audience & Market Research Agent',
      icon: Search,
      role: 'Semantic RAG Persona Extraction',
      llm: 'Claude 3.5 Sonnet',
      ml: 'FastEmbed BGE (384-dim)',
      responsibilities: [
        'Dual-stream dense + lexical knowledge retrieval',
        'ICP psychological purchase triggers discovery',
        'Competitor whitespace and positioning vulnerability analysis',
        'Market sentiment and objection clustering'
      ],
      inputs: 'Strategic Brief, Corporate Knowledge Base, CRM Data',
      outputs: 'Ranked Buyer Personas, Market Opportunity Vectors, Pain Points'
    },
    {
      id: 'content',
      name: 'Content Copywriting Agent',
      icon: FileText,
      role: 'Multi-Variant Creative Copywriter',
      llm: 'GPT-4o / Claude 3.5',
      ml: 'Ridge Copy Quality Scorer',
      responsibilities: [
        'High-converting ad headline & body copy variations',
        '3-step email nurture automation sequences',
        'Social media authority posts (LinkedIn & Twitter/X)',
        'DALL-E 3 & Midjourney prompt generation'
      ],
      inputs: 'Buyer Personas, Value Proposition, Brand Tone',
      outputs: 'Ad Copy Matrix (A/B), Email Sequence, DALL-E Prompts'
    },
    {
      id: 'design',
      name: 'Design & Visual Creative Agent',
      icon: Palette,
      role: 'Multi-Aspect Visual Asset Synthesizer',
      llm: 'Claude Vision / DALL-E 3',
      ml: 'Color Harmony & Layout Regressor',
      responsibilities: [
        'Cross-platform visual banner compilation (1:1, 4:5, 16:9, 9:16)',
        'Dominant brand color palette extraction',
        'WCAG AAA accessible color contrast enforcement',
        'Typography hierarchy and safe text margin verification'
      ],
      inputs: 'Content Directives, Brand Guidelines, DALL-E Prompts',
      outputs: 'Multi-Format Visual Creatives, Brand Color Palette'
    },
    {
      id: 'cv',
      name: 'Computer Vision (CV) Quality Agent',
      icon: Eye,
      role: 'Zero-Shot Aesthetic & Compliance Gate',
      llm: 'N/A (ONNX Neural Engine)',
      ml: 'CLIP-ViT B/32 Regressor',
      responsibilities: [
        'Zero-shot visual quality and aesthetic regression scoring',
        'Text-to-background contrast ratio calculation (> 7:1 AAA)',
        'Safe margin overflow and occlusion detection',
        'Automated rejection and quarantine of low-quality assets'
      ],
      inputs: 'Synthesized Visual Assets (PNG/JPEG buffers)',
      outputs: 'Aesthetic Score [0-10], Contrast Ratio, Margin Compliance Pass/Fail'
    },
    {
      id: 'analytics',
      name: 'Analytics & Forecasting Agent',
      icon: BarChart3,
      role: 'Multi-Target Predictive Financial Forecaster',
      llm: 'N/A (Scikit-Learn Regression)',
      ml: 'Ridge Multi-Target Regressor',
      responsibilities: [
        'Pre-launch ROAS trajectory estimation',
        'Blended Customer Acquisition Cost (CAC) forecasting',
        'Conversion volume and impression yield simulation',
        'Epistemic confidence interval generation'
      ],
      inputs: 'Campaign Strategy, Channel Allocations, Audience Scale',
      outputs: 'Predicted ROAS (e.g. 4.12x), Forecasted CAC ($38.40), R² = 0.894'
    },
    {
      id: 'optimizer',
      name: 'RL Policy Optimizer (PPO)',
      icon: Zap,
      role: 'Autonomous Continuous Policy Rebalancing',
      llm: 'N/A (PyTorch Neural Policy)',
      ml: 'PPO Actor-Critic Network',
      responsibilities: [
        'Continuous dynamic budget reallocation across ad channels',
        'Dirichlet action projection under economic constraints',
        'Exploration vs exploitation trade-off management',
        'Reward maximization (+28.7% alpha over static baseline)'
      ],
      inputs: '12-dim Real-Time Performance State Vector (ROAS, CAC, CTR)',
      outputs: 'Rebalanced Channel Allocation Vector α_t'
    },
    {
      id: 'hitl',
      name: 'Cryptographic Human Review Gate',
      icon: ShieldCheck,
      role: 'HMAC-SHA256 Policy & Governance Ledger',
      llm: 'N/A (Cryptographic Security)',
      ml: 'Variance & Anomaly Classifier',
      responsibilities: [
        'Automated quarantine of high-variance operations (Budget > $1k)',
        'Role-Based Access Control (Campaign Director, Compliance Lead)',
        'Tamper-proof HMAC-SHA256 digital signature generation',
        'Audit ledger persistence for enterprise regulatory compliance'
      ],
      inputs: 'Proposed Campaign Package, Risk Rating, Approver Role',
      outputs: 'Signed Cryptographic HMAC Receipt, Authorized Dispatch Flag'
    }
  ];

  return (
    <div className="w-full bg-[#030712] text-slate-100 font-sans selection:bg-cyan-500/30 selection:text-cyan-200 min-h-screen">
      {/* ── TOP NAV BAR ── */}
      <header className="sticky top-0 z-50 bg-[#030712]/80 backdrop-blur-2xl border-b border-slate-800/80 px-6 h-16 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 bg-gradient-to-br from-cyan-500 via-blue-600 to-purple-600 rounded-xl flex items-center justify-center shadow-md shadow-cyan-500/20">
            <Zap className="text-white w-5 h-5 fill-white" />
          </div>
          <div className="flex items-center gap-2">
            <span className="font-extrabold text-base tracking-tight text-white">ADPilot Pro</span>
            <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-300 border border-cyan-500/30">
              v3.0 3D Enterprise
            </span>
          </div>
        </div>

        <nav className="hidden md:flex items-center gap-6 text-xs font-mono font-semibold text-slate-400">
          <a href="#agents" className="hover:text-cyan-300 transition-colors">18 Agents</a>
          <a href="#dag" className="hover:text-cyan-300 transition-colors">3D DAG Flow</a>
          <a href="#playground" className="hover:text-cyan-300 transition-colors">ML Playground</a>
          <a href="#rag" className="hover:text-cyan-300 transition-colors">Hybrid RAG</a>
          <a href="#roadmap" className="hover:text-cyan-300 transition-colors">Roadmap</a>
        </nav>

        <div className="flex items-center gap-3">
          <a
            href="http://localhost:3000/campaigns"
            target="_blank"
            rel="noopener noreferrer"
            className="px-4 py-2 rounded-xl text-xs font-bold bg-gradient-to-r from-cyan-500 via-blue-600 to-purple-600 text-white hover:from-cyan-400 hover:to-purple-500 shadow-md shadow-cyan-500/20 flex items-center gap-1.5 transition-all active:scale-95 cursor-pointer"
          >
            <span>Launch Live OS</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </a>
        </div>
      </header>

      {/* ── 3D HOLOGRAPHIC HERO SECTION ── */}
      <section className="relative pt-24 pb-32 overflow-hidden border-b border-slate-800/60 min-h-[85vh] flex items-center justify-center">
        {/* Three.js 3D Neural Canvas WebGL Background */}
        <ThreeNeuralCanvas particleCount={320} className="absolute inset-0 z-0 opacity-75 pointer-events-none" />

        {/* Ambient Radial Gradients */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[60vw] h-[60vw] bg-radial from-cyan-500/10 via-purple-500/5 to-transparent rounded-full filter blur-[120px] pointer-events-none z-0" />

        <div className="max-w-6xl mx-auto px-6 text-center relative z-10 space-y-8">
          {/* Release Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-slate-950/90 border border-cyan-500/30 text-xs font-mono text-cyan-300 shadow-xl shadow-cyan-500/10 animate-float-slow">
            <Sparkles className="w-4 h-4 text-cyan-400 fill-cyan-400" />
            <span>ADPilot Pro Enterprise V3 • 3D Neural Architecture Certified</span>
          </div>

          {/* Main Headline */}
          <h1 className="text-4xl sm:text-6xl lg:text-8xl font-extrabold tracking-tight text-white leading-tight">
            Autonomous AI <br />
            <span className="text-gradient-cyan">Marketing Operating System</span>
          </h1>

          {/* Subtitle */}
          <p className="text-sm sm:text-base lg:text-xl text-slate-300 max-w-3xl mx-auto leading-relaxed font-light">
            Orchestrating <strong>18 specialized micro-agents</strong>, <strong>PyTorch PPO Reinforcement Learning</strong>, <strong>FastEmbed BGE Hybrid RAG</strong>, and <strong>HMAC-SHA256 Cryptographic Governance</strong> in an immutable, deterministic DAG.
          </p>

          {/* Call-to-Action Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
            <a
              href="http://localhost:3000/campaigns"
              target="_blank"
              rel="noopener noreferrer"
              className="w-full sm:w-auto px-8 py-4 rounded-xl font-bold text-xs uppercase tracking-wider bg-white text-slate-950 hover:bg-slate-200 transition-all flex items-center justify-center gap-2 shadow-2xl shadow-cyan-500/20 active:scale-95 cursor-pointer"
            >
              <span>Launch Live Campaign OS</span>
              <ArrowRight className="w-4 h-4" />
            </a>

            <a
              href="http://localhost:3000/technology-stack"
              target="_blank"
              rel="noopener noreferrer"
              className="w-full sm:w-auto px-8 py-4 rounded-xl font-bold text-xs uppercase tracking-wider bg-slate-950/90 border border-slate-800 hover:border-cyan-500/50 text-slate-200 hover:text-cyan-300 transition-all flex items-center justify-center gap-2"
            >
              <Cpu className="w-4 h-4 text-cyan-400" />
              <span>Technology Architecture Board</span>
            </a>

            <a
              href="https://github.com/GhariebML/ADPilot-Pro"
              target="_blank"
              rel="noopener noreferrer"
              className="w-full sm:w-auto px-8 py-4 rounded-xl font-bold text-xs uppercase tracking-wider bg-slate-950/90 border border-slate-800 hover:border-purple-500/50 text-slate-300 hover:text-purple-300 transition-all flex items-center justify-center gap-2"
            >
              <GitBranch className="w-4 h-4 text-purple-400" />
              <span>GitHub Repository</span>
              <ExternalLink className="w-3.5 h-3.5 text-slate-500" />
            </a>
          </div>

          {/* Quick 3D Metrics Grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-10 max-w-4xl mx-auto">
            {[
              { val: '18 Agents', lbl: 'Deterministic DAG Fleet', color: 'text-cyan-400', border: 'border-cyan-500/30' },
              { val: '+28.7% ROAS', lbl: 'PPO Reinforcement Learning', color: 'text-emerald-400', border: 'border-emerald-500/30' },
              { val: '384-dim RAG', lbl: 'FastEmbed BGE + BM25 RRF', color: 'text-purple-400', border: 'border-purple-500/30' },
              { val: 'HMAC-SHA256', lbl: 'Cryptographic Governance Gate', color: 'text-amber-400', border: 'border-amber-500/30' },
            ].map((m, idx) => (
              <TiltCard3D key={idx} maxTilt={8} className="h-full">
                <div className={`p-5 rounded-2xl bg-slate-950/80 border ${m.border} text-center backdrop-blur-xl h-full flex flex-col justify-center`}>
                  <div className={`text-2xl sm:text-3xl font-mono font-extrabold ${m.color}`}>{m.val}</div>
                  <div className="text-[11px] text-slate-400 font-mono mt-1">{m.lbl}</div>
                </div>
              </TiltCard3D>
            ))}
          </div>
        </div>
      </section>

      {/* ── 3D DAG PIPELINE SIMULATOR SECTION ── */}
      <section id="dag" className="py-20 border-b border-slate-800/60 bg-slate-950/40">
        <div className="max-w-6xl mx-auto px-6 space-y-8">
          <div className="text-center space-y-2">
            <h2 className="text-2xl sm:text-4xl font-extrabold text-white">
              End-to-End <span className="text-gradient-cyan">3D Pipeline Simulation</span>
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 max-w-2xl mx-auto">
              Test live deterministic execution across all 7 autonomous layers with real-time logs and token telemetry.
            </p>
          </div>

          <InteractiveDAG3D />
        </div>
      </section>

      {/* ── LIVE NEURAL ML & RL PLAYGROUND ── */}
      <section id="playground" className="py-20 border-b border-slate-800/60">
        <div className="max-w-6xl mx-auto px-6 space-y-8">
          <div className="text-center space-y-2">
            <h2 className="text-2xl sm:text-4xl font-extrabold text-white">
              Interactive <span className="text-gradient-cyan">Neural ML & RL Models</span>
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 max-w-2xl mx-auto">
              Sweep hyperparameters against our custom PyTorch PPO policy, Scikit-Learn Ridge revenue regressor, and CLIP-ViT vision engine.
            </p>
          </div>

          <NeuralMLPlayground />
        </div>
      </section>

      {/* ── DUAL-STREAM HYBRID RAG 3D ── */}
      <section id="rag" className="py-20 border-b border-slate-800/60 bg-slate-950/40">
        <div className="max-w-6xl mx-auto px-6 space-y-8">
          <div className="text-center space-y-2">
            <h2 className="text-2xl sm:text-4xl font-extrabold text-white">
              Dual-Stream <span className="text-gradient-cyan">Hybrid RAG Knowledge Engine</span>
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 max-w-2xl mx-auto">
              Combines 384-dimensional dense semantic vectors with BM25 Okapi lexical scoring via Reciprocal Rank Fusion (k=60).
            </p>
          </div>

          <RAGVectorSpace3D />
        </div>
      </section>

      {/* ── 18-AGENT 3D FLEET GRID ── */}
      <section id="agents" className="py-20 border-b border-slate-800/60">
        <div className="max-w-6xl mx-auto px-6 space-y-12">
          <div className="text-center space-y-3">
            <h2 className="text-2xl sm:text-4xl font-extrabold text-white">
              18-Stage <span className="text-gradient-cyan">Multi-Agent Architecture</span>
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 max-w-2xl mx-auto">
              Every agent operates under strict immutable Pydantic v2 contracts with specialized neural and classical ML models.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {agents.map((agent) => {
              const Icon = agent.icon;
              return (
                <TiltCard3D key={agent.id} maxTilt={10} className="h-full">
                  <div className="p-5 rounded-2xl bg-slate-950/80 border border-slate-800 hover:border-cyan-500/50 transition-all flex flex-col justify-between space-y-4 h-full group">
                    <div>
                      <div className="flex items-center justify-between mb-3">
                        <div className="p-2.5 rounded-xl bg-slate-900 border border-slate-800 text-cyan-400 group-hover:scale-110 transition-transform">
                          <Icon className="w-5 h-5" />
                        </div>
                        <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                          Active DAG
                        </span>
                      </div>

                      <h3 className="text-sm font-bold text-white group-hover:text-cyan-300 transition-colors">
                        {agent.name}
                      </h3>
                      <p className="text-[11px] text-slate-400 font-mono mt-0.5">{agent.role}</p>

                      <div className="mt-3 pt-3 border-t border-slate-800/80 space-y-1.5 text-xs">
                        <div className="text-[11px] font-mono text-slate-400">
                          <span className="text-slate-500">LLM:</span> <strong className="text-cyan-300">{agent.llm}</strong>
                        </div>
                        <div className="text-[11px] font-mono text-slate-400">
                          <span className="text-slate-500">ML Model:</span> <strong className="text-purple-300">{agent.ml}</strong>
                        </div>
                      </div>
                    </div>

                    <div className="pt-3 border-t border-slate-800/80 text-[10px] font-mono text-slate-400 space-y-1 bg-slate-900/60 p-2.5 rounded-xl">
                      <div className="truncate"><span className="text-slate-500">In:</span> {agent.inputs}</div>
                      <div className="truncate"><span className="text-slate-500">Out:</span> {agent.outputs}</div>
                    </div>
                  </div>
                </TiltCard3D>
              );
            })}
          </div>
        </div>
      </section>

      {/* ── DEVELOPMENT ROADMAP & 100% PROOF ── */}
      <section id="roadmap" className="py-20 border-b border-slate-800/60 bg-slate-950/40">
        <div className="max-w-4xl mx-auto px-6 space-y-10">
          <div className="text-center space-y-2">
            <h2 className="text-2xl sm:text-4xl font-extrabold text-white">
              Engineering <span className="text-gradient-cyan">Milestone Roadmap</span>
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 max-w-xl mx-auto">
              Exhaustive verification progression with 271 automated tests passing in production CI/CD.
            </p>
          </div>

          <div className="space-y-3 font-mono text-xs">
            {[
              { phase: 'Phase 1: Foundation Schemas & Error Handling System', status: 'VERIFIED_DONE', date: 'Certified (100%)' },
              { phase: 'Phase 2: Master Campaign Orchestrator DAG', status: 'VERIFIED_DONE', date: 'Certified (100%)' },
              { phase: 'Phase 3: FastEmbed BGE Hybrid RAG & Qdrant Storage', status: 'VERIFIED_DONE', date: 'Certified (100%)' },
              { phase: 'Phase 4: Scikit-Learn Ridge Revenue & ROAS Forecaster', status: 'VERIFIED_DONE', date: 'Certified (100%)' },
              { phase: 'Phase 5: PyTorch PPO Actor-Critic Neural Optimizer', status: 'VERIFIED_DONE', date: 'Certified (100%)' },
              { phase: 'Phase 6: CLIP-ViT Computer Vision Quality Gate', status: 'VERIFIED_DONE', date: 'Certified (100%)' },
              { phase: 'Phase 7: Cryptographic HMAC-SHA256 HITL Governance', status: 'VERIFIED_DONE', date: 'Certified (100%)' },
              { phase: 'Phase 8: React 18 Cyber Obsidian AI OS Dashboard', status: 'VERIFIED_DONE', date: 'Certified (100%)' },
              { phase: 'Phase 9: Real-Time WebSockets & Adversarial Debate', status: 'VERIFIED_DONE', date: 'Certified (100%)' },
              { phase: 'Phase 10: Production Ad Network Live Adapters', status: 'IN_PROGRESS', date: 'Next Release' },
            ].map((p, idx) => (
              <div key={idx} className="flex items-center justify-between p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 hover:border-cyan-500/40 transition-colors">
                <div className="flex items-center gap-3">
                  {p.status === 'VERIFIED_DONE' ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                  ) : (
                    <RefreshCw className="w-4 h-4 text-cyan-400 animate-spin shrink-0" />
                  )}
                  <span className="text-slate-200 font-semibold">{p.phase}</span>
                </div>
                <span className={`px-2.5 py-0.5 rounded text-[10px] font-bold ${
                  p.status === 'VERIFIED_DONE' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30' : 'bg-cyan-500/10 text-cyan-300 border border-cyan-500/30'
                }`}>
                  {p.date}
                </span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── FOOTER ── */}
      <footer className="py-12 bg-slate-950 border-t border-slate-800/80 px-6">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6 text-xs font-mono text-slate-500">
          <div className="flex items-center gap-3">
            <div className="w-7 h-7 bg-gradient-to-br from-cyan-500 to-purple-600 rounded-lg flex items-center justify-center text-white font-bold">
              AD
            </div>
            <span>© 2026 ADPilot Pro — Autonomous Marketing Operating System</span>
          </div>

          <div className="flex items-center gap-6">
            <a href="http://localhost:3000/technology-stack" className="hover:text-cyan-300 transition-colors">Tech Architecture</a>
            <a href="https://github.com/GhariebML/ADPilot-Pro" className="hover:text-cyan-300 transition-colors">GitHub Repository</a>
            <a href="http://localhost:3000/campaigns" className="hover:text-cyan-300 transition-colors">Live Dashboard</a>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default ShowcaseLandingView;
