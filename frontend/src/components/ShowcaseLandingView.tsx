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
  Share2,
  Code2,
  Brain,
  Network
} from 'lucide-react';
import { ThreeHolographicGlobe, VisualMode } from './showcase/ThreeHolographicGlobe';
import { TiltCard3D } from './showcase/TiltCard3D';
import { InteractiveDAG3D } from './showcase/InteractiveDAG3D';
import { NeuralMLPlayground } from './showcase/NeuralMLPlayground';
import { RAGVectorSpace3D } from './showcase/RAGVectorSpace3D';
import { All18AgentsMatrix } from './showcase/All18AgentsMatrix';
import { LiveCampaignSimulatorStudio } from './showcase/LiveCampaignSimulatorStudio';
import { MathematicalFormulasDeepDive } from './showcase/MathematicalFormulasDeepDive';
import { EnterpriseComparisonMatrix } from './showcase/EnterpriseComparisonMatrix';
import { TechnicalWhitepaperModal } from './showcase/TechnicalWhitepaperModal';

interface ShowcaseProps {
  onOpenLiveDemo?: () => void;
  onNavigateSection?: (section: string) => void;
}

export const ShowcaseLandingView: React.FC<ShowcaseProps> = () => {
  const [isWhitepaperOpen, setIsWhitepaperOpen] = useState<boolean>(false);
  const [visualMode, setVisualMode] = useState<VisualMode>('brain');
  const isStandalone = typeof window !== 'undefined' && window.location.port === '3001';

  return (
    <div className="w-full bg-[#030712] text-slate-100 font-sans selection:bg-cyan-500/30 selection:text-cyan-200 min-h-screen">
      {/* ── TOP NAV BAR (Rendered on Standalone Port 3001 or as Sleek Subnav) ── */}
      {isStandalone && (
        <header className="sticky top-0 z-50 bg-[#030712]/90 backdrop-blur-2xl border-b border-slate-800/80 px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 bg-slate-900 border border-cyan-500/40 rounded-xl overflow-hidden flex items-center justify-center p-1 shadow-md shadow-cyan-500/20">
              <img src="/logo.png" alt="ADPilot Logo" className="w-full h-full object-contain filter drop-shadow-[0_0_6px_rgba(6,182,212,0.6)]" />
            </div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-base tracking-tight text-white">ADPilot Pro</span>
              <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-300 border border-cyan-500/30">
                v3.0 3D Enterprise
              </span>
            </div>
          </div>

          <nav className="hidden lg:flex items-center gap-5 text-xs font-mono font-semibold text-slate-400">
            <a href="#agents" className="hover:text-cyan-300 transition-colors">18 Agents</a>
            <a href="#simulator" className="hover:text-cyan-300 transition-colors">Campaign Studio</a>
            <a href="#dag" className="hover:text-cyan-300 transition-colors">3D DAG Flow</a>
            <a href="#playground" className="hover:text-cyan-300 transition-colors">ML Playground</a>
            <a href="#formulas" className="hover:text-cyan-300 transition-colors">Formulas & Proofs</a>
            <a href="#comparison" className="hover:text-cyan-300 transition-colors">Comparison</a>
          </nav>

          <div className="flex items-center gap-2.5">
            <button
              onClick={() => setIsWhitepaperOpen(true)}
              className="hidden sm:flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl text-xs font-mono font-bold bg-slate-900 border border-slate-800 text-slate-300 hover:text-white hover:border-slate-700 transition-all"
            >
              <BookOpen className="w-3.5 h-3.5 text-cyan-400" />
              <span>Whitepaper</span>
            </button>

            <a
              href="https://github.com/GhariebML/ADPilot-Pro"
              target="_blank"
              rel="noreferrer"
              className="hidden sm:flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl text-xs font-mono font-bold bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 hover:bg-cyan-500/20 transition-all"
            >
              <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
              <span>GitHub</span>
            </a>

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
      )}

      {/* ── 3D HOLOGRAPHIC GLOBAL BACKGROUND ── */}
      <ThreeHolographicGlobe
        activeMode={visualMode}
        onModeChange={setVisualMode}
        className="fixed inset-0 w-full h-full pointer-events-none z-0"
      />

      {/* ── 3D HOLOGRAPHIC HERO SECTION (PERFECTLY CENTERED) ── */}
      <section className="relative z-10 w-full py-16 sm:py-24 overflow-hidden border-b border-slate-800/60 flex flex-col items-center justify-center text-center">
        {/* Ambient Glow Orbs */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[70vw] h-[70vw] bg-radial from-cyan-500/10 via-purple-500/5 to-transparent rounded-full filter blur-[140px] pointer-events-none z-0" />

        <div className="w-full max-w-5xl mx-auto px-4 sm:px-6 relative z-10 flex flex-col items-center justify-center space-y-6 text-center">
          {/* Logo & Release Badge */}
          <div className="flex flex-col items-center gap-3">
            <div className="w-20 h-20 sm:w-24 sm:h-24 rounded-3xl bg-slate-950/80 border border-cyan-500/50 p-2.5 shadow-2xl shadow-cyan-500/20 backdrop-blur-2xl transition-transform hover:scale-105 duration-300">
              <img src="/logo.png" alt="ADPilot Pro Logo" className="w-full h-full object-contain filter drop-shadow-[0_0_15px_rgba(6,182,212,0.8)]" />
            </div>
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-slate-950/90 border border-cyan-500/40 text-xs font-mono text-cyan-300 shadow-xl shadow-cyan-500/10">
              <Sparkles className="w-4 h-4 text-cyan-400 fill-cyan-400" />
              <span>ADPilot Pro Enterprise V3 • 18-Agent Autonomous Marketing OS</span>
            </div>
          </div>

          {/* Main Headline */}
          <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-white leading-[1.1] max-w-4xl mx-auto">
            Autonomous AI <br />
            <span className="text-gradient-cyan">Marketing Operating System</span>
          </h1>

          {/* Subtitle */}
          <p className="text-sm sm:text-base lg:text-lg text-slate-300 max-w-3xl mx-auto leading-relaxed font-light">
            Orchestrating <strong>18 specialized micro-agents</strong>, <strong>PyTorch PPO Reinforcement Learning</strong>, <strong>FastEmbed BGE Hybrid RAG</strong>, and <strong>Cryptographic HMAC-SHA256 Governance</strong> in an immutable, deterministic DAG.
          </p>

          {/* 3D Hologram Interactive Mode Switcher HUD */}
          <div className="flex items-center justify-center gap-1.5 p-1 rounded-xl bg-slate-950/85 border border-slate-800 backdrop-blur-3xl shadow-xl z-20">
            <button
              onClick={() => setVisualMode('brain')}
              className={`px-3 py-1.5 rounded-lg text-xs font-mono font-bold flex items-center gap-1.5 transition-all ${
                visualMode === 'brain'
                  ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <Brain className="w-3.5 h-3.5" />
              <span>Neural Brain Core</span>
            </button>

            <button
              onClick={() => setVisualMode('globe')}
              className={`px-3 py-1.5 rounded-lg text-xs font-mono font-bold flex items-center gap-1.5 transition-all ${
                visualMode === 'globe'
                  ? 'bg-purple-500/20 text-purple-300 border border-purple-500/40 shadow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <Globe className="w-3.5 h-3.5" />
              <span>Ad Dispatch Globe</span>
            </button>

            <button
              onClick={() => setVisualMode('torus')}
              className={`px-3 py-1.5 rounded-lg text-xs font-mono font-bold flex items-center gap-1.5 transition-all ${
                visualMode === 'torus'
                  ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 shadow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <Network className="w-3.5 h-3.5" />
              <span>Quantum Gimbal</span>
            </button>
          </div>

          {/* Action CTA Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-3.5 pt-1 w-full max-w-md mx-auto">
            <a
              href="http://localhost:3000/campaigns"
              target="_blank"
              rel="noopener noreferrer"
              className="w-full sm:w-auto px-7 py-3 rounded-xl font-bold text-xs uppercase tracking-wider bg-white text-slate-950 hover:bg-slate-200 transition-all flex items-center justify-center gap-2 shadow-xl shadow-cyan-500/20 active:scale-95 cursor-pointer shrink-0"
            >
              <span>Launch Live OS</span>
              <ArrowRight className="w-4 h-4" />
            </a>

            <button
              onClick={() => setIsWhitepaperOpen(true)}
              className="w-full sm:w-auto px-7 py-3 rounded-xl font-bold text-xs uppercase tracking-wider bg-slate-950/90 border border-slate-800 hover:border-cyan-500/50 text-slate-200 hover:text-cyan-300 transition-all flex items-center justify-center gap-2 shrink-0"
            >
              <BookOpen className="w-4 h-4 text-cyan-400" />
              <span>Whitepaper</span>
            </button>

            <a
              href="http://localhost:3000/technology-stack"
              target="_blank"
              rel="noopener noreferrer"
              className="w-full sm:w-auto px-7 py-3 rounded-xl font-bold text-xs uppercase tracking-wider bg-slate-950/90 border border-slate-800 hover:border-purple-500/50 text-slate-300 hover:text-purple-300 transition-all flex items-center justify-center gap-2 shrink-0"
            >
              <Cpu className="w-4 h-4 text-purple-400" />
              <span>Architecture</span>
            </a>
          </div>

          {/* Quick Metrics Grid (Centered 4-Column Layout) */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3.5 pt-6 w-full max-w-4xl mx-auto">
            {[
              { val: '18 Agents', lbl: 'Deterministic DAG Fleet', color: 'text-cyan-400', border: 'border-cyan-500/30' },
              { val: '+28.7% ROAS', lbl: 'PPO Policy Alpha Return', color: 'text-emerald-400', border: 'border-emerald-500/30' },
              { val: '384-dim RAG', lbl: 'FastEmbed BGE + BM25 RRF', color: 'text-purple-400', border: 'border-purple-500/30' },
              { val: 'HMAC-SHA256', lbl: 'Cryptographic HITL Gate', color: 'text-amber-400', border: 'border-amber-500/30' },
            ].map((m, idx) => (
              <TiltCard3D key={idx} maxTilt={8} className="h-full">
                <div className={`p-4 rounded-2xl bg-slate-950/85 border ${m.border} text-center backdrop-blur-3xl h-full flex flex-col justify-center`}>
                  <div className={`text-xl sm:text-2xl font-mono font-extrabold ${m.color}`}>{m.val}</div>
                  <div className="text-[10px] text-slate-400 font-mono mt-0.5">{m.lbl}</div>
                </div>
              </TiltCard3D>
            ))}
          </div>
        </div>
      </section>

      {/* â”€â”€ MODULE 1: IN-SHOWCASE LIVE CAMPAIGN STUDIO â”€â”€ */}
      <section id="simulator" className="py-16 border-b border-slate-800/60 bg-slate-950/10 backdrop-blur-sm relative z-10">
        <div className="max-w-6xl mx-auto px-6 space-y-8">
          <div className="text-center space-y-2">
            <h2 className="text-2xl sm:text-4xl font-extrabold text-white">
              Instant <span className="text-gradient-cyan">In-Showcase Campaign Studio</span>
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 max-w-2xl mx-auto">
              Select an industry vertical to generate live multi-channel copy, visual color palettes, and predictive ROAS metrics.
            </p>
          </div>

          <LiveCampaignSimulatorStudio />
        </div>
      </section>

      {/* â”€â”€ MODULE 2: INTERACTIVE 3D DAG PIPELINE FLOW â”€â”€ */}
      <section id="dag" className="py-16 border-b border-slate-800/60 relative z-10">
        <div className="max-w-6xl mx-auto px-6 space-y-8">
          <div className="text-center space-y-2">
            <h2 className="text-2xl sm:text-4xl font-extrabold text-white">
              7-Stage <span className="text-gradient-cyan">Deterministic 3D Pipeline</span>
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 max-w-2xl mx-auto">
              Simulate end-to-end state transitions across Ingestion, Strategy, RAG, Creative, Vision, PPO Optimizer, and Cryptographic Gate.
            </p>
          </div>

          <InteractiveDAG3D />
        </div>
      </section>

      {/* â”€â”€ MODULE 3: 18-AGENT MATRIX & CONTRACT ENCYCLOPEDIA â”€â”€ */}
      <section id="agents" className="py-16 border-b border-slate-800/60 bg-slate-950/10 backdrop-blur-sm relative z-10">
        <div className="max-w-6xl mx-auto px-6 space-y-8">
          <div className="text-center space-y-2">
            <h2 className="text-2xl sm:text-4xl font-extrabold text-white">
              18-Stage <span className="text-gradient-cyan">Master Agent Fleet & Contracts</span>
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 max-w-2xl mx-auto">
              Complete directory of all 18 micro-agents with Pydantic v2 schemas, model engines, and deterministic fallback protocols.
            </p>
          </div>

          <All18AgentsMatrix />
        </div>
      </section>

      {/* â”€â”€ MODULE 4: NEURAL ML & RL PLAYGROUND â”€â”€ */}
      <section id="playground" className="py-16 border-b border-slate-800/60 relative z-10">
        <div className="max-w-6xl mx-auto px-6 space-y-8">
          <div className="text-center space-y-2">
            <h2 className="text-2xl sm:text-4xl font-extrabold text-white">
              Interactive <span className="text-gradient-cyan">Neural ML & RL Models</span>
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 max-w-2xl mx-auto">
              Test live parameter sweeps against our PyTorch PPO Policy Network, Ridge Revenue Forecaster, and CLIP-ViT visual quality engine.
            </p>
          </div>

          <NeuralMLPlayground />
        </div>
      </section>

      {/* â”€â”€ MODULE 5: MATHEMATICAL FORMULAS & FORMAL PROOFS â”€â”€ */}
      <section id="formulas" className="py-16 border-b border-slate-800/60 bg-slate-950/10 backdrop-blur-sm relative z-10">
        <div className="max-w-6xl mx-auto px-6 space-y-8">
          <div className="text-center space-y-2">
            <h2 className="text-2xl sm:text-4xl font-extrabold text-white">
              Mathematical <span className="text-gradient-cyan">Formulas & Formal Proofs</span>
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 max-w-2xl mx-auto">
              Explore the exact mathematical equations governing PPO clipped surrogate loss, Dirichlet simplex bounds, and RRF k=60 fusion.
            </p>
          </div>

          <MathematicalFormulasDeepDive />
        </div>
      </section>

      {/* â”€â”€ MODULE 6: DUAL-STREAM HYBRID RAG 3D â”€â”€ */}
      <section id="rag" className="py-16 border-b border-slate-800/60 relative z-10">
        <div className="max-w-6xl mx-auto px-6 space-y-8">
          <div className="text-center space-y-2">
            <h2 className="text-2xl sm:text-4xl font-extrabold text-white">
              Dual-Stream <span className="text-gradient-cyan">Hybrid RAG Knowledge Engine</span>
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 max-w-2xl mx-auto">
              FastEmbed BGE 384-dimensional dense semantic vectors fused with BM25 Okapi lexical scoring via Reciprocal Rank Fusion (k=60).
            </p>
          </div>

          <RAGVectorSpace3D />
        </div>
      </section>

      {/* â”€â”€ MODULE 7: ENTERPRISE COMPARISON MATRIX â”€â”€ */}
      <section id="comparison" className="py-16 border-b border-slate-800/60 bg-slate-950/10 backdrop-blur-sm relative z-10">
        <div className="max-w-6xl mx-auto px-6 space-y-8">
          <div className="text-center space-y-2">
            <h2 className="text-2xl sm:text-4xl font-extrabold text-white">
              Enterprise <span className="text-gradient-cyan">Capability Comparison</span>
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 max-w-2xl mx-auto">
              Comparing architectural determinism, reinforcement learning, and governance against manual agencies and legacy AI tools.
            </p>
          </div>

          <EnterpriseComparisonMatrix />
        </div>
      </section>

      {/* â”€â”€ MODULE 8: ROADMAP & 100% PROOF â”€â”€ */}
      <section id="roadmap" className="py-16 border-b border-slate-800/60 relative z-10">
        <div className="max-w-4xl mx-auto px-6 space-y-8">
          <div className="text-center space-y-2">
            <h2 className="text-2xl sm:text-4xl font-extrabold text-white">
              Engineering <span className="text-gradient-cyan">Milestone Roadmap</span>
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 max-w-xl mx-auto">
              Exhaustive milestone verification with 271 automated tests passing in production CI/CD.
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

      {/* â”€â”€ FOOTER â”€â”€ */}
      <footer className="py-12 bg-slate-950/20 backdrop-blur-md border-t border-slate-800/80 px-6 relative z-10">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6 text-xs font-mono text-slate-500">
          <div className="flex items-center gap-3">
            <div className="w-7 h-7 bg-slate-900 border border-cyan-500/40 rounded-lg overflow-hidden flex items-center justify-center p-0.5 shadow-sm">
              <img src="/logo.png" alt="ADPilot Logo" className="w-full h-full object-contain" />
            </div>
            <span>© 2026 ADPilot Pro — Autonomous Marketing Operating System</span>
          </div>

          <div className="flex items-center gap-6">
            <button onClick={() => setIsWhitepaperOpen(true)} className="hover:text-cyan-300 transition-colors">
              Technical Whitepaper
            </button>
            <a href="http://localhost:3000/technology-stack" className="hover:text-cyan-300 transition-colors">
              Architecture Board
            </a>
            <a href="https://github.com/GhariebML/ADPilot-Pro" className="hover:text-cyan-300 transition-colors">
              GitHub Repository
            </a>
            <a href="http://localhost:3000/campaigns" className="hover:text-cyan-300 transition-colors">
              Live Dashboard
            </a>
          </div>
        </div>
      </footer>

      {/* â”€â”€ IN-APP TECHNICAL WHITEPAPER MODAL â”€â”€ */}
      <TechnicalWhitepaperModal
        isOpen={isWhitepaperOpen}
        onClose={() => setIsWhitepaperOpen(false)}
      />
    </div>
  );
};

export default ShowcaseLandingView;

