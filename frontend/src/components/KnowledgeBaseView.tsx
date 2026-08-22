import React, { useState } from 'react';
import { 
  BookOpen, 
  Search, 
  Database, 
  Layers, 
  Cpu, 
  Sparkles, 
  CheckCircle2, 
  Plus, 
  FileText, 
  Brain, 
  HardDrive, 
  ArrowRight,
  RefreshCw,
  FolderOpen
} from 'lucide-react';

export const KnowledgeBaseView: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [activeMemoryTab, setActiveMemoryTab] = useState<'rag' | 'memory'>('rag');

  const ragDocuments = [
    {
      id: 'doc-01',
      title: 'B2B SaaS Growth Marketing Playbook 2026',
      chunks: 48,
      vectorDim: 384,
      model: 'BAAI/bge-small-en-v1.5',
      category: 'Strategic Playbook',
      similarityScore: 0.94,
      lastIndexed: '2 hours ago'
    },
    {
      id: 'doc-02',
      title: 'Enterprise High-Converting Ad Copy Guidelines',
      chunks: 32,
      vectorDim: 384,
      model: 'BAAI/bge-small-en-v1.5',
      category: 'Copywriting Framework',
      similarityScore: 0.91,
      lastIndexed: '1 day ago'
    },
    {
      id: 'doc-03',
      title: 'Competitor Intelligence Benchmark (MarTech Rivals)',
      chunks: 24,
      vectorDim: 384,
      model: 'BAAI/bge-small-en-v1.5',
      category: 'Market Research',
      similarityScore: 0.88,
      lastIndexed: '3 days ago'
    },
    {
      id: 'doc-04',
      title: 'Brand Voice Identity & Tone Safeguards',
      chunks: 16,
      vectorDim: 384,
      model: 'BAAI/bge-small-en-v1.5',
      category: 'Brand Guidelines',
      similarityScore: 0.96,
      lastIndexed: '5 days ago'
    }
  ];

  const memoryTiers = [
    {
      name: 'Tier 1: Campaign Working Memory',
      scope: 'Active Session',
      storage: 'Fast InMemory Cache',
      items: '18 Stage Context Variables',
      desc: 'Stores transient brief parameters, agent scratchpads, and immediate intermediate contracts.',
      status: 'Active (0.2ms latency)'
    },
    {
      name: 'Tier 2: Brand Identity Memory',
      scope: 'Persistent Across Campaigns',
      storage: 'SQLite Structured Store',
      items: 'Typography, Color Palettes, Negative Tone Rules',
      desc: 'Ensures long-term stylistic consistency and prevents off-brand ad generation.',
      status: 'Synced (1.1ms latency)'
    },
    {
      name: 'Tier 3: Customer & Persona Memory',
      scope: 'Global ICP Intelligence',
      storage: 'Qdrant Vector Store',
      items: '12 Audience Segment Archetypes',
      desc: 'Contains historical psychological triggers, pain points, and conversion objections.',
      status: 'Indexed (4.2ms latency)'
    },
    {
      name: 'Tier 4: Execution Feedback Memory',
      scope: 'Reinforcement Learning',
      storage: 'PPO Trajectory Buffer',
      items: '1,482 Historical Action-Reward Pairs',
      desc: 'Powers continuous policy updates based on live CTR, ROAS, and CAC performance signals.',
      status: 'Optimizing (15.8ms latency)'
    }
  ];

  const filteredDocs = ragDocuments.filter(d => 
    d.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    d.category.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="w-full space-y-6">
      {/* Header Banner */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 relative overflow-hidden backdrop-blur-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2.5">
              <span className="p-2 rounded-xl bg-purple-500/10 text-purple-400 border border-purple-500/20">
                <Brain className="w-5 h-5" />
              </span>
              <h2 className="text-xl font-bold text-slate-100">Global Knowledge Base, RAG & Multi-Tier Memory</h2>
            </div>
            <p className="text-xs text-slate-400 mt-1 max-w-2xl">
              Enterprise semantic vector retrieval (FastEmbed BGE + Qdrant) and multi-tiered agent memory ensuring zero hallucination and strict brand adherence.
            </p>
          </div>

          {/* Tab Switcher */}
          <div className="flex items-center gap-2 bg-slate-950/80 border border-slate-800 rounded-xl p-1.5 shrink-0">
            <button
              onClick={() => setActiveMemoryTab('rag')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold font-mono transition-all ${
                activeMemoryTab === 'rag'
                  ? 'bg-purple-500/20 text-purple-300 border border-purple-500/40 shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Vector Documents (RAG)
            </button>
            <button
              onClick={() => setActiveMemoryTab('memory')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold font-mono transition-all ${
                activeMemoryTab === 'memory'
                  ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Multi-Tier Memory Engine
            </button>
          </div>
        </div>
      </div>

      {/* TAB 1: RAG Documents */}
      {activeMemoryTab === 'rag' && (
        <div className="space-y-4">
          {/* Search Bar & Stats */}
          <div className="flex flex-col sm:flex-row items-center justify-between gap-3 bg-slate-900/80 border border-slate-800 rounded-2xl p-4">
            <div className="relative w-full sm:w-80">
              <Search className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
              <input
                type="text"
                placeholder="Search vector knowledge store..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-9 pr-3.5 py-2 text-xs text-slate-100 placeholder:text-slate-500 focus:outline-none focus:border-purple-500"
              />
            </div>

            <div className="flex items-center gap-4 text-xs font-mono text-slate-400">
              <span>Indexed Vectors: <strong className="text-cyan-400">120 Chunks</strong></span>
              <span>Embedding Metric: <strong className="text-purple-400">Cosine (384-d)</strong></span>
            </div>
          </div>

          {/* Document Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {filteredDocs.map(doc => (
              <div key={doc.id} className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 backdrop-blur-xl flex flex-col justify-between hover:border-slate-700 transition-colors">
                <div>
                  <div className="flex items-center justify-between gap-2 mb-2">
                    <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-purple-500/10 text-purple-300 border border-purple-500/20">
                      {doc.category}
                    </span>
                    <span className="text-[10px] font-mono text-emerald-400 font-bold flex items-center gap-1">
                      <CheckCircle2 className="w-3 h-3" /> HitRate: {Math.round(doc.similarityScore * 100)}%
                    </span>
                  </div>

                  <h3 className="text-sm font-bold text-slate-100 mt-1">{doc.title}</h3>
                  
                  <div className="space-y-1.5 text-xs font-mono mt-3 text-slate-400">
                    <div className="flex justify-between py-1 border-b border-slate-800/60">
                      <span>Vector Dimension:</span>
                      <span className="text-slate-200">{doc.vectorDim}-d Dense</span>
                    </div>
                    <div className="flex justify-between py-1 border-b border-slate-800/60">
                      <span>Embedding Model:</span>
                      <span className="text-cyan-300">{doc.model}</span>
                    </div>
                    <div className="flex justify-between py-1">
                      <span>Indexed Chunks:</span>
                      <span className="text-purple-300 font-bold">{doc.chunks} Embeddings</span>
                    </div>
                  </div>
                </div>

                <div className="pt-3 mt-3 border-t border-slate-800 flex items-center justify-between text-[11px] font-mono text-slate-500">
                  <span>Last synced: {doc.lastIndexed}</span>
                  <span className="text-purple-400 font-semibold cursor-pointer hover:underline">Explore Embeddings →</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 2: Multi-Tier Memory Engine */}
      {activeMemoryTab === 'memory' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {memoryTiers.map((tier, idx) => (
            <div key={idx} className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 backdrop-blur-xl flex flex-col justify-between hover:border-slate-700 transition-colors">
              <div>
                <div className="flex items-center justify-between gap-2 mb-2">
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-cyan-500/10 text-cyan-300 border border-cyan-500/20">
                    {tier.scope}
                  </span>
                  <span className="text-[10px] font-mono text-emerald-400 font-bold">
                    {tier.status}
                  </span>
                </div>

                <h3 className="text-sm font-bold text-slate-100 mt-1">{tier.name}</h3>
                <p className="text-xs text-slate-400 mt-2 font-sans leading-relaxed">{tier.desc}</p>

                <div className="mt-4 p-3 rounded-xl bg-slate-950 border border-slate-800/80 space-y-1.5 text-xs font-mono">
                  <div className="flex justify-between">
                    <span className="text-slate-500">Storage Backend:</span>
                    <span className="text-purple-300 font-semibold">{tier.storage}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">Managed Artifacts:</span>
                    <span className="text-slate-300 truncate max-w-[200px]">{tier.items}</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
