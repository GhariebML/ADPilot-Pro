import './App.css'
import { useState, useEffect, useCallback } from 'react'
import { Routes, Route, useNavigate, useLocation, Navigate } from 'react-router-dom'
import { CampaignBriefForm } from './components/CampaignBriefForm'
import { LiveOrchestration } from './components/LiveOrchestration'
import { ResultDisplay } from './components/ResultDisplay'
import { StrategyView, ResearchView, SavedView, SettingsView, DashboardView, AnalyticsView } from './components/SidebarViews'
import { CampaignControlBar } from './components/CampaignControlBar'
import { InteractivePipelineDAG } from './components/InteractivePipelineDAG'
import { AgentObservatory } from './components/AgentObservatory'
import { AgentDetailDrawer } from './components/AgentDetailDrawer'
import { IOInspectorModal } from './components/IOInspectorModal'
import { HITLApprovalCenter } from './components/HITLApprovalCenter'
import { OptimizerDashboard } from './components/OptimizerDashboard'
import { ModelRegistryView } from './components/ModelRegistryView'
import { CreativeStudioView } from './components/CreativeStudioView'
import { CampaignTimelineView } from './components/CampaignTimelineView'
import { SystemHealthView } from './components/SystemHealthView'
import { KnowledgeBaseView } from './components/KnowledgeBaseView'
import { LiveActivityFeed } from './components/LiveActivityFeed'
import { CommandPalette } from './components/CommandPalette'
import { InteractiveDemoModal } from './components/InteractiveDemoModal'
import { TechnologyStackView } from './components/TechnologyStackView'
import { ShowcaseLandingView } from './components/ShowcaseLandingView'
import { CampaignSimulationView } from './components/simulation/CampaignSimulationView'
import { MASTER_AGENTS } from './data/agentContracts'
import { useTaskPolling } from './hooks/useTaskPolling'
import { campaignService } from './services/api'
import { useAppStore } from './store/useAppStore'
import type { ContentOutput, AgentContract, AIActivityEvent, CampaignBrief } from './types'
import {
  Compass,
  Search,
  FileText,
  Palette,
  BarChart3,
  Zap,
  ShieldCheck,
  Activity,
  Box,
  BookOpen,
  Settings as SettingsIcon,
  Bell,
  User,
  Plus,
  LayoutDashboard,
  Layers,
  Sparkles,
  Command,
  Clock,
  CheckCircle2,
  Cpu
} from 'lucide-react'

function App() {
  const navigate = useNavigate()
  const location = useLocation()
  
  // Zustand Global State
  const { 
    activeAgent, setActiveAgent, 
    currentTaskId, setCurrentTaskId, 
    theme, toggleTheme 
  } = useAppStore()

  // Local State
  const [campaignId, setCampaignId] = useState<string | null>(null)
  const [campaignBrief, setCampaignBrief] = useState<CampaignBrief | null>({
    businessName: 'AI Growth Engine',
    productName: 'AI SaaS Platform',
    productDescription: 'Autonomous B2B marketing optimization and lead generation platform for high-growth SaaS.',
    targetAudience: 'Small and medium businesses, SaaS founders, Growth Marketers',
    goals: ['lead_generation', 'sales_conversion'],
    budget: 10000,
    duration: '30 Days',
    tone: 'professional'
  })
  const [results, setResults] = useState<ContentOutput | null>(null)
  const [isDownloading, setIsDownloading] = useState(false)

  // Modals and Drawers state
  const [selectedAgentForDrawer, setSelectedAgentForDrawer] = useState<AgentContract | null>(null)
  const [selectedAgentForIO, setSelectedAgentForIO] = useState<AgentContract | null>(null)
  const [isActivityFeedOpen, setIsActivityFeedOpen] = useState(false)
  const [isCommandPaletteOpen, setIsCommandPaletteOpen] = useState(false)
  const [isDemoModalOpen, setIsDemoModalOpen] = useState(false)

  // Live Activity Events Stream
  const [activityEvents] = useState<AIActivityEvent[]>([
    { id: '1', timestamp: '18:39:13', agent: 'Context Builder', action: 'SCHEMA_VALIDATED', level: 'info', details: 'Validated B2B SaaS brief parameters.', latency: '2.1ms' },
    { id: '2', timestamp: '18:39:14', agent: 'Strategy Agent', action: 'SYNTHESIS_COMPLETE', level: 'success', details: 'Formulated 3-channel allocation plan (LinkedIn 45%, Meta 35%, Google 20%).', latency: '1420ms' },
    { id: '3', timestamp: '18:39:15', agent: 'Research Agent', action: 'RAG_RETRIEVED', level: 'info', details: 'Dense + BM25 Hybrid RRF matched top 3 ICP psychological purchase drivers.', latency: '820ms' },
    { id: '4', timestamp: '18:39:16', agent: 'Content Agent', action: 'COPY_SCORING', level: 'success', details: 'Ridge ML Copy Evaluator scored 8 ad variants (5.43/10 Quality Score).', latency: '1980ms' },
    { id: '5', timestamp: '18:39:18', agent: 'Design Agent', action: 'CANVAS_RENDERED', level: 'info', details: 'Nano Banana Studio created 4 multi-aspect ratio visual assets.', latency: '2450ms' },
    { id: '6', timestamp: '18:39:20', agent: 'CV Agent', action: 'CLIP_QUALITY_PASS', level: 'success', details: 'CLIP-ViT zero-shot visual aesthetic verified (8.7/10). Safe margins: 100%.', latency: '410ms' },
    { id: '7', timestamp: '18:39:21', agent: 'Analytics Agent', action: 'FORECAST_COMPUTED', level: 'info', details: 'Predictive Ridge Model estimated 3.84x ROAS, $42.10 CAC.', latency: '310ms' },
    { id: '8', timestamp: '18:39:21', agent: 'PPO Optimizer', action: 'ACTION_POLICY_EMITTED', level: 'success', details: 'Neural policy rebalanced budget (+12% LinkedIn) under constraint guards.', latency: '290ms' },
    { id: '9', timestamp: '18:39:22', agent: 'HITL Gate', action: 'HUMAN_APPROVAL_RECORDED', level: 'success', details: 'Campaign Director authorized live multi-channel deployment.', latency: '50ms' }
  ])

  // Custom OS active section Ã¢â‚¬â€ defaults to showcase on dedicated showcase port (3001) or /showcase
  const isShowcasePort = typeof window !== 'undefined' && window.location.port === '3001'
  const [activeOSSection, setActiveOSSection] = useState<string>(isShowcasePort ? 'showcase' : 'pipeline')

  // Theme Sync
  useEffect(() => {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
    localStorage.setItem('theme', theme)
  }, [theme])

  // Sync URL Path with active OS view
  useEffect(() => {
    const path = location.pathname.toLowerCase()
    const isShowcase = typeof window !== 'undefined' && window.location.port === '3001'
    if (path === '/showcase' || (isShowcase && (path === '/' || path === '/campaigns'))) {
      setActiveOSSection('showcase')
    } else if (path === '/technology-stack' || path === '/technologies' || path === '/tech-stack') {
      setActiveOSSection('techstack')
    } else if (path === '/dashboard') {
      setActiveOSSection('dashboard')
    }
  }, [location.pathname])

  // React Query Task Polling
  const { status, loading, error } = useTaskPolling(currentTaskId)

  const handleBriefSubmit = (taskId: string) => {
    setCurrentTaskId(taskId)
    setCampaignId(taskId)
    setResults(null)
    setActiveOSSection('pipeline')
  }

  const handleNewCampaign = () => {
    setCurrentTaskId(null)
    setCampaignId(null)
    setResults(null)
    setActiveAgent('content')
    setActiveOSSection('brief')
    navigate('/campaigns')
  }

  const handleTaskComplete = useCallback(async () => {
    if (campaignId && status?.status === 'completed' && !results) {
      try {
        const content = await campaignService.getCampaignContent(campaignId)
        setResults(content)
      } catch (err) {
        console.error('Failed to fetch results:', err)
      }
    }
  }, [campaignId, status, results])

  useEffect(() => {
    if (status?.status === 'completed' && !results) {
      handleTaskComplete()
    }
  }, [status, results, handleTaskComplete])

  const handleDownloadAssets = async () => {
    if (!campaignId) return
    setIsDownloading(true)
    try {
      await new Promise(resolve => setTimeout(resolve, 1500))
      const blob = await campaignService.downloadDesignAssets(campaignId)
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `campaign-${campaignId}-assets.zip`
      link.click()
      window.URL.revokeObjectURL(url)
    } catch (err) {
      console.error('Failed to download assets:', err)
    } finally {
      setIsDownloading(false)
    }
  }

  const getSectionMeta = (sec: string) => {
    switch (sec) {
      case 'dashboard': return { title: 'Executive Dashboard & Intelligence', icon: LayoutDashboard, tag: 'Live Metrics' };
      case 'brief': return { title: 'Campaign Ingestion & Synthesis Brief', icon: FileText, tag: 'Step 1 of 18' };
      case 'simulation': return { title: 'End-to-End Multi-Agent Simulation', icon: Activity, tag: 'Deterministic' };
      case 'pipeline': return { title: 'Interactive Master Pipeline (DAG 3.0)', icon: Layers, tag: '18 Agents' };
      case 'agents': return { title: 'AI Agent Center & Contract Observatory', icon: Compass, tag: 'Zero Hallucination' };
      case 'creative': return { title: 'Nano Banana Creative Studio & Diffusion', icon: Palette, tag: 'Multi-Format' };
      case 'optimizer': return { title: 'RL Policy Optimizer (Continuous PPO)', icon: Zap, tag: 'PyTorch Active' };
      case 'knowledge': return { title: 'Knowledge Base & Multi-Tier Vector Memory', icon: BookOpen, tag: 'Hybrid RAG' };
      case 'hitl': return { title: 'Human-in-the-Loop Approval & Governance', icon: ShieldCheck, tag: 'Gate Control' };
      case 'timeline': return { title: 'Campaign Event Timeline & State Audit', icon: Clock, tag: 'Audit Log' };
      case 'showcase': return { title: 'Enterprise Showcase & 3D Visualizer', icon: Sparkles, tag: 'v3.0 3D' };
      case 'techstack': return { title: 'Technology Stack & Architecture Deep Dive', icon: Cpu, tag: 'Full Stack' };
      case 'models': return { title: 'ML & Neural Policy Model Registry', icon: Box, tag: 'Checkpoints' };
      case 'health': return { title: 'Platform Diagnostics & System Health', icon: Activity, tag: '100% Online' };
      case 'settings': return { title: 'System Configuration & Preferences', icon: SettingsIcon, tag: 'Config' };
      default: return { title: 'Enterprise AI Campaign OS', icon: Cpu, tag: 'v3.0' };
    }
  };

  const currentMeta = getSectionMeta(activeOSSection);
  const CurrentIcon = currentMeta.icon;

  return (
    <div className="flex h-screen bg-[#030712] overflow-hidden text-slate-100 font-sans transition-colors duration-500 relative selection:bg-cyan-500/30 selection:text-cyan-200">
      {/* Dynamic Ambient Mesh Glows */}
      <div className="absolute top-[-10%] left-[-10%] w-[45vw] h-[45vw] bg-cyan-600/10 rounded-full mix-blend-screen filter blur-[140px] pointer-events-none" />
      <div className="absolute top-[25%] right-[-10%] w-[40vw] h-[40vw] bg-purple-600/10 rounded-full mix-blend-screen filter blur-[140px] pointer-events-none" />
      <div className="absolute bottom-[-10%] left-[30%] w-[50vw] h-[50vw] bg-blue-600/10 rounded-full mix-blend-screen filter blur-[160px] pointer-events-none" />

      {/* ── Enterprise AI OS Sidebar Navigation ── */}
      <aside className="w-[265px] bg-[#07090e]/80 border-r border-white/[0.08] flex flex-col z-30 shrink-0 backdrop-blur-3xl shadow-2xl shadow-black/80">
        {/* Brand Header */}
        <div className="p-4 flex items-center justify-between border-b border-white/[0.08] bg-slate-950/40">
          <div className="flex items-center gap-3">
            <div className="relative group">
              <div className="w-10 h-10 bg-gradient-to-br from-cyan-500/20 via-blue-600/20 to-purple-600/20 border border-cyan-500/40 rounded-xl flex items-center justify-center shadow-lg shadow-cyan-500/10 transition-all duration-300 group-hover:scale-105 group-hover:border-cyan-400">
                <Cpu className="text-cyan-400 w-5 h-5 animate-pulse-slow" />
              </div>
              <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-cyan-400 rounded-full ring-2 ring-[#07090e] animate-ping" />
              <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-cyan-400 rounded-full ring-2 ring-[#07090e]" />
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="text-base font-black tracking-tight text-white">ADPilot Pro</span>
                <span className="px-1.5 py-0.2 rounded text-[9px] font-mono font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
                  v3.0
                </span>
              </div>
              <span className="text-[10px] text-slate-400 font-mono uppercase tracking-wider font-semibold block mt-0.5">
                Autonomous Marketing OS
              </span>
            </div>
          </div>
        </div>

        {/* 5-Tier Operating System Navigation */}
        <nav className="flex-1 px-3 py-4 space-y-4 overflow-y-auto">
          {/* SECTION 1: OVERVIEW */}
          <div>
            <div className="px-3 text-[10px] font-mono font-bold uppercase tracking-wider text-slate-500 mb-1.5 flex items-center justify-between">
              <span>Overview</span>
              <span className="text-[9px] text-slate-600 font-normal">Core</span>
            </div>
            <div className="space-y-1">
              <button
                onClick={() => { setActiveOSSection('dashboard'); navigate('/dashboard'); }}
                className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-semibold transition-all duration-200 active:scale-[0.98] ${
                  activeOSSection === 'dashboard'
                    ? 'bg-gradient-to-r from-blue-600/25 via-blue-500/15 to-transparent text-cyan-300 border-l-2 border-l-cyan-400 border-y border-r border-white/[0.08] shadow-sm'
                    : 'text-slate-400 hover:bg-slate-900/50 hover:text-slate-200 border border-transparent hover:border-white/[0.05]'
                }`}
              >
                <LayoutDashboard className={`w-4 h-4 ${activeOSSection === 'dashboard' ? 'text-cyan-400' : 'text-blue-400'}`} />
                <span>Executive Dashboard</span>
              </button>
              <button
                onClick={() => { setActiveOSSection('brief'); navigate('/campaigns'); }}
                className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-semibold transition-all duration-200 active:scale-[0.98] ${
                  activeOSSection === 'brief'
                    ? 'bg-gradient-to-r from-cyan-600/25 via-cyan-500/15 to-transparent text-cyan-300 border-l-2 border-l-cyan-400 border-y border-r border-white/[0.08] shadow-sm'
                    : 'text-slate-400 hover:bg-slate-900/50 hover:text-slate-200 border border-transparent hover:border-white/[0.05]'
                }`}
              >
                <FileText className={`w-4 h-4 ${activeOSSection === 'brief' ? 'text-cyan-300' : 'text-cyan-400'}`} />
                <span>Campaign Ingestion Brief</span>
              </button>
              <button
                onClick={() => { setActiveOSSection('simulation'); navigate('/simulation'); }}
                className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-semibold transition-all duration-200 active:scale-[0.98] ${
                  activeOSSection === 'simulation'
                    ? 'bg-gradient-to-r from-emerald-600/25 via-emerald-500/15 to-transparent text-emerald-300 border-l-2 border-l-emerald-400 border-y border-r border-white/[0.08] shadow-sm'
                    : 'text-slate-400 hover:bg-slate-900/50 hover:text-slate-200 border border-transparent hover:border-white/[0.05]'
                }`}
              >
                <Activity className={`w-4 h-4 ${activeOSSection === 'simulation' ? 'text-emerald-300' : 'text-emerald-400'}`} />
                <span>End-to-End Simulation</span>
              </button>
            </div>
          </div>

          {/* SECTION 2: AI WORKSPACE & DAG */}
          <div>
            <div className="px-3 text-[10px] font-mono font-bold uppercase tracking-wider text-slate-500 mb-1.5 flex items-center justify-between">
              <span>AI Workspace & DAG</span>
              <span className="text-[9px] text-slate-600 font-normal">Fleet</span>
            </div>
            <div className="space-y-1">
              <button
                onClick={() => { setActiveOSSection('pipeline'); navigate('/campaigns'); }}
                className={`w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs font-semibold transition-all duration-200 active:scale-[0.98] ${
                  activeOSSection === 'pipeline'
                    ? 'bg-gradient-to-r from-cyan-600/25 via-cyan-500/15 to-transparent text-cyan-300 border-l-2 border-l-cyan-400 border-y border-r border-white/[0.08] shadow-sm'
                    : 'text-slate-400 hover:bg-slate-900/50 hover:text-slate-200 border border-transparent hover:border-white/[0.05]'
                }`}
              >
                <div className="flex items-center gap-2.5">
                  <Layers className={`w-4 h-4 ${activeOSSection === 'pipeline' ? 'text-cyan-300' : 'text-cyan-400'}`} />
                  <span>Interactive Pipeline DAG</span>
                </div>
                <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
              </button>

              <button
                onClick={() => { setActiveOSSection('agents'); navigate('/campaigns'); }}
                className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-semibold transition-all duration-200 active:scale-[0.98] ${
                  activeOSSection === 'agents'
                    ? 'bg-gradient-to-r from-purple-600/25 via-purple-500/15 to-transparent text-purple-300 border-l-2 border-l-purple-400 border-y border-r border-white/[0.08] shadow-sm'
                    : 'text-slate-400 hover:bg-slate-900/50 hover:text-slate-200 border border-transparent hover:border-white/[0.05]'
                }`}
              >
                <Compass className={`w-4 h-4 ${activeOSSection === 'agents' ? 'text-purple-300' : 'text-purple-400'}`} />
                <span>AI Agent Observatory</span>
              </button>

              <button
                onClick={() => { setActiveOSSection('creative'); navigate('/campaigns'); }}
                className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-semibold transition-all duration-200 active:scale-[0.98] ${
                  activeOSSection === 'creative'
                    ? 'bg-gradient-to-r from-pink-600/25 via-pink-500/15 to-transparent text-pink-300 border-l-2 border-l-pink-400 border-y border-r border-white/[0.08] shadow-sm'
                    : 'text-slate-400 hover:bg-slate-900/50 hover:text-slate-200 border border-transparent hover:border-white/[0.05]'
                }`}
              >
                <Palette className={`w-4 h-4 ${activeOSSection === 'creative' ? 'text-pink-300' : 'text-pink-400'}`} />
                <span>Nano Banana Studio</span>
              </button>

              <button
                onClick={() => { setActiveOSSection('optimizer'); navigate('/campaigns'); }}
                className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-semibold transition-all duration-200 active:scale-[0.98] ${
                  activeOSSection === 'optimizer'
                    ? 'bg-gradient-to-r from-amber-600/25 via-amber-500/15 to-transparent text-amber-300 border-l-2 border-l-amber-400 border-y border-r border-white/[0.08] shadow-sm'
                    : 'text-slate-400 hover:bg-slate-900/50 hover:text-slate-200 border border-transparent hover:border-white/[0.05]'
                }`}
              >
                <Zap className={`w-4 h-4 ${activeOSSection === 'optimizer' ? 'text-amber-300' : 'text-amber-400'}`} />
                <span>RL Policy Optimizer (PPO)</span>
              </button>
            </div>
          </div>

          {/* SECTION 3: KNOWLEDGE & GOVERNANCE */}
          <div>
            <div className="px-3 text-[10px] font-mono font-bold uppercase tracking-wider text-slate-500 mb-1.5 flex items-center justify-between">
              <span>Memory & Governance</span>
              <span className="text-[9px] text-slate-600 font-normal">Control</span>
            </div>
            <div className="space-y-1">
              <button
                onClick={() => { setActiveOSSection('knowledge'); navigate('/campaigns'); }}
                className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-semibold transition-all duration-200 active:scale-[0.98] ${
                  activeOSSection === 'knowledge'
                    ? 'bg-gradient-to-r from-indigo-600/25 via-indigo-500/15 to-transparent text-indigo-300 border-l-2 border-l-indigo-400 border-y border-r border-white/[0.08] shadow-sm'
                    : 'text-slate-400 hover:bg-slate-900/50 hover:text-slate-200 border border-transparent hover:border-white/[0.05]'
                }`}
              >
                <BookOpen className={`w-4 h-4 ${activeOSSection === 'knowledge' ? 'text-indigo-300' : 'text-indigo-400'}`} />
                <span>RAG & Vector Memory</span>
              </button>

              <button
                onClick={() => { setActiveOSSection('hitl'); navigate('/campaigns'); }}
                className={`w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs font-semibold transition-all duration-200 active:scale-[0.98] ${
                  activeOSSection === 'hitl'
                    ? 'bg-gradient-to-r from-rose-600/25 via-rose-500/15 to-transparent text-rose-300 border-l-2 border-l-rose-400 border-y border-r border-white/[0.08] shadow-sm'
                    : 'text-slate-400 hover:bg-slate-900/50 hover:text-slate-200 border border-transparent hover:border-white/[0.05]'
                }`}
              >
                <div className="flex items-center gap-2.5">
                  <ShieldCheck className={`w-4 h-4 ${activeOSSection === 'hitl' ? 'text-rose-300' : 'text-rose-400'}`} />
                  <span>Human Review Gate</span>
                </div>
                <span className="px-1.5 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">
                  2 Pending
                </span>
              </button>

              <button
                onClick={() => { setActiveOSSection('timeline'); navigate('/campaigns'); }}
                className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-semibold transition-all duration-200 active:scale-[0.98] ${
                  activeOSSection === 'timeline'
                    ? 'bg-gradient-to-r from-emerald-600/25 via-emerald-500/15 to-transparent text-emerald-300 border-l-2 border-l-emerald-400 border-y border-r border-white/[0.08] shadow-sm'
                    : 'text-slate-400 hover:bg-slate-900/50 hover:text-slate-200 border border-transparent hover:border-white/[0.05]'
                }`}
              >
                <Clock className={`w-4 h-4 ${activeOSSection === 'timeline' ? 'text-emerald-300' : 'text-emerald-400'}`} />
                <span>Event Timeline Audit</span>
              </button>
            </div>
          </div>

          {/* SECTION 4: SYSTEM & SHOWCASE */}
          <div>
            <div className="px-3 text-[10px] font-mono font-bold uppercase tracking-wider text-slate-500 mb-1.5 flex items-center justify-between">
              <span>System & Showcase</span>
              <span className="text-[9px] text-slate-600 font-normal">Platform</span>
            </div>
            <div className="space-y-1">
              <button
                onClick={() => { setActiveOSSection('showcase'); navigate('/showcase'); }}
                className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-semibold transition-all duration-200 active:scale-[0.98] ${
                  activeOSSection === 'showcase'
                    ? 'bg-gradient-to-r from-purple-600/25 via-purple-500/15 to-transparent text-purple-300 border-l-2 border-l-purple-400 border-y border-r border-white/[0.08] shadow-sm'
                    : 'text-slate-400 hover:bg-slate-900/50 hover:text-slate-200 border border-transparent hover:border-white/[0.05]'
                }`}
              >
                <Sparkles className={`w-4 h-4 ${activeOSSection === 'showcase' ? 'text-purple-300' : 'text-purple-400'}`} />
                <span>Showcase Portal V3</span>
              </button>

              <button
                onClick={() => { setActiveOSSection('techstack'); navigate('/technology-stack'); }}
                className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-semibold transition-all duration-200 active:scale-[0.98] ${
                  activeOSSection === 'techstack'
                    ? 'bg-gradient-to-r from-cyan-600/25 via-cyan-500/15 to-transparent text-cyan-300 border-l-2 border-l-cyan-400 border-y border-r border-white/[0.08] shadow-sm'
                    : 'text-slate-400 hover:bg-slate-900/50 hover:text-slate-200 border border-transparent hover:border-white/[0.05]'
                }`}
              >
                <Cpu className={`w-4 h-4 ${activeOSSection === 'techstack' ? 'text-cyan-300' : 'text-cyan-400'}`} />
                <span>Technology Stack & Arch</span>
              </button>

              <button
                onClick={() => { setActiveOSSection('models'); navigate('/campaigns'); }}
                className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-semibold transition-all duration-200 active:scale-[0.98] ${
                  activeOSSection === 'models'
                    ? 'bg-gradient-to-r from-blue-600/25 via-blue-500/15 to-transparent text-blue-300 border-l-2 border-l-blue-400 border-y border-r border-white/[0.08] shadow-sm'
                    : 'text-slate-400 hover:bg-slate-900/50 hover:text-slate-200 border border-transparent hover:border-white/[0.05]'
                }`}
              >
                <Box className={`w-4 h-4 ${activeOSSection === 'models' ? 'text-blue-300' : 'text-blue-400'}`} />
                <span>Neural Model Registry</span>
              </button>

              <button
                onClick={() => { setActiveOSSection('health'); navigate('/campaigns'); }}
                className={`w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs font-semibold transition-all duration-200 active:scale-[0.98] ${
                  activeOSSection === 'health'
                    ? 'bg-gradient-to-r from-emerald-600/25 via-emerald-500/15 to-transparent text-emerald-300 border-l-2 border-l-emerald-400 border-y border-r border-white/[0.08] shadow-sm'
                    : 'text-slate-400 hover:bg-slate-900/50 hover:text-slate-200 border border-transparent hover:border-white/[0.05]'
                }`}
              >
                <div className="flex items-center gap-2.5">
                  <Activity className={`w-4 h-4 ${activeOSSection === 'health' ? 'text-emerald-300' : 'text-emerald-400'}`} />
                  <span>Platform Diagnostics</span>
                </div>
                <span className="w-2 h-2 rounded-full bg-emerald-400 shadow-sm shadow-emerald-400" />
              </button>

              <button
                onClick={() => { setActiveOSSection('settings'); navigate('/campaigns'); }}
                className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-semibold transition-all duration-200 active:scale-[0.98] ${
                  activeOSSection === 'settings'
                    ? 'bg-slate-800 text-slate-200 border-l-2 border-l-slate-400 border-y border-r border-white/[0.08]'
                    : 'text-slate-400 hover:bg-slate-900/50 hover:text-slate-200 border border-transparent hover:border-white/[0.05]'
                }`}
              >
                <SettingsIcon className="w-4 h-4 text-slate-400" />
                <span>System Settings</span>
              </button>
            </div>
          </div>
        </nav>

        {/* Sidebar Footer */}
        <div className="p-3.5 border-t border-white/[0.08] bg-slate-950/60 space-y-2.5">
          <button
            onClick={handleNewCampaign}
            className="w-full flex items-center justify-center gap-2 py-2 px-3 rounded-xl text-xs font-bold bg-gradient-to-r from-cyan-500 via-blue-600 to-indigo-600 hover:from-cyan-400 hover:via-blue-500 hover:to-indigo-500 text-white shadow-lg shadow-cyan-500/20 transition-all duration-200 active:scale-[0.98]"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>New Campaign</span>
          </button>
          
          <div className="flex items-center justify-between px-1 text-[11px] font-mono text-slate-400">
            <span className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              <span>18 Agents Ready</span>
            </span>
            <span className="text-slate-500 font-semibold">99.9% Up</span>
          </div>
        </div>
      </aside>

      {/* ── Main Application Content Canvas ── */}
      <main className="flex-1 flex flex-col overflow-hidden relative z-10">
        {/* Top App Bar with Dynamic Breadcrumb */}
        <header className="h-16 bg-[#07090e]/80 border-b border-white/[0.08] px-6 flex items-center justify-between z-20 shrink-0 backdrop-blur-3xl shadow-sm">
          {/* Breadcrumb & Section Title */}
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <div className="p-1.5 rounded-lg bg-cyan-500/10 border border-cyan-500/20 text-cyan-400">
                <CurrentIcon className="w-4 h-4" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h1 className="text-sm font-bold text-slate-100 tracking-tight">
                    {currentMeta.title}
                  </h1>
                  <span className="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-white/[0.06] text-cyan-300 border border-white/[0.08]">
                    {currentMeta.tag}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Center Search & Demo Launcher */}
          <div className="hidden md:flex items-center gap-3">
            <button
              onClick={() => setIsCommandPaletteOpen(true)}
              className="flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-slate-950/80 border border-white/[0.08] hover:border-cyan-500/40 text-slate-400 hover:text-slate-200 text-xs font-medium transition-all shadow-inner"
            >
              <Search className="w-3.5 h-3.5 text-slate-500" />
              <span>Search workspace, agents, models...</span>
              <kbd className="px-1.5 py-0.5 rounded bg-slate-900 text-[10px] font-mono text-slate-400 border border-slate-800 ml-2">
                Ctrl K
              </kbd>
            </button>

            <button
              onClick={() => setIsDemoModalOpen(true)}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-gradient-to-r from-cyan-500/15 via-blue-500/15 to-purple-500/15 text-cyan-300 border border-cyan-500/30 text-xs font-semibold hover:border-cyan-400 transition-all active:scale-95"
            >
              <Sparkles className="w-3.5 h-3.5 fill-cyan-400 text-cyan-400" />
              <span>1-Click Demo</span>
            </button>
          </div>

          {/* Top Right Status, Feeds, Profile */}
          <div className="flex items-center gap-3">
            <button
              onClick={() => setIsActivityFeedOpen(!isActivityFeedOpen)}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-950/80 border border-white/[0.08] hover:border-cyan-500/40 text-xs font-mono text-cyan-400 transition-all relative"
            >
              <Activity className="w-3.5 h-3.5 animate-pulse" />
              <span className="hidden sm:inline">AI Activity</span>
              <span className="w-2 h-2 rounded-full bg-cyan-400" />
            </button>

            <button
              onClick={toggleTheme}
              title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} mode`}
              className="p-2 rounded-xl bg-slate-950/80 border border-white/[0.08] text-slate-400 hover:text-slate-200 hover:border-white/[0.15] transition-all"
            >
              <Sparkles className="w-4 h-4 text-amber-400" />
            </button>

            <div className="h-5 w-[1px] bg-white/[0.08]" />

            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-cyan-500 via-blue-600 to-indigo-600 flex items-center justify-center text-white text-xs font-extrabold shadow-md shadow-cyan-500/20">
                AD
              </div>
              <div className="hidden xl:block text-left">
                <div className="text-xs font-bold text-slate-200 leading-tight">Admin Director</div>
                <div className="text-[9px] text-cyan-400 font-mono uppercase font-semibold">Autonomous Ops</div>
              </div>
            </div>
          </div>
        </header>

        {/* Ã¢â€â‚¬Ã¢â€â‚¬ Main Scrollable Body Ã¢â€â‚¬Ã¢â€â‚¬ */}
        <div className="flex-1 overflow-y-auto p-6 bg-transparent">
          <div className="max-w-7xl mx-auto space-y-6">
            {/* Top Campaign Control Bar (Hidden on Showcase & TechStack standalone views) */}
            {activeOSSection !== 'showcase' && activeOSSection !== 'techstack' && (
              <CampaignControlBar
                campaign={campaignBrief}
                progress={status?.progress || (results ? 100 : 0)}
                status={status?.status || (results ? 'completed' : 'idle')}
                activeAgentsCount={MASTER_AGENTS.length}
                totalAgentsCount={MASTER_AGENTS.length}
                confidenceScore={94}
                onOpenHITL={() => setActiveOSSection('hitl')}
                onOpenDemo={() => setIsDemoModalOpen(true)}
                onExportReport={handleDownloadAssets}
              />
            )}

            {/* Dynamic View Switcher */}
            {activeOSSection === 'brief' && (
              <div className="space-y-6">
                {currentTaskId && (loading || status?.status === 'in_progress') ? (
                  <div className="bg-slate-950/40 border border-slate-800/60 rounded-2xl p-6 backdrop-blur-3xl shadow-2xl">
                    <LiveOrchestration status={status} isLoading={loading} error={error} />
                  </div>
                ) : results ? (
                  <div className="space-y-6">
                    <div className="flex items-center justify-between bg-emerald-500/10 border border-emerald-500/30 rounded-2xl p-4">
                      <div className="flex items-center gap-3">
                        <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                        <div>
                          <h4 className="text-sm font-bold text-emerald-300">Campaign Package Successfully Generated</h4>
                          <p className="text-xs text-slate-400">All 18 stages executed with 100% contract compliance.</p>
                        </div>
                      </div>
                      <button
                        onClick={handleNewCampaign}
                        className="px-3 py-1.5 rounded-xl text-xs font-semibold bg-slate-800 text-slate-200 hover:bg-slate-700 transition-colors"
                      >
                        Create Another Campaign
                      </button>
                    </div>
                    <ResultDisplay
                      content={results}
                      onDownload={handleDownloadAssets}
                      isDownloading={isDownloading}
                    />
                  </div>
                ) : (
                  <div className="grid grid-cols-1 xl:grid-cols-12 gap-6 items-start">
                    <div className="xl:col-span-5 bg-slate-950/40 border border-slate-800/60 rounded-2xl p-6 backdrop-blur-3xl shadow-2xl">
                      <CampaignBriefForm onSubmit={handleBriefSubmit} isLoading={loading} />
                    </div>
                    <div className="xl:col-span-7">
                      <InteractivePipelineDAG
                        agents={MASTER_AGENTS}
                        activeAgentId={selectedAgentForDrawer?.id}
                        onSelectAgent={(ag) => setSelectedAgentForDrawer(ag)}
                        onInspectIO={(ag) => setSelectedAgentForIO(ag)}
                        isRunning={loading}
                      />
                    </div>
                  </div>
                )}
              </div>
            )}

            {activeOSSection === 'pipeline' && (
              <div className="space-y-6">
                {currentTaskId && (loading || status?.status === 'in_progress') && (
                  <div className="bg-slate-950/40 border border-slate-800/60 rounded-2xl p-6 backdrop-blur-3xl shadow-2xl">
                    <LiveOrchestration status={status} isLoading={loading} error={error} />
                  </div>
                )}

                <InteractivePipelineDAG
                  agents={MASTER_AGENTS}
                  activeAgentId={selectedAgentForDrawer?.id}
                  onSelectAgent={(ag) => setSelectedAgentForDrawer(ag)}
                  onInspectIO={(ag) => setSelectedAgentForIO(ag)}
                  isRunning={loading}
                />

                {results && (
                  <div className="pt-4">
                    <ResultDisplay
                      content={results}
                      onDownload={handleDownloadAssets}
                      isDownloading={isDownloading}
                    />
                  </div>
                )}
              </div>
            )}

            {activeOSSection === 'agents' && (
              <AgentObservatory
                agents={MASTER_AGENTS}
                onSelectAgent={(ag) => setSelectedAgentForDrawer(ag)}
                onInspectIO={(ag) => setSelectedAgentForIO(ag)}
              />
            )}

            {activeOSSection === 'optimizer' && (
              <OptimizerDashboard />
            )}

            {activeOSSection === 'hitl' && (
              <HITLApprovalCenter />
            )}

            {activeOSSection === 'showcase' && (
              <ShowcaseLandingView />
            )}

            {activeOSSection === 'techstack' && (
              <TechnologyStackView />
            )}

            {activeOSSection === 'models' && (
              <ModelRegistryView />
            )}

            {activeOSSection === 'creative' && (
              <CreativeStudioView />
            )}

            {activeOSSection === 'timeline' && (
              <CampaignTimelineView />
            )}

            {activeOSSection === 'knowledge' && (
              <KnowledgeBaseView />
            )}

            {activeOSSection === 'health' && (
              <SystemHealthView />
            )}

            {activeOSSection === 'dashboard' && (
              <DashboardView />
            )}

            {activeOSSection === 'settings' && (
              <div className="max-w-2xl mx-auto">
                <SettingsView theme={theme} toggleTheme={toggleTheme} />
              </div>
            )}

            {activeOSSection === 'simulation' && (
              <CampaignSimulationView />
            )}
          </div>
        </div>

        {/* Ã¢â€â‚¬Ã¢â€â‚¬ Slide-Over Drawers & Modals Ã¢â€â‚¬Ã¢â€â‚¬ */}
        <AgentDetailDrawer
          agent={selectedAgentForDrawer}
          isOpen={selectedAgentForDrawer !== null}
          onClose={() => setSelectedAgentForDrawer(null)}
          onInspectIO={(ag) => {
            setSelectedAgentForDrawer(null);
            setSelectedAgentForIO(ag);
          }}
        />

        <IOInspectorModal
          agent={selectedAgentForIO}
          isOpen={selectedAgentForIO !== null}
          onClose={() => setSelectedAgentForIO(null)}
        />

        <LiveActivityFeed
          isOpen={isActivityFeedOpen}
          onClose={() => setIsActivityFeedOpen(false)}
          events={activityEvents}
        />

        <CommandPalette
          isOpen={isCommandPaletteOpen}
          onClose={() => setIsCommandPaletteOpen(false)}
          onNavigate={(sec) => setActiveOSSection(sec)}
          onStartDemo={() => setIsDemoModalOpen(true)}
        />

        <InteractiveDemoModal
          isOpen={isDemoModalOpen}
          onClose={() => setIsDemoModalOpen(false)}
          agents={MASTER_AGENTS}
        />
      </main>
    </div>
  )
}

export default App



