import React, { useState } from 'react';
import { 
  Box, 
  CheckCircle2, 
  Cpu, 
  Sparkles, 
  Layers, 
  BarChart3, 
  TrendingUp, 
  Zap, 
  FileCode2, 
  Activity,
  Award
} from 'lucide-react';
import type { ModelRegistryItem } from '../types';

export const ModelRegistryView: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'catalog' | 'arena'>('catalog');

  const models: ModelRegistryItem[] = [
    {
      id: 'model-ppo-001',
      name: 'PPO Continuous Policy Network',
      category: 'Reinforcement Learning',
      artifactPath: 'research/models/optimizer/ppo_policy.pt',
      responsibleAgent: 'Optimization Agent',
      framework: 'PyTorch',
      status: 'PRODUCTION_READY',
      inputDim: '12-dim Continuous State',
      outputDim: 'K-dim Action Vector',
      inferenceLatency: '15.8ms',
      accuracyOrReward: '+0.48 Mean Reward'
    },
    {
      id: 'model-ridge-001',
      name: 'Multi-Target Revenue & ROAS Forecaster',
      category: 'Classical ML Regression',
      artifactPath: 'research/models/analytics/revenue_forecaster.pkl',
      responsibleAgent: 'Analytics Agent',
      framework: 'Scikit-Learn',
      status: 'PRODUCTION_READY',
      inputDim: 'Scaled Features (StandardScaler)',
      outputDim: '[ROAS, CAC, CVR]',
      inferenceLatency: '2.1ms',
      accuracyOrReward: 'R² = 0.894'
    },
    {
      id: 'model-content-001',
      name: 'Copy Quality & Brand Voice Classifier',
      category: 'Classical ML Regression',
      artifactPath: 'research/models/content/brand_voice_classifier.pkl',
      responsibleAgent: 'Content Copywriting Agent',
      framework: 'Scikit-Learn',
      status: 'PRODUCTION_READY',
      inputDim: 'TF-IDF + Text Statistics',
      outputDim: 'Quality Score [0-10]',
      inferenceLatency: '3.4ms',
      accuracyOrReward: 'MSE = 0.12'
    },
    {
      id: 'model-clip-001',
      name: 'CLIP-ViT Visual Quality & Margin Regressor',
      category: 'Zero-Shot Vision',
      artifactPath: 'research/models/cv/creative_quality_regressor.pkl',
      responsibleAgent: 'Computer Vision Agent',
      framework: 'CLIP-ViT (ONNX)',
      status: 'PRODUCTION_READY',
      inputDim: '512-dim ViT Embeddings',
      outputDim: 'Aesthetic Score [0-10]',
      inferenceLatency: '4.8ms',
      accuracyOrReward: 'Accuracy = 91.2%'
    },
    {
      id: 'model-bge-001',
      name: 'BGE Semantic Vector Embeddings',
      category: 'Vector Embeddings',
      artifactPath: 'storage/qdrant_rag / BAAI/bge-small-en-v1.5',
      responsibleAgent: 'RAG & Memory Engine',
      framework: 'FastEmbed BGE',
      status: 'ACTIVE_ONLINE',
      inputDim: 'Variable Text Chunks',
      outputDim: '384-dim Dense Vector',
      inferenceLatency: '23.3ms',
      accuracyOrReward: 'MRR = 1.00 • HitRate = 1.0'
    }
  ];

  const benchmarks = [
    { model: 'GPT-4o Router', task: 'Strategic Roadmap Planning', latency: '1,420ms', costPer1k: '$0.0050', quality: '96.2%', status: 'Primary Router' },
    { model: 'Claude 3.5 Sonnet', task: 'Ad Copywriting & Nurture Sequences', latency: '1,980ms', costPer1k: '$0.0030', quality: '97.5%', status: 'Creative Lead' },
    { model: 'PPO Continuous Policy', task: 'Dynamic Budget Reallocation', latency: '15.8ms', costPer1k: '$0.0000', quality: '+0.48 Reward', status: 'Active Policy' },
    { model: 'Ridge Revenue Forecaster', task: 'Multi-Target ROI Prediction', latency: '2.1ms', costPer1k: '$0.0000', quality: 'R² = 0.894', status: 'Predictive Forecaster' },
    { model: 'CLIP-ViT (ONNX)', task: 'Visual Quality & Contrast Check', latency: '4.8ms', costPer1k: '$0.0000', quality: '91.2% Accuracy', status: 'Safety Gate' },
  ];

  return (
    <div className="w-full space-y-6">
      {/* Header Banner */}
      <div className="glass-panel-elevated rounded-2xl p-6 relative overflow-hidden shadow-2xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-3">
              <span className="p-2.5 rounded-xl bg-gradient-to-br from-purple-500/25 to-pink-500/25 text-purple-400 border border-purple-500/40 shadow-[0_0_20px_rgba(168,85,247,0.25)]">
                <Box className="w-6 h-6" />
              </span>
              <div>
                <h2 className="text-xl font-black text-slate-100 flex items-center gap-2">
                  Custom Machine Learning & Neural Model Registry
                  <span className="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-purple-500/15 text-purple-300 border border-purple-500/30">
                    PyTorch / ONNX / Scikit
                  </span>
                </h2>
                <p className="text-xs text-slate-400 mt-0.5 max-w-2xl">
                  Catalog and benchmark arena for custom trained neural weights, statistical forecasters, and vision scoring models powering ADPilot.
                </p>
              </div>
            </div>
          </div>

          {/* Toggle Tabs */}
          <div className="flex items-center gap-2 bg-[#07090e]/90 border border-white/[0.08] rounded-xl p-1.5 shrink-0 shadow-inner">
            <button
              onClick={() => setActiveTab('catalog')}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-bold font-mono transition-all ${
                activeTab === 'catalog'
                  ? 'bg-purple-500/25 text-purple-300 border border-purple-400 shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Model Artifacts ({models.length})
            </button>
            <button
              onClick={() => setActiveTab('arena')}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-bold font-mono transition-all ${
                activeTab === 'arena'
                  ? 'bg-cyan-500/25 text-cyan-300 border border-cyan-400 shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Benchmark Arena
            </button>
          </div>
        </div>
      </div>

      {/* VIEW 1: Model Artifacts Cards */}
      {activeTab === 'catalog' && (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
          {models.map(model => (
            <div key={model.id} className="glass-card-premium p-5 flex flex-col justify-between hover:border-purple-500/40 transition-all shadow-2xl">
              <div>
                <div className="flex items-start justify-between gap-2 mb-3">
                  <div>
                    <span className="px-2.5 py-0.5 rounded text-[10px] font-mono font-bold bg-blue-500/15 text-blue-300 border border-blue-500/30">
                      {model.category}
                    </span>
                    <h3 className="text-sm font-bold text-slate-100 mt-2">{model.name}</h3>
                  </div>
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 shrink-0">
                    {model.status}
                  </span>
                </div>

                {/* Artifact File Path */}
                <div className="p-2.5 rounded-xl bg-[#07090e] border border-white/[0.08] font-mono text-[11px] text-slate-400 mb-4 truncate shadow-inner">
                  <span className="text-slate-500">File: </span>
                  <span className="text-cyan-400 font-medium">{model.artifactPath}</span>
                </div>

                {/* Specs Table */}
                <div className="space-y-2 text-xs font-mono">
                  <div className="flex justify-between py-1 border-b border-white/[0.05]">
                    <span className="text-slate-400">Agent:</span>
                    <span className="text-slate-200 font-semibold">{model.responsibleAgent}</span>
                  </div>
                  <div className="flex justify-between py-1 border-b border-white/[0.05]">
                    <span className="text-slate-400">Framework:</span>
                    <span className="text-purple-300 font-semibold">{model.framework}</span>
                  </div>
                  <div className="flex justify-between py-1 border-b border-white/[0.05]">
                    <span className="text-slate-400">Input Schema:</span>
                    <span className="text-slate-200 truncate max-w-[160px]">{model.inputDim}</span>
                  </div>
                  <div className="flex justify-between py-1 border-b border-white/[0.05]">
                    <span className="text-slate-400">Output Schema:</span>
                    <span className="text-slate-200 truncate max-w-[160px]">{model.outputDim}</span>
                  </div>
                </div>
              </div>

              {/* Performance Footer */}
              <div className="mt-4 pt-3 border-t border-white/[0.08] flex items-center justify-between font-mono">
                <div className="flex items-center gap-1.5 text-xs text-amber-400 font-bold">
                  <Zap className="w-3.5 h-3.5" />
                  <span>{model.inferenceLatency}</span>
                </div>
                <div className="flex items-center gap-1 text-xs text-emerald-400 font-bold">
                  <Award className="w-3.5 h-3.5" />
                  <span>{model.accuracyOrReward}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* VIEW 2: Benchmark Arena Table */}
      {activeTab === 'arena' && (
        <div className="glass-panel-elevated rounded-2xl overflow-hidden shadow-2xl">
          <div className="p-4 border-b border-white/[0.08] flex items-center justify-between">
            <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-cyan-400 flex items-center gap-2">
              <BarChart3 className="w-4 h-4" />
              <span>Multi-Model Latency, Cost & Precision Leaderboard</span>
            </h3>
            <span className="text-xs font-mono text-slate-400">Evaluation Benchmark: MMLU / MT-Bench</span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left font-mono text-xs">
              <thead className="bg-[#07090e] border-b border-white/[0.08] text-slate-400 uppercase text-[10px]">
                <tr>
                  <th className="p-3.5">Model Architecture</th>
                  <th className="p-3.5">Specialized Task</th>
                  <th className="p-3.5">Inference Latency</th>
                  <th className="p-3.5">Cost / 1k Tokens</th>
                  <th className="p-3.5">Quality Metric</th>
                  <th className="p-3.5">Role</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/[0.05]">
                {benchmarks.map((bm, idx) => (
                  <tr key={idx} className="hover:bg-white/[0.02] transition-colors">
                    <td className="p-3.5 font-bold text-slate-100 flex items-center gap-2">
                      <Cpu className="w-3.5 h-3.5 text-purple-400" />
                      <span>{bm.model}</span>
                    </td>
                    <td className="p-3.5 text-slate-300">{bm.task}</td>
                    <td className="p-3.5 text-amber-400 font-bold">{bm.latency}</td>
                    <td className="p-3.5 text-slate-400">{bm.costPer1k}</td>
                    <td className="p-3.5 text-emerald-400 font-bold">{bm.quality}</td>
                    <td className="p-3.5">
                      <span className="px-2 py-0.5 rounded text-[10px] bg-cyan-500/15 text-cyan-300 border border-cyan-500/30">
                        {bm.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
