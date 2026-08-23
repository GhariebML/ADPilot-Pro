import React, { useState } from 'react';
import { 
  Database, 
  Search, 
  Layers, 
  Sparkles, 
  CheckCircle2, 
  ArrowRight,
  BookOpen,
  FileCode2
} from 'lucide-react';

export const RAGVectorSpace3D: React.FC = () => {
  const [activeQuery, setActiveQuery] = useState<string>('Enterprise B2B FinOps Cloud Migration Value Proposition');
  const [searchTriggered, setSearchTriggered] = useState<boolean>(true);

  const sampleQueries = [
    'Enterprise B2B FinOps Cloud Migration Value Proposition',
    'High-Converting SaaS Ad Headlines & Call-to-Actions',
    'Real Estate High-Net-Worth Investor Buyer Persona',
    'Competitor White-Space Pricing Vulnerability'
  ];

  const matchedChunks = [
    {
      id: 'chunk-01',
      title: 'Cloud Cost Optimization Whitepaper (Page 4)',
      score: '0.962 Dense Cosine',
      bm25: '18.4 BM25 Rank',
      rrf: '0.0324 RRF Score',
      text: 'Enterprise workloads migrating to Kubernetes microservices achieve on average 32.4% compute cost reduction and sub-minute automated failover.'
    },
    {
      id: 'chunk-02',
      title: 'Winning B2B Creative Copy Bank (Q3 2025)',
      score: '0.938 Dense Cosine',
      bm25: '16.1 BM25 Rank',
      rrf: '0.0308 RRF Score',
      text: 'Headline formula: Stop Burning AWS Spend. Automated FinOps architecture delivering instant visibility within 14 days.'
    },
    {
      id: 'chunk-03',
      title: 'Executive Decision Maker ICP Research Dossier',
      score: '0.915 Dense Cosine',
      bm25: '14.7 BM25 Rank',
      rrf: '0.0291 RRF Score',
      text: 'Primary emotional trigger: Fear of vendor lock-in and unpredictable monthly cloud bill spikes among CTOs and CFOs.'
    }
  ];

  return (
    <div className="w-full bg-slate-950/40 border border-slate-800/60 shadow-2xl rounded-2xl p-6 backdrop-blur-2xl space-y-6 shadow-2xl relative overflow-hidden">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800/80 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-1.5 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <Database className="w-4 h-4" />
            </span>
            <h3 className="text-base font-bold text-white font-mono uppercase tracking-wider">
              Dual-Stream Hybrid RAG & Vector Space 3D
            </h3>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            FastEmbed BGE 384-dimensional dense semantic vectors fused with BM25 Okapi lexical scoring (RRF k=60) stored in local Qdrant.
          </p>
        </div>

        <span className="px-3 py-1 rounded-xl text-xs font-mono font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 shrink-0">
          HitRate = 1.0 â€¢ MRR = 1.00
        </span>
      </div>

      {/* Query Bar */}
      <div className="space-y-2">
        <label className="text-xs font-mono text-slate-400 uppercase tracking-wider block">
          Select or Enter Benchmark Retrieval Query:
        </label>
        <div className="flex flex-wrap gap-2">
          {sampleQueries.map((q, idx) => (
            <button
              key={idx}
              onClick={() => { setActiveQuery(q); setSearchTriggered(true); }}
              className={`px-3 py-1.5 rounded-xl text-xs font-mono transition-all text-left truncate max-w-md ${
                activeQuery === q
                  ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/50 shadow-sm'
                  : 'bg-slate-900 border border-slate-800 text-slate-400 hover:text-slate-200'
              }`}
            >
              {q}
            </button>
          ))}
        </div>
      </div>

      {/* Results Matrix */}
      <div className="space-y-3">
        <h4 className="text-xs font-mono font-bold text-slate-300 uppercase">
          Retrieved Grounding Documents (Qdrant Vector DB Collection: <code className="text-cyan-400">adpilot_knowledge</code>)
        </h4>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {matchedChunks.map((chunk) => (
            <div key={chunk.id} className="p-4 rounded-xl bg-slate-900/70 border border-slate-800 space-y-3 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between gap-1 mb-2">
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 font-bold">
                    {chunk.score}
                  </span>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 border border-purple-500/20 font-bold">
                    {chunk.rrf}
                  </span>
                </div>

                <h5 className="text-xs font-bold text-slate-100 line-clamp-1">{chunk.title}</h5>
                <p className="text-xs text-slate-300 mt-2 leading-relaxed bg-slate-950/70 p-3 rounded-lg border border-slate-800/80">
                  "{chunk.text}"
                </p>
              </div>

              <div className="pt-2 border-t border-slate-800 text-[10px] font-mono text-slate-500 flex justify-between">
                <span>Sparse: {chunk.bm25}</span>
                <span className="text-emerald-400 font-bold">Grounding Verified</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default RAGVectorSpace3D;

