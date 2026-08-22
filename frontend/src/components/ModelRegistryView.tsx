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
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 relative overflow-hidden backdrop-blur-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2.5">
              <span className="p-2 rounded-xl bg-purple-500/10 text-purple-400 border border-purple-500/20">
                <Box className="w-5 h-5" />
              </span>
              <h2 className="text-xl font-bold text-slate-100">Custom Machine Learning & Neural Model Registry</h2>
            </div>
            <p className="text-xs text-slate-400 mt-1 max-w-2xl">
              Catalog and benchmark arena for custom trained neural weights, statistical forecasters, and vision scoring models powering ADPilot.
            </p>
          </div>

          {/* Toggle Tabs */}
          <div className="flex items-center gap-2 bg-slate-950/80 border border-slate-800 rounded-xl p-1.5 shrink-0">
            <button
              onClick={() => setActiveTab('catalog')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold font-mono transition-all ${
                activeTab === 'catalog'
                  ? 'bg-purple-500/20 text-purple-300 border border-purple-500/40 shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Model Artifacts ({models.length})
            </button>
            <button
              onClick={() => setActiveTab('arena')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold font-mono transition-all ${
                activeTab === 'arena'
                  ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm'
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
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {models.map(model => (
            <div key={model.id} className="bg-slate-900/80 border border-slate-800/90 rounded-2xl p-5 backdrop-blur-xl flex flex-col justify-between hover:border-slate-700 transition-all">
              <div>
                <div className="flex items-start justify-between gap-2 mb-3">
                  <div>
                    <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-blue-500/10 text-blue-400 border border-blue-500/20">
                      {model.category}
                    </span>
                    <h3 className="text-sm font-bold text-slate-100 mt-2">{model.name}</h3>
                  </div>
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 shrink-0">
                    {model.status}
                  </span>
                </div>

                {/* Artifact File Path */}
                <div className="p-2.5 rounded-xl bg-slate-950 border border-slate-800/80 font-mono text-[11px] text-slate-400 mb-4 truncate">
                  <span className="text-slate-500">File: </span>
                  <span className="text-cyan-400 font-medium">{model.artifactPath}</span>
                </div>

                {/* Specs Table */}
                <div className="space-y-2 text-xs font-mono">
                  <div className="flex justify-between py-1 border-b border-slate-800/60">
                    <span className="text-slate-500">Agent:</span>
                    <span className="text-slate-300 font-semibold">{model.responsibleAgent}</span>
                  </div>
                  <div className="flex justify-between py-1 border-b border-slate-800/60">
                    <span className="text-slate-500">Framework:</span>
                    <span className="text-purple-300 font-semibold">{model.framework}</span>
                  </div>
                  <div className="flex justify-between py-1 border-b border-slate-800/60">
                    <span className="text-slate-500">Input Schema:</span>
                    <span className="text-slate-300 truncate max-w-[160px]">{model.inputDim}</span>
                  </div>
                  <div className="flex justify-between py-1 border-b border-slate-800/60">
                    <span className="text-slate-500">Output Schema:</span>
                    <span className="text-slate-300 truncate max-w-[160px]">{model.outputDim}</span>
                  </div>
                </div>
              </div>

              {/* Telemetry Footer */}
              <div className="pt-4 mt-4 border-t border-slate-800 flex items-center justify-between text-xs font-mono">
                <span className="text-slate-400">
                  Latency: <strong className="text-slate-200">{model.inferenceLatency}</strong>
                </span>
                <span className="text-emerald-400 font-bold">{model.accuracyOrReward}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* VIEW 2: Benchmark Arena Table */}
      {activeTab === 'arena' && (
        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 backdrop-blur-xl space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800">
            <div>
              <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
                <Award className="w-4 h-4 text-cyan-400" />
                Fleet Model Latency, Cost & Quality Arena
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">
                Benchmark evaluation measuring real-time inference speed, cost efficiency, and accuracy across LLMs and custom ML weights.
              </p>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono">
              <thead>
                <tr className="border-b border-slate-800 text-[10px] uppercase text-slate-500 bg-slate-950/60">
                  <th className="py-3 px-4 rounded-l-lg">Model Architecture</th>
                  <th className="py-3 px-4">Primary Agency Task</th>
                  <th className="py-3 px-4">Inference Latency</th>
                  <th className="py-3 px-4">Cost / 1k Tokens</th>
                  <th className="py-3 px-4">Benchmark Metric</th>
                  <th className="py-3 px-4 rounded-r-lg">Deployment Role</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {benchmarks.map((bm, i) => (
                  <tr key={i} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-3 px-4 font-bold text-cyan-300">{bm.model}</td>
                    <td className="py-3 px-4 text-slate-300 font-sans">{bm.task}</td>
                    <td className="py-3 px-4 text-slate-200">{bm.latency}</td>
                    <td className="py-3 px-4 text-emerald-400 font-bold">{bm.costPer1k}</td>
                    <td className="py-3 px-4 text-purple-300">{bm.quality}</td>
                    <td className="py-3 px-4">
                      <span className="px-2 py-0.5 rounded text-[10px] bg-slate-950 text-slate-400 border border-slate-800">
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
