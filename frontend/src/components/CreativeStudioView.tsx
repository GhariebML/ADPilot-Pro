import React, { useState } from 'react';
import { 
  Palette, 
  Sparkles, 
  Layers, 
  Download, 
  CheckCircle2, 
  Sliders, 
  Eye, 
  RefreshCw,
  Image as ImageIcon
} from 'lucide-react';

export const CreativeStudioView: React.FC = () => {
  const [selectedFormat, setSelectedFormat] = useState<'1:1' | '16:9' | '9:16'>('1:1');

  const creatives = [
    {
      id: 'cr-1',
      platform: 'LinkedIn Sponsored Content',
      aspectRatio: '1:1',
      dimensions: '1080 x 1080',
      headline: 'Autonomous B2B Marketing Operating System',
      prompt: 'Sleek futuristic 3D enterprise interface floating over dark titanium slate. Electric blue and cyan neon data streams. Clean typography and glassmorphic dashboards. Minimalist, premium tech aesthetic.',
      qualityScore: 9.2,
      contrastRatio: '14.2:1 (AAA)',
      safeZoneMargin: '100% Passed',
      imageUrl: 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80'
    },
    {
      id: 'cr-2',
      platform: 'Meta Ads Feed',
      aspectRatio: '1:1',
      dimensions: '1080 x 1080',
      headline: 'Meet Your 24/7 AI Marketing Team',
      prompt: 'Clean visual breakdown of autonomous marketing agents working in parallel. High contrast cyber gradient, modern startup energy, high clarity UI widgets.',
      qualityScore: 8.9,
      contrastRatio: '12.8:1 (AAA)',
      safeZoneMargin: '100% Passed',
      imageUrl: 'https://images.unsplash.com/photo-1634017839464-5c339ebe3cb4?auto=format&fit=crop&w=800&q=80'
    },
    {
      id: 'cr-3',
      platform: 'Google Display Network',
      aspectRatio: '16:9',
      dimensions: '1920 x 1080',
      headline: 'Stop Burning Budget: Predict ROAS Before Launching',
      prompt: 'Horizontal widescreen analytics banner showing positive upward ROAS trajectory graph in glowing emerald green. Deep obsidian background with glass panels.',
      qualityScore: 9.4,
      contrastRatio: '16.1:1 (AAA)',
      safeZoneMargin: '100% Passed',
      imageUrl: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80'
    },
    {
      id: 'cr-4',
      platform: 'Instagram Story & Reels',
      aspectRatio: '9:16',
      dimensions: '1080 x 1920',
      headline: 'Scale Your SaaS Marketing with Zero Overhead',
      prompt: 'Vertical portrait format with bold headline banner, dynamic gradient lighting, high energy startup SaaS aesthetic, call to action button overlay.',
      qualityScore: 9.0,
      contrastRatio: '13.5:1 (AAA)',
      safeZoneMargin: '100% Passed',
      imageUrl: 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80'
    }
  ];

  const filteredCreatives = creatives.filter(c => c.aspectRatio === selectedFormat);

  return (
    <div className="w-full space-y-6">
      {/* Header Banner */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 relative overflow-hidden backdrop-blur-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2.5">
              <span className="p-2 rounded-xl bg-pink-500/10 text-pink-400 border border-pink-500/20">
                <Palette className="w-5 h-5" />
              </span>
              <h2 className="text-xl font-bold text-slate-100">Design Agent & Nano Banana Creative Studio</h2>
            </div>
            <p className="text-xs text-slate-400 mt-1 max-w-2xl">
              Multi-format creative generation studio synthesizing prompt directives, brand palettes, and typography guidelines into cross-platform visual assets validated by Computer Vision (CLIP-ViT).
            </p>
          </div>

          {/* Aspect Ratio Filter Tabs */}
          <div className="flex items-center gap-2 bg-slate-950/80 border border-slate-800 rounded-xl p-1.5 shrink-0">
            {(['1:1', '16:9', '9:16'] as const).map(fmt => (
              <button
                key={fmt}
                onClick={() => setSelectedFormat(fmt)}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold font-mono transition-all ${
                  selectedFormat === fmt
                    ? 'bg-pink-500/20 text-pink-300 border border-pink-500/40 shadow-sm'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {fmt} Aspect
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Creatives Showcase Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {filteredCreatives.map(cr => (
          <div key={cr.id} className="bg-slate-900/80 border border-slate-800/90 rounded-2xl overflow-hidden backdrop-blur-xl flex flex-col justify-between shadow-xl">
            {/* Image Preview Window */}
            <div className="relative bg-slate-950 aspect-video sm:aspect-auto sm:h-64 overflow-hidden group">
              <img 
                src={cr.imageUrl} 
                alt={cr.headline} 
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-transparent to-transparent opacity-80" />
              
              <div className="absolute top-3 left-3 flex items-center gap-2">
                <span className="px-2.5 py-1 rounded-md text-[11px] font-mono font-bold bg-slate-950/80 text-cyan-300 border border-slate-700 backdrop-blur-md">
                  {cr.platform}
                </span>
                <span className="px-2 py-1 rounded-md text-[10px] font-mono bg-slate-950/80 text-slate-300 border border-slate-700 backdrop-blur-md">
                  {cr.dimensions}
                </span>
              </div>

              <div className="absolute bottom-3 left-3 right-3">
                <h4 className="text-sm font-bold text-white drop-shadow-md">
                  {cr.headline}
                </h4>
              </div>
            </div>

            {/* Creative Directives & Quality Scores */}
            <div className="p-5 space-y-4">
              <div>
                <div className="text-[11px] font-mono uppercase text-slate-500 mb-1">Diffusion Prompt Directive</div>
                <p className="text-xs text-slate-300 bg-slate-950/70 p-3 rounded-xl border border-slate-800 leading-relaxed font-mono">
                  {cr.prompt}
                </p>
              </div>

              {/* CV Quality Gate Stats */}
              <div className="grid grid-cols-3 gap-2 text-center text-xs font-mono">
                <div className="p-2 rounded-lg bg-slate-950 border border-slate-800">
                  <div className="text-[10px] text-slate-500 uppercase">CLIP Quality</div>
                  <div className="text-emerald-400 font-bold mt-0.5">{cr.qualityScore} / 10</div>
                </div>
                <div className="p-2 rounded-lg bg-slate-950 border border-slate-800">
                  <div className="text-[10px] text-slate-500 uppercase">Contrast</div>
                  <div className="text-cyan-400 font-bold mt-0.5">{cr.contrastRatio}</div>
                </div>
                <div className="p-2 rounded-lg bg-slate-950 border border-slate-800">
                  <div className="text-[10px] text-slate-500 uppercase">Safe Margin</div>
                  <div className="text-purple-400 font-bold mt-0.5">{cr.safeZoneMargin}</div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
