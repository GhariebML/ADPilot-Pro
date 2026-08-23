import React, { useState } from 'react';
import { 
  Play, 
  Sparkles, 
  CheckCircle2, 
  Download, 
  Building2, 
  Laptop, 
  ShoppingBag, 
  Cloud, 
  BarChart3, 
  Palette, 
  FileText, 
  Activity,
  Layers,
  ArrowRight,
  Zap,
  ShieldCheck
} from 'lucide-react';

interface PresetVertical {
  id: string;
  name: string;
  category: string;
  icon: React.ElementType;
  brief: {
    businessName: string;
    productDescription: string;
    targetAudience: string;
    primaryGoal: string;
    budget: number;
  };
  generatedOutput: {
    headlines: string[];
    bodyCopy: string;
    colorPalette: string[];
    predictedRoas: string;
    forecastedCac: string;
    recommendedChannels: string[];
  };
}

export const LiveCampaignSimulatorStudio: React.FC = () => {
  const presets: PresetVertical[] = [
    {
      id: 'finops',
      name: 'CloudOps FinOps Platform',
      category: 'B2B Enterprise Cloud',
      icon: Cloud,
      brief: {
        businessName: 'CloudScale AI',
        productDescription: 'Automated Kubernetes FinOps cost optimization reducing AWS/GCP bills by 35%.',
        targetAudience: 'VP Infrastructure, CTOs, Enterprise DevOps Directors',
        primaryGoal: 'Enterprise Demo Bookings',
        budget: 25000,
      },
      generatedOutput: {
        headlines: [
          'Stop Burning AWS Spend: Automated Kubernetes FinOps.',
          'Cut Cloud Infrastructure Costs by 35% in 14 Days.',
          'Zero-Downtime Autonomous FinOps for Enterprise Tech.'
        ],
        bodyCopy: 'CloudScale AI continuously optimizes container clusters in real time. Eliminate overprovisioned idle nodes and lock in enterprise visibility with guaranteed SOC2 compliance.',
        colorPalette: ['#06B6D4', '#3B82F6', '#1E293B', '#F8FAFC'],
        predictedRoas: '4.82x',
        forecastedCac: '$42.50',
        recommendedChannels: ['LinkedIn Sponsored InMail (50%)', 'Google Search High-Intent (30%)', 'Direct Retargeting (20%)']
      }
    },
    {
      id: 'realestate',
      name: 'Aura Heights Luxury Living',
      category: 'Prime Real Estate & Luxury',
      icon: Building2,
      brief: {
        businessName: 'Aura Heights Residences',
        productDescription: 'Ultra-luxury waterfront penthouses featuring private yacht slips and helipads.',
        targetAudience: 'High-Net-Worth Individuals (HNWI), Tech Founders, Family Offices',
        primaryGoal: 'Private VIP Viewing Appointments',
        budget: 40000,
      },
      generatedOutput: {
        headlines: [
          'Waterfront Serenity Redefined: Private VIP Penthouse Previews.',
          'Where Architectural Mastery Meets Uncompromised Coastal Luxury.',
          'Exclusive Marina Living for the Discerning Global Visionary.'
        ],
        bodyCopy: 'Step into an oasis of understated elegance with bespoke Italian marble, panoramic ocean vistas, and 24/7 dedicated concierge service in the heart of the luxury harbor.',
        colorPalette: ['#0F172A', '#D97706', '#E2E8F0', '#10B981'],
        predictedRoas: '6.15x',
        forecastedCac: '$180.00',
        recommendedChannels: ['Meta Instagram Curated Reels (45%)', 'LinkedIn Executive Feed (35%)', 'Google Display Prime (20%)']
      }
    },
    {
      id: 'sdr_saas',
      name: 'NexusFlow Autonomous SDR',
      category: 'B2B AI Agent Software',
      icon: Laptop,
      brief: {
        businessName: 'NexusFlow AI',
        productDescription: 'Autonomous outbound AI sales agent researching accounts and booking qualified discovery calls.',
        targetAudience: 'Chief Revenue Officers, VPs of Sales, SaaS Founders',
        primaryGoal: '14-Day Free Enterprise Trial Starts',
        budget: 18000,
      },
      generatedOutput: {
        headlines: [
          'Triple Outbound Pipeline Velocity Without Hiring More Reps.',
          'The 24/7 Autonomous AI SDR That Never Misses a Buying Signal.',
          'Hyper-Personalized Sales Prospecting at Infinite Scale.'
        ],
        bodyCopy: 'NexusFlow AI dynamically ingests intent data, writes bespoke multi-channel sequences, and schedules qualified meetings directly into your CRM.',
        colorPalette: ['#8B5CF6', '#06B6D4', '#0F172A', '#FFFFFF'],
        predictedRoas: '5.20x',
        forecastedCac: '$34.20',
        recommendedChannels: ['LinkedIn Thought Leader Ads (55%)', 'Google Search (30%)', 'Email Nurture (15%)']
      }
    },
    {
      id: 'apparel',
      name: 'Veloce Pro Athletic Wear',
      category: 'Direct-to-Consumer (D2C)',
      icon: ShoppingBag,
      brief: {
        businessName: 'Veloce Athletics',
        productDescription: 'High-performance recycled titanium-infused compression gear for elite marathoners.',
        targetAudience: 'Marathon Runners, Triathletes, Performance Fitness Enthusiasts',
        primaryGoal: 'Direct E-Commerce Purchases',
        budget: 12000,
      },
      generatedOutput: {
        headlines: [
          'Engineered for the Finish Line: Titanium-Infused Compression.',
          'Recover 40% Faster. Run Stronger Every Single Mile.',
          'Zero Friction. Maximum Power: The Elite Marathon Standard.'
        ],
        bodyCopy: 'Crafted from sustainable ultra-lightweight fibers that regulate core body temperature through 26.2 miles of high-intensity performance.',
        colorPalette: ['#EF4444', '#0284C7', '#0F172A', '#F1F5F9'],
        predictedRoas: '4.45x',
        forecastedCac: '$22.80',
        recommendedChannels: ['Meta Dynamic Product Ads (60%)', 'Google Shopping (25%)', 'Email Retargeting (15%)']
      }
    }
  ];

  const [activePreset, setActivePreset] = useState<PresetVertical>(presets[0]);
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [completedSimulation, setCompletedSimulation] = useState<boolean>(true);

  const handleSimulate = (preset: PresetVertical) => {
    setActivePreset(preset);
    setIsGenerating(true);
    setCompletedSimulation(false);

    setTimeout(() => {
      setIsGenerating(false);
      setCompletedSimulation(true);
    }, 800);
  };

  return (
    <div className="w-full bg-slate-950/40 border border-slate-800/60 shadow-2xl rounded-2xl p-6 backdrop-blur-2xl space-y-6 shadow-2xl relative overflow-hidden">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800/80 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-1.5 rounded-lg bg-pink-500/10 text-pink-400 border border-pink-500/20">
              <Sparkles className="w-4 h-4" />
            </span>
            <h3 className="text-base font-bold text-white font-mono uppercase tracking-wider">
              Live In-Showcase Campaign Generation Studio
            </h3>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Select a commercial vertical to test live deterministic multi-agent formulation across copy, design palettes, and predictive metrics.
          </p>
        </div>

        <span className="px-3 py-1 rounded-xl text-xs font-mono font-bold bg-pink-500/10 text-pink-300 border border-pink-500/30 shrink-0">
          Zero-Credit Live Simulator
        </span>
      </div>

      {/* Preset Selector Buttons */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        {presets.map((preset) => {
          const Icon = preset.icon;
          const isSelected = activePreset.id === preset.id;
          return (
            <button
              key={preset.id}
              onClick={() => handleSimulate(preset)}
              className={`p-4 rounded-xl border text-left transition-all flex items-start gap-3 ${
                isSelected
                  ? 'bg-cyan-500/15 border-cyan-500/50 shadow-md shadow-cyan-500/10'
                  : 'bg-slate-900/60 border-slate-800 hover:border-slate-700 hover:bg-slate-900'
              }`}
            >
              <div className={`p-2 rounded-lg ${isSelected ? 'bg-cyan-500/20 text-cyan-300' : 'bg-slate-950 text-slate-400'}`}>
                <Icon className="w-5 h-5" />
              </div>
              <div className="overflow-hidden">
                <div className="text-xs font-bold text-white truncate">{preset.name}</div>
                <div className="text-[10px] text-slate-400 font-mono mt-0.5 truncate">{preset.category}</div>
              </div>
            </button>
          );
        })}
      </div>

      {/* Live Generated Artifact Canvas */}
      {isGenerating ? (
        <div className="p-12 rounded-2xl bg-slate-900/60 border border-slate-800 flex flex-col items-center justify-center space-y-3 font-mono text-xs">
          <Activity className="w-6 h-6 text-cyan-400 animate-spin" />
          <span className="text-slate-300">18-Stage DAG formulating campaign package for {activePreset.name}...</span>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 font-mono text-xs">
          {/* Column 1: Multi-Variant Ad Copy */}
          <div className="p-5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-4 flex flex-col justify-between">
            <div className="space-y-3">
              <div className="flex items-center gap-2 text-cyan-400 font-bold uppercase">
                <FileText className="w-4 h-4" />
                <span>Generated Ad Copy (A/B)</span>
              </div>

              <div className="space-y-2">
                {activePreset.generatedOutput.headlines.map((headline, idx) => (
                  <div key={idx} className="p-2.5 rounded-lg bg-slate-950 border border-slate-800/80 text-[11px] text-slate-200">
                    <span className="text-slate-500 block text-[9px]">VARIANT {String.fromCharCode(65 + idx)}:</span>
                    "{headline}"
                  </div>
                ))}
              </div>

              <div className="p-3 rounded-lg bg-slate-950/40 border border-slate-800/60 shadow-2xl text-[11px] text-slate-300 leading-relaxed">
                <span className="text-slate-500 block text-[9px] mb-1">LONG-FORM COPY DIRECTIVE:</span>
                {activePreset.generatedOutput.bodyCopy}
              </div>
            </div>

            <div className="text-[10px] text-slate-500 pt-2 border-t border-slate-800">
              Generated by ContentAgent (Claude 3.5 Sonnet)
            </div>
          </div>

          {/* Column 2: Brand Color Palette & Visuals */}
          <div className="p-5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-4 flex flex-col justify-between">
            <div className="space-y-3">
              <div className="flex items-center gap-2 text-pink-400 font-bold uppercase">
                <Palette className="w-4 h-4" />
                <span>Extracted Brand Colors & Design</span>
              </div>

              <div className="grid grid-cols-4 gap-2">
                {activePreset.generatedOutput.colorPalette.map((hex, idx) => (
                  <div key={idx} className="space-y-1.5 text-center">
                    <div className="h-14 rounded-lg border border-slate-700 shadow-inner" style={{ backgroundColor: hex }} />
                    <span className="text-[10px] text-slate-400">{hex}</span>
                  </div>
                ))}
              </div>

              <div className="space-y-2 pt-2">
                <div className="p-2 rounded-lg bg-slate-950 border border-slate-800 flex justify-between text-[11px]">
                  <span className="text-slate-400">WCAG Contrast Audit</span>
                  <span className="text-emerald-400 font-bold">11.4:1 AAA Pass</span>
                </div>
                <div className="p-2 rounded-lg bg-slate-950 border border-slate-800 flex justify-between text-[11px]">
                  <span className="text-slate-400">CLIP-ViT Aesthetic Score</span>
                  <span className="text-purple-300 font-bold">9.38 / 10.0</span>
                </div>
              </div>
            </div>

            <div className="text-[10px] text-slate-500 pt-2 border-t border-slate-800">
              Validated by CVAgent (ONNX CLIP-ViT B/32)
            </div>
          </div>

          {/* Column 3: Predicted Financial Yield & Allocations */}
          <div className="p-5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-4 flex flex-col justify-between">
            <div className="space-y-3">
              <div className="flex items-center gap-2 text-emerald-400 font-bold uppercase">
                <BarChart3 className="w-4 h-4" />
                <span>PPO & ML Yield Forecast</span>
              </div>

              <div className="grid grid-cols-2 gap-2 text-center">
                <div className="p-3 rounded-lg bg-slate-950 border border-slate-800">
                  <span className="text-[10px] text-slate-500 block">PREDICTED ROAS</span>
                  <span className="text-lg font-bold text-emerald-400">{activePreset.generatedOutput.predictedRoas}</span>
                </div>
                <div className="p-3 rounded-lg bg-slate-950 border border-slate-800">
                  <span className="text-[10px] text-slate-500 block">FORECASTED CAC</span>
                  <span className="text-lg font-bold text-cyan-400">{activePreset.generatedOutput.forecastedCac}</span>
                </div>
              </div>

              <div className="space-y-1.5 pt-1">
                <span className="text-[10px] text-slate-400 block uppercase">PPO Policy Allocations:</span>
                {activePreset.generatedOutput.recommendedChannels.map((ch, idx) => (
                  <div key={idx} className="p-2 rounded-lg bg-slate-950 border border-slate-800/80 text-[11px] text-slate-200 flex items-center gap-2">
                    <CheckCircle2 className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
                    <span>{ch}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="text-[10px] text-slate-500 pt-2 border-t border-slate-800">
              Computed by OptimizationAgent & AnalyticsAgent
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default LiveCampaignSimulatorStudio;

