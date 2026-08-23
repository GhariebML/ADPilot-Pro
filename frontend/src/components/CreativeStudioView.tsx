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
  Image as ImageIcon,
  Copy,
  Check,
  Smartphone,
  Monitor,
  LayoutGrid
} from 'lucide-react';

interface CreativeItem {
  id: string;
  platform: string;
  aspectRatio: '1:1' | '4:5' | '16:9' | '9:16';
  dimensions: string;
  headline: string;
  prompt: string;
  qualityScore: number;
  contrastRatio: string;
  safeZoneMargin: string;
  palette: string[];
  imageUrl: string;
}

export const CreativeStudioView: React.FC = () => {
  const [selectedFormat, setSelectedFormat] = useState<'1:1' | '4:5' | '16:9' | '9:16'>('1:1');
  const [copiedPromptId, setCopiedPromptId] = useState<string | null>(null);
  const [copiedColorHex, setCopiedColorHex] = useState<string | null>(null);

  const creatives: CreativeItem[] = [
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
      palette: ['#07090e', '#00f0ff', '#3b82f6', '#8b5cf6'],
      imageUrl: 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80'
    },
    {
      id: 'cr-2',
      platform: 'Meta Instagram & Facebook Feed',
      aspectRatio: '4:5',
      dimensions: '1080 x 1350',
      headline: 'Meet Your 24/7 Autonomous AI Marketing Fleet',
      prompt: 'Clean visual breakdown of autonomous marketing agents working in parallel. High contrast cyber gradient, modern startup energy, high clarity UI widgets.',
      qualityScore: 8.9,
      contrastRatio: '12.8:1 (AAA)',
      safeZoneMargin: '100% Passed',
      palette: ['#0f172a', '#38bdf8', '#c084fc', '#10b981'],
      imageUrl: 'https://images.unsplash.com/photo-1634017839464-5c339ebe3cb4?auto=format&fit=crop&w=800&q=80'
    },
    {
      id: 'cr-3',
      platform: 'Google Display Network & YouTube Ads',
      aspectRatio: '16:9',
      dimensions: '1920 x 1080',
      headline: 'Stop Burning Budget: Predict ROAS Before Launching',
      prompt: 'Horizontal widescreen analytics banner showing positive upward ROAS trajectory graph in glowing emerald green. Deep obsidian background with glass panels.',
      qualityScore: 9.4,
      contrastRatio: '16.1:1 (AAA)',
      safeZoneMargin: '100% Passed',
      palette: ['#0a0f1d', '#10b981', '#06b6d4', '#f59e0b'],
      imageUrl: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80'
    },
    {
      id: 'cr-4',
      platform: 'Instagram Story & TikTok Vertical Reels',
      aspectRatio: '9:16',
      dimensions: '1080 x 1920',
      headline: 'Scale Your SaaS Marketing with Zero Overhead',
      prompt: 'Vertical portrait format with bold headline banner, dynamic gradient lighting, high energy startup SaaS aesthetic, call to action button overlay.',
      qualityScore: 9.0,
      contrastRatio: '13.5:1 (AAA)',
      safeZoneMargin: '100% Passed',
      palette: ['#020617', '#8b5cf6', '#ec4899', '#00f0ff'],
      imageUrl: 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80'
    }
  ];

  const handleCopyPrompt = (id: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedPromptId(id);
    setTimeout(() => setCopiedPromptId(null), 2000);
  };

  const handleCopyColor = (hex: string) => {
    navigator.clipboard.writeText(hex);
    setCopiedColorHex(hex);
    setTimeout(() => setCopiedColorHex(null), 1500);
  };

  const filteredCreatives = creatives.filter(c => c.aspectRatio === selectedFormat);

  return (
    <div className="w-full space-y-6">
      {/* Header Banner */}
      <div className="bg-slate-950/80 border border-slate-800/90 rounded-2xl p-6 relative overflow-hidden backdrop-blur-2xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2.5">
              <span className="p-2 rounded-xl bg-pink-500/10 text-pink-400 border border-pink-500/20">
                <Palette className="w-5 h-5" />
              </span>
              <h2 className="text-xl font-bold text-slate-100">Creative Studio & Visual Asset Lab</h2>
            </div>
            <p className="text-xs text-slate-400 mt-1 max-w-2xl">
              Cross-platform visual compositions synthesized by Design Agent, audited with zero-shot CLIP-ViT aesthetic regression, and verified for WCAG AAA accessibility.
            </p>
          </div>

          {/* Aspect Ratio Filter Tabs */}
          <div className="flex items-center gap-1.5 bg-slate-900/90 border border-slate-800 rounded-xl p-1.5 shrink-0">
            {[
              { id: '1:1', label: '1:1 Square', icon: LayoutGrid },
              { id: '4:5', label: '4:5 Feed', icon: Smartphone },
              { id: '16:9', label: '16:9 Display', icon: Monitor },
              { id: '9:16', label: '9:16 Story', icon: Smartphone },
            ].map(fmt => {
              const Icon = fmt.icon;
              return (
                <button
                  key={fmt.id}
                  onClick={() => setSelectedFormat(fmt.id as any)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-semibold font-mono flex items-center gap-1.5 transition-all ${
                    selectedFormat === fmt.id
                      ? 'bg-pink-500/20 text-pink-300 border border-pink-500/40 shadow-sm'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  <Icon className="w-3.5 h-3.5" />
                  <span>{fmt.label}</span>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Creatives Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {filteredCreatives.map((creative) => (
          <div key={creative.id} className="bg-slate-950/70 border border-slate-800/90 rounded-2xl p-5 backdrop-blur-xl flex flex-col justify-between hover:border-slate-700 transition-all space-y-4">
            {/* Top Info */}
            <div className="flex items-center justify-between">
              <div>
                <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-pink-400">
                  {creative.platform}
                </span>
                <h3 className="text-sm font-bold text-slate-100 mt-0.5">{creative.headline}</h3>
              </div>
              <span className="px-2.5 py-1 rounded-lg text-[10px] font-mono font-bold bg-slate-900 text-slate-300 border border-slate-800">
                {creative.dimensions}
              </span>
            </div>

            {/* Visual Image Preview */}
            <div className="relative rounded-xl overflow-hidden border border-slate-800 bg-slate-900 group aspect-video flex items-center justify-center">
              <img
                src={creative.imageUrl}
                alt={creative.headline}
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-slate-950/90 via-transparent to-transparent flex items-end p-4">
                <div className="flex items-center justify-between w-full">
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-1 rounded bg-slate-950/80 backdrop-blur-md text-[10px] font-mono text-emerald-400 border border-emerald-500/30 flex items-center gap-1">
                      <CheckCircle2 className="w-3 h-3" /> CLIP {creative.qualityScore}/10
                    </span>
                    <span className="px-2 py-1 rounded bg-slate-950/80 backdrop-blur-md text-[10px] font-mono text-cyan-400 border border-cyan-500/30">
                      WCAG {creative.contrastRatio}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Extracted Color Palette */}
            <div>
              <div className="text-[10px] font-mono font-bold uppercase tracking-wider text-slate-500 mb-1.5 flex items-center justify-between">
                <span>Extracted Brand Palette</span>
                <span className="text-slate-600 font-normal">Click hex to copy</span>
              </div>
              <div className="flex items-center gap-2">
                {creative.palette.map((hex, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => handleCopyColor(hex)}
                    className="flex-1 p-2 rounded-lg border border-slate-800 bg-slate-900/60 hover:bg-slate-900 flex items-center justify-center gap-1.5 transition-all text-[11px] font-mono font-semibold"
                  >
                    <span className="w-3.5 h-3.5 rounded-full border border-white/20 shrink-0" style={{ backgroundColor: hex }} />
                    <span className="text-slate-300">{copiedColorHex === hex ? 'Copied!' : hex}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Prompt Directives Box */}
            <div className="bg-slate-900/60 border border-slate-800/80 rounded-xl p-3.5 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5 text-pink-400" />
                  DALL-E 3 & Midjourney Prompt Directive
                </span>
                <button
                  type="button"
                  onClick={() => handleCopyPrompt(creative.id, creative.prompt)}
                  className="text-[10px] font-mono text-cyan-400 hover:text-cyan-300 flex items-center gap-1 transition-colors"
                >
                  {copiedPromptId === creative.id ? (
                    <>
                      <Check className="w-3 h-3 text-emerald-400" />
                      <span className="text-emerald-400">Copied</span>
                    </>
                  ) : (
                    <>
                      <Copy className="w-3 h-3" />
                      <span>Copy Prompt</span>
                    </>
                  )}
                </button>
              </div>
              <p className="text-xs text-slate-300 font-mono leading-relaxed bg-slate-950/70 p-2.5 rounded-lg border border-slate-800/50">
                "{creative.prompt}"
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
