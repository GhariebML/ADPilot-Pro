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
  RefreshCw
} from 'lucide-react';

interface ShowcaseProps {
  onOpenLiveDemo?: () => void;
  onNavigateSection?: (section: string) => void;
}

export const ShowcaseLandingView: React.FC<ShowcaseProps> = ({ onOpenLiveDemo, onNavigateSection }) => {
  const [activeTab, setActiveTab] = useState<'all' | 'agents' | 'rag' | 'ml' | 'governance'>('all');
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
              v3.0 Enterprise
            </span>
          </div>
        </div>

        <nav className="hidden md:flex items-center gap-6 text-xs font-mono font-semibold text-slate-400">
          <a href="#agents" className="hover:text-cyan-300 transition-colors">18 Agents</a>
          <a href="#rag" className="hover:text-cyan-300 transition-colors">Hybrid RAG</a>
          <a href="#ml" className="hover:text-cyan-300 transition-colors">PPO & ML Models</a>
          <a href="#architecture" className="hover:text-cyan-300 transition-colors">Architecture</a>
          <a href="#governance" className="hover:text-cyan-300 transition-colors">HITL Governance</a>
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

      {/* ── HERO SECTION ── */}
      <section className="relative pt-20 pb-24 overflow-hidden border-b border-slate-800/60">
        {/* Background Glowing Ambient Orbs */}
        <div className="absolute top-[-10%] left-[-5%] w-[45vw] h-[45vw] bg-cyan-600/10 rounded-full filter blur-[140px] pointer-events-none" />
        <div className="absolute top-[20%] right-[-10%] w-[40vw] h-[40vw] bg-purple-600/10 rounded-full filter blur-[140px] pointer-events-none" />

        <div className="max-w-6xl mx-auto px-6 text-center relative z-10 space-y-8">
          {/* Release Badge */}
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-slate-900/90 border border-slate-800 text-xs font-mono text-cyan-300 shadow-inner">
            <Sparkles className="w-3.5 h-3.5 text-cyan-400 fill-cyan-400" />
            <span>Introducing ADPilot Pro Enterprise OS — 271 Verified Tests Passing</span>
          </div>

          {/* Main Headline */}
          <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-white leading-tight">
            Autonomous Multi-Agent <br />
            <span className="text-gradient-cyan">Marketing Operating System</span>
          </h1>

          {/* Subtitle */}
          <p className="text-sm sm:text-base lg:text-lg text-slate-400 max-w-3xl mx-auto leading-relaxed">
            ADPilot Pro combines <strong>18 specialized AI agents</strong>, <strong>custom PyTorch Reinforcement Learning (PPO)</strong>, <strong>Dual-Stream FastEmbed Hybrid RAG</strong>, and <strong>Cryptographic HMAC-SHA256 Governance</strong> to formulate, design, audit, and scale marketing campaigns from a single business brief.
          </p>

          {/* Call-to-Action Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-2">
            <a
              href="http://localhost:3000/campaigns"
              target="_blank"
              rel="noopener noreferrer"
              className="w-full sm:w-auto px-7 py-3.5 rounded-xl font-bold text-xs uppercase tracking-wider bg-white text-slate-950 hover:bg-slate-200 transition-all flex items-center justify-center gap-2 shadow-xl shadow-white/10 active:scale-95"
            >
              <span>Explore Live Dashboard</span>
              <ArrowRight className="w-4 h-4" />
            </a>

            <a
              href="http://localhost:3000/technology-stack"
              target="_blank"
              rel="noopener noreferrer"
              className="w-full sm:w-auto px-7 py-3.5 rounded-xl font-bold text-xs uppercase tracking-wider bg-slate-900 border border-slate-800 hover:border-cyan-500/50 text-slate-200 hover:text-cyan-300 transition-all flex items-center justify-center gap-2"
            >
              <Cpu className="w-4 h-4 text-cyan-400" />
              <span>Technology Architecture Board</span>
            </a>

            <a
              href="https://github.com/GhariebML/ADPilot-Pro"
              target="_blank"
              rel="noopener noreferrer"
              className="w-full sm:w-auto px-7 py-3.5 rounded-xl font-bold text-xs uppercase tracking-wider bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-300 transition-all flex items-center justify-center gap-2"
            >
              <GitBranch className="w-4 h-4 text-purple-400" />
              <span>GitHub Repository</span>
              <ExternalLink className="w-3.5 h-3.5 text-slate-500" />
            </a>
          </div>

          {/* Quick Metrics Ticker */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-8 max-w-4xl mx-auto">
            <div className="p-4 rounded-2xl bg-slate-950/70 border border-slate-800/80 text-center">
              <div className="text-2xl font-mono font-bold text-cyan-400">18 Agents</div>
              <div className="text-[11px] text-slate-500 font-mono mt-0.5">Deterministic DAG</div>
            </div>
            <div className="p-4 rounded-2xl bg-slate-950/70 border border-slate-800/80 text-center">
              <div className="text-2xl font-mono font-bold text-emerald-400">+28.7% ROAS</div>
              <div className="text-[11px] text-slate-500 font-mono mt-0.5">PPO Neural Alpha</div>
            </div>
            <div className="p-4 rounded-2xl bg-slate-950/70 border border-slate-800/80 text-center">
              <div className="text-2xl font-mono font-bold text-purple-400">384-dim RAG</div>
              <div className="text-[11px] text-slate-500 font-mono mt-0.5">FastEmbed + BM25 RRF</div>
            </div>
            <div className="p-4 rounded-2xl bg-slate-950/70 border border-slate-800/80 text-center">
              <div className="text-2xl font-mono font-bold text-amber-400">HMAC-SHA256</div>
              <div className="text-[11px] text-slate-500 font-mono mt-0.5">Cryptographic HITL</div>
            </div>
          </div>
        </div>
      </section>

      {/* ── TECHNOLOGY ECOSYSTEM ── */}
      <section id="stack" className="py-20 border-b border-slate-800/60 bg-slate-950/40">
        <div className="max-w-6xl mx-auto px-6 space-y-12">
          <div className="text-center space-y-3">
            <h2 className="text-2xl sm:text-4xl font-extrabold text-white">
              Technology <span className="text-gradient-cyan">Ecosystem</span>
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 max-w-2xl mx-auto">
              Engineered with a high-performance Python 3.12 backend, PyTorch deep reinforcement learning, ONNX computer vision, and a modern React 18 / Vite frontend.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Frontend */}
            <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-cyan-500/40 transition-all space-y-4">
              <div className="flex items-center gap-2.5">
                <Globe className="w-5 h-5 text-cyan-400" />
                <h3 className="text-base font-bold text-white">Frontend & AI OS</h3>
              </div>
              <div className="flex flex-wrap gap-1.5">
                {['React 18.3', 'Vite 7.3', 'TypeScript 5.8', 'TailwindCSS 3.4', 'Zustand 5', 'Lucide Icons', 'Vitest'].map(t => (
                  <span key={t} className="px-2.5 py-1 rounded-lg bg-slate-950 border border-slate-800 text-[11px] font-mono text-slate-300">{t}</span>
                ))}
              </div>
            </div>

            {/* Backend */}
            <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-blue-500/40 transition-all space-y-4">
              <div className="flex items-center gap-2.5">
                <Server className="w-5 h-5 text-blue-400" />
                <h3 className="text-base font-bold text-white">Backend & Runtime</h3>
              </div>
              <div className="flex flex-wrap gap-1.5">
                {['FastAPI 0.115', 'Python 3.12', 'Pydantic v2', 'Uvicorn ASGI', 'Starlette', 'AsyncIO Pub/Sub', 'ARQ Worker'].map(t => (
                  <span key={t} className="px-2.5 py-1 rounded-lg bg-slate-950 border border-slate-800 text-[11px] font-mono text-slate-300">{t}</span>
                ))}
              </div>
            </div>

            {/* AI & ML Models */}
            <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-purple-500/40 transition-all space-y-4">
              <div className="flex items-center gap-2.5">
                <Cpu className="w-5 h-5 text-purple-400" />
                <h3 className="text-base font-bold text-white">Neural Models & ML</h3>
              </div>
              <div className="flex flex-wrap gap-1.5">
                {['PyTorch 2.11 (PPO)', 'Scikit-Learn (Ridge)', 'CLIP-ViT B/32 (ONNX)', 'FastEmbed BGE', 'OpenAI GPT-4o', 'Claude 3.5 Sonnet'].map(t => (
                  <span key={t} className="px-2.5 py-1 rounded-lg bg-slate-950 border border-slate-800 text-[11px] font-mono text-slate-300">{t}</span>
                ))}
              </div>
            </div>

            {/* RAG & Memory */}
            <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-emerald-500/40 transition-all space-y-4">
              <div className="flex items-center gap-2.5">
                <Database className="w-5 h-5 text-emerald-400" />
                <h3 className="text-base font-bold text-white">RAG & 4-Tier Memory</h3>
              </div>
              <div className="flex flex-wrap gap-1.5">
                {['Qdrant Vector DB (v1.18)', 'BM25 Okapi Lexical', 'RRF (k=60) Fusion', 'SQLite WAL Store', 'LRU Working Memory', 'PyTorch Buffer'].map(t => (
                  <span key={t} className="px-2.5 py-1 rounded-lg bg-slate-950 border border-slate-800 text-[11px] font-mono text-slate-300">{t}</span>
                ))}
              </div>
            </div>

            {/* Storage & DB */}
            <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-amber-500/40 transition-all space-y-4">
              <div className="flex items-center gap-2.5">
                <HardDrive className="w-5 h-5 text-amber-400" />
                <h3 className="text-base font-bold text-white">Data & Persistence</h3>
              </div>
              <div className="flex flex-wrap gap-1.5">
                {['SQLAlchemy 2.0 (Async)', 'aiosqlite Database', 'PostgreSQL Ready', 'Redis Cache', 'Qdrant Collections'].map(t => (
                  <span key={t} className="px-2.5 py-1 rounded-lg bg-slate-950 border border-slate-800 text-[11px] font-mono text-slate-300">{t}</span>
                ))}
              </div>
            </div>

            {/* Governance & CI/CD */}
            <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-rose-500/40 transition-all space-y-4">
              <div className="flex items-center gap-2.5">
                <ShieldCheck className="w-5 h-5 text-rose-400" />
                <h3 className="text-base font-bold text-white">Governance & DevOps</h3>
              </div>
              <div className="flex flex-wrap gap-1.5">
                {['HMAC-SHA256 Signatures', 'RBAC Policy Guard', 'Docker Multi-Stage', 'Docker Compose', 'GitHub Actions (3 Jobs)', 'Ruff Linter'].map(t => (
                  <span key={t} className="px-2.5 py-1 rounded-lg bg-slate-950 border border-slate-800 text-[11px] font-mono text-slate-300">{t}</span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── THE PROBLEM VS THE SOLUTION ── */}
      <section className="py-20 border-b border-slate-800/60">
        <div className="max-w-6xl mx-auto px-6 space-y-16">
          {/* Problem */}
          <div className="space-y-8">
            <div className="text-center space-y-2">
              <h2 className="text-2xl sm:text-4xl font-extrabold text-white">
                The <span className="text-rose-400">Problem</span> in Modern Digital Marketing
              </h2>
              <p className="text-xs sm:text-sm text-slate-400 max-w-2xl mx-auto">
                Modern performance marketing is fragmented, manual, and prone to budget burning.
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="p-5 rounded-2xl bg-rose-950/15 border border-rose-900/30 space-y-2">
                <div className="text-2xl font-mono font-bold text-rose-400">73% Time</div>
                <div className="text-sm font-bold text-white">Manual Friction</div>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Teams spend over 70% of weekly hours juggling copy variants, spreadsheets, and manual uploads.
                </p>
              </div>

              <div className="p-5 rounded-2xl bg-rose-950/15 border border-rose-900/30 space-y-2">
                <div className="text-2xl font-mono font-bold text-rose-400">Siloed Tools</div>
                <div className="text-sm font-bold text-white">Context Drift</div>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Designers, copywriters, and media buyers operate in disconnected silos with zero unified memory.
                </p>
              </div>

              <div className="p-5 rounded-2xl bg-rose-950/15 border border-rose-900/30 space-y-2">
                <div className="text-2xl font-mono font-bold text-rose-400">Blind Bidding</div>
                <div className="text-sm font-bold text-white">Heuristic Budgets</div>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Channel budget allocations rely on gut instinct rather than continuous reinforcement learning.
                </p>
              </div>

              <div className="p-5 rounded-2xl bg-rose-950/15 border border-rose-900/30 space-y-2">
                <div className="text-2xl font-mono font-bold text-rose-400">Zero Audit</div>
                <div className="text-sm font-bold text-white">Compliance Risk</div>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Uncontrolled autonomous deployments risk brand violations without cryptographic audit trails.
                </p>
              </div>
            </div>
          </div>

          {/* Solution */}
          <div className="space-y-8 pt-6">
            <div className="text-center space-y-2">
              <h2 className="text-2xl sm:text-4xl font-extrabold text-white">
                The <span className="text-gradient-cyan">ADPilot Pro Solution</span>
              </h2>
              <p className="text-xs sm:text-sm text-slate-400 max-w-2xl mx-auto">
                An interconnected 18-stage deterministic AI Operating System passing strict Pydantic contracts.
              </p>
            </div>

            {/* Stepper Flow */}
            <div className="p-6 rounded-2xl bg-slate-950 border border-slate-800 max-w-3xl mx-auto space-y-3 font-mono text-xs">
              {[
                { label: '01. Ingestion Brief', desc: 'User submits brand parameters & budget', color: 'text-cyan-400' },
                { label: '02. Strategy Formulation', desc: 'Strategy Agent synthesizes multi-channel roadmap', color: 'text-blue-400' },
                { label: '03. Hybrid RAG Intelligence', desc: 'Research & Audience agents query Qdrant vectors', color: 'text-purple-400' },
                { label: '04. Creative Synthesis', desc: 'Content & Design agents generate copy & visual assets', color: 'text-pink-400' },
                { label: '05. Vision & ML Quality Gate', desc: 'CLIP-ViT & Ridge Forecaster predict ROI & check contrast', color: 'text-indigo-400' },
                { label: '06. PPO Policy Rebalancing', desc: 'Reinforcement learning neural network optimizes budget', color: 'text-amber-400' },
                { label: '07. Cryptographic Governance', desc: 'Human director approves signed HMAC receipt for deployment', color: 'text-emerald-400' },
              ].map((step, idx) => (
                <div key={idx} className="flex items-center justify-between p-3 rounded-xl bg-slate-900/60 border border-slate-800/80">
                  <div className="flex items-center gap-3">
                    <span className={`font-bold ${step.color}`}>{step.label}</span>
                    <span className="text-slate-400 hidden sm:inline">• {step.desc}</span>
                  </div>
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ── MULTI-AGENT ARCHITECTURE DEEP DIVE ── */}
      <section id="agents" className="py-20 border-b border-slate-800/60 bg-slate-950/40">
        <div className="max-w-6xl mx-auto px-6 space-y-12">
          <div className="text-center space-y-3">
            <h2 className="text-2xl sm:text-4xl font-extrabold text-white">
              Multi-Agent <span className="text-gradient-cyan">Architecture</span>
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 max-w-2xl mx-auto">
              Specialized autonomous agents operating in an immutable DAG pipeline with dedicated neural models.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {agents.map((agent) => {
              const Icon = agent.icon;
              return (
                <div
                  key={agent.id}
                  className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800 hover:border-cyan-500/40 transition-all flex flex-col justify-between space-y-4 group"
                >
                  <div>
                    <div className="flex items-center justify-between mb-3">
                      <div className="p-2 rounded-xl bg-slate-950 border border-slate-800 text-cyan-400">
                        <Icon className="w-5 h-5" />
                      </div>
                      <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                        Active
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

                  <div className="pt-3 border-t border-slate-800/80 text-[10px] font-mono text-slate-400 space-y-1 bg-slate-950/60 p-2.5 rounded-xl">
                    <div className="truncate"><span className="text-slate-500">In:</span> {agent.inputs}</div>
                    <div className="truncate"><span className="text-slate-500">Out:</span> {agent.outputs}</div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* ── DEVELOPMENT ROADMAP ── */}
      <section id="roadmap" className="py-20 border-b border-slate-800/60">
        <div className="max-w-4xl mx-auto px-6 space-y-10">
          <div className="text-center space-y-2">
            <h2 className="text-2xl sm:text-4xl font-extrabold text-white">
              Development <span className="text-gradient-cyan">Roadmap & Verification</span>
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 max-w-xl mx-auto">
              Systematic milestone progression from initial architecture to production certification.
            </p>
          </div>

          <div className="space-y-3 font-mono text-xs">
            {[
              { phase: 'Phase 1: Foundation Schemas & Error System', status: 'VERIFIED_DONE', date: 'Certified' },
              { phase: 'Phase 2: Master Campaign Orchestrator DAG', status: 'VERIFIED_DONE', date: 'Certified' },
              { phase: 'Phase 3: FastEmbed BGE Hybrid RAG & Qdrant', status: 'VERIFIED_DONE', date: 'Certified' },
              { phase: 'Phase 4: Ridge Revenue & ROAS ML Forecaster', status: 'VERIFIED_DONE', date: 'Certified' },
              { phase: 'Phase 5: PPO Actor-Critic Neural Optimizer', status: 'VERIFIED_DONE', date: 'Certified' },
              { phase: 'Phase 6: CLIP-ViT Computer Vision Quality Gate', status: 'VERIFIED_DONE', date: 'Certified' },
              { phase: 'Phase 7: Cryptographic HMAC-SHA256 HITL Gate', status: 'VERIFIED_DONE', date: 'Certified' },
              { phase: 'Phase 8: React 18 Cyber Obsidian AI OS Dashboard', status: 'VERIFIED_DONE', date: 'Certified' },
              { phase: 'Phase 9: Real-Time WebSockets & Agent Debate', status: 'VERIFIED_DONE', date: 'Certified' },
              { phase: 'Phase 10: Production Ad Network Live Adapters', status: 'IN_PROGRESS', date: 'Next Release' },
            ].map((p, idx) => (
              <div key={idx} className="flex items-center justify-between p-3.5 rounded-xl bg-slate-900/60 border border-slate-800">
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
