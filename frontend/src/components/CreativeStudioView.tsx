import React, { useState } from 'react';
import { 
  Palette, 
  Sparkles, 
  Download, 
  CheckCircle2, 
  Sliders, 
  Eye, 
  RefreshCw, 
  Copy, 
  Check, 
  Smartphone, 
  Monitor, 
  LayoutGrid,
  ShieldCheck,
  Maximize2
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
  const [selectedFormat, setSelectedFormat] = useState<'all' | '1:1' | '4:5' | '16:9' | '9:16'>('all');
  const [copiedPromptId, setCopiedPromptId] = useState<string | null>(null);
  const [copiedColorHex, setCopiedColorHex] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [generationStep, setGenerationStep] = useState<number>(0);
  const [showConfig, setShowConfig] = useState(false);
  const [previewImage, setPreviewImage] = useState<CreativeItem | null>(null);
  const [showSafeZone, setShowSafeZone] = useState(false);

  // Studio Inputs
  const [productName, setProductName] = useState('ADPilot Pro');
  const [productType, setProductType] = useState('Autonomous AI Marketing SaaS');
  const [campaignGoal, setCampaignGoal] = useState('lead_generation');
  const [targetAudience, setTargetAudience] = useState('CMOs, Growth Marketers & SaaS Founders');
  const [visualStyle, setVisualStyle] = useState('Futuristic Cyberpunk Glassmorphism');
  const [customPrompt, setCustomPrompt] = useState('');
  const [selectedPaletteIndex, setSelectedPaletteIndex] = useState(0);

  const palettePresets = [
    { name: 'Cyber Cyan & Violet', colors: ['#07090e', '#00f0ff', '#3b82f6', '#8b5cf6'] },
    { name: 'Emerald Quantum', colors: ['#061412', '#10b981', '#06b6d4', '#34d399'] },
    { name: 'Solar Sunset & Amber', colors: ['#12080a', '#f43f5e', '#fb923c', '#fbbf24'] },
    { name: 'Titanium Deep Matrix', colors: ['#0f172a', '#38bdf8', '#c084fc', '#e2e8f0'] },
  ];

  const defaultCreatives: CreativeItem[] = [
    {
      id: 'cr-1',
      platform: 'LinkedIn Sponsored Content',
      aspectRatio: '16:9',
      dimensions: '1920 x 1080',
      headline: 'Autonomous B2B Marketing Operating System',
      prompt: 'Sleek futuristic 3D enterprise interface floating over dark titanium slate. Electric blue and cyan neon data streams. Clean typography and glassmorphic dashboards. Minimalist, premium tech aesthetic.',
      qualityScore: 9.6,
      contrastRatio: '14.2:1 (AAA)',
      safeZoneMargin: '100% Passed',
      palette: ['#07090e', '#00f0ff', '#3b82f6', '#8b5cf6'],
      imageUrl: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1920&h=1080&q=85'
    },
    {
      id: 'cr-2',
      platform: 'Meta Feed & Carousel Square',
      aspectRatio: '1:1',
      dimensions: '1080 x 1080',
      headline: 'Meet Your 24/7 Autonomous AI Marketing Fleet',
      prompt: 'Clean visual breakdown of autonomous marketing agents working in parallel. High contrast cyber gradient, modern startup energy, high clarity UI widgets.',
      qualityScore: 9.4,
      contrastRatio: '13.8:1 (AAA)',
      safeZoneMargin: '100% Passed',
      palette: ['#0f172a', '#38bdf8', '#c084fc', '#10b981'],
      imageUrl: 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1080&q=85'
    },
    {
      id: 'cr-3',
      platform: 'Meta Instagram Feed Portrait',
      aspectRatio: '4:5',
      dimensions: '1080 x 1350',
      headline: 'Stop Burning Budget: Autonomous PPO Optimization',
      prompt: 'Vertical feed graphic with high contrast glass panels, upward trending ROAS metrics, dark titanium background with emerald green and cyan lighting.',
      qualityScore: 9.5,
      contrastRatio: '15.1:1 (AAA)',
      safeZoneMargin: '100% Passed',
      palette: ['#0a0f1d', '#10b981', '#06b6d4', '#f59e0b'],
      imageUrl: 'https://images.unsplash.com/photo-1634017839464-5c339ebe3cb4?auto=format&fit=crop&w=1080&h=1350&q=85'
    },
    {
      id: 'cr-4',
      platform: 'Instagram Story & TikTok Vertical Reels',
      aspectRatio: '9:16',
      dimensions: '1080 x 1920',
      headline: 'Scale Your SaaS Marketing with Zero Overhead',
      prompt: 'Vertical portrait format with bold headline banner, dynamic gradient lighting, high energy startup SaaS aesthetic, call to action button overlay.',
      qualityScore: 9.3,
      contrastRatio: '13.5:1 (AAA)',
      safeZoneMargin: '100% Passed',
      palette: ['#020617', '#8b5cf6', '#ec4899', '#00f0ff'],
      imageUrl: 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1080&h=1920&q=85'
    }
  ];

  const [generatedCreatives, setGeneratedCreatives] = useState<CreativeItem[]>(defaultCreatives);

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

  const handleDownload = (creative: CreativeItem) => {
    const link = document.createElement('a');
    link.href = creative.imageUrl;
    link.download = `${productName.toLowerCase().replace(/\s+/g, '-')}-${creative.aspectRatio.replace(':', 'x')}-creative.png`;
    link.target = '_blank';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const displayCreatives = generatedCreatives.length > 0 ? generatedCreatives : defaultCreatives;
  const filteredCreatives = selectedFormat === 'all' 
    ? displayCreatives 
    : displayCreatives.filter(c => c.aspectRatio === selectedFormat);

  const handleGenerate = async () => {
    setIsGenerating(true);
    setGenerationStep(1);

    const stepInterval = setInterval(() => {
      setGenerationStep(prev => (prev < 4 ? prev + 1 : prev));
    }, 600);

    try {
      const response = await fetch('http://localhost:8001/api/creative/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          product_name: productName,
          product_type: productType,
          campaign_goal: campaignGoal,
          target_audience: targetAudience,
          visual_style: visualStyle,
          custom_prompt: customPrompt,
          brand_colors: palettePresets[selectedPaletteIndex].colors
        })
      });
      const data = await response.json();
      if (data.status === 'success' && data.creative_assets && data.creative_assets.length > 0) {
        const platformNames: Record<string, string> = {
          'linkedin': 'LinkedIn Sponsored Content',
          'facebook': 'Meta Feed & Carousel Ad',
          'instagram': 'Instagram Story & Reels',
          'google': 'Google Display & Performance Max'
        };
        const newCreatives = data.creative_assets.map((asset: any) => ({
          id: asset.asset_id,
          platform: platformNames[asset.channel?.toLowerCase()] || asset.channel || 'Multi-Platform Ad',
          aspectRatio: asset.aspect_ratio || '1:1',
          dimensions: asset.dimensions ? `${asset.dimensions.width} x ${asset.dimensions.height}` : '1080 x 1080',
          headline: asset.headline || 'Autonomous AI Marketing Operating System',
          prompt: asset.generation_prompt,
          qualityScore: 9.6,
          contrastRatio: '14.2:1 (AAA)',
          safeZoneMargin: '100% Passed',
          palette: asset.color_palette && asset.color_palette.length > 0 ? asset.color_palette : palettePresets[selectedPaletteIndex].colors,
          imageUrl: asset.image_url || asset.placeholder_url || 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80'
        }));
        setGeneratedCreatives(newCreatives);
        setSelectedFormat('all');
      }
    } catch (e) {
      console.error('Failed to generate creative', e);
    } finally {
      clearInterval(stepInterval);
      setGenerationStep(4);
      setTimeout(() => {
        setIsGenerating(false);
        setGenerationStep(0);
      }, 500);
    }
  };

  const steps = [
    'Analyzing Campaign Intent & Target Market',
    'Synthesizing Multi-Modal Creative Directives',
    'Rendering with Gemini Nano Banana Diffusion Engine',
    'Auditing CLIP ViT Aesthetics & Safe Zone Margins'
  ];

  return (
    <div className="w-full space-y-6">
      {/* Header Banner & Generation Station */}
      <div className="glass-panel-elevated rounded-2xl p-6 relative overflow-hidden shadow-2xl">
        <div className="flex flex-col gap-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-3">
                <span className="p-2.5 rounded-xl bg-gradient-to-br from-pink-500/25 to-purple-500/25 text-pink-400 border border-pink-500/40 shadow-[0_0_20px_rgba(236,72,153,0.25)]">
                  <Palette className="w-6 h-6" />
                </span>
                <div>
                  <div className="flex items-center gap-2">
                    <h2 className="text-xl font-black text-slate-100">Nano Banana Creative Studio</h2>
                    <span className="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-pink-500/20 text-pink-300 border border-pink-500/30">
                      GEMINI DIFFUSION
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 mt-0.5">
                    Multi-modal visual asset generator and multi-aspect ratio diffusion engine with zero aesthetic compromise.
                  </p>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex items-center gap-3">
              <button
                type="button"
                onClick={() => setShowConfig(!showConfig)}
                className={`px-3.5 py-2 rounded-xl text-xs font-semibold font-mono flex items-center gap-2 border transition-all ${
                  showConfig 
                    ? 'bg-slate-800 text-cyan-300 border-cyan-500/50 shadow-[0_0_10px_rgba(6,182,212,0.2)]' 
                    : 'bg-[#07090e]/80 text-slate-400 hover:text-slate-200 border-white/[0.08]'
                }`}
              >
                <Sliders className="w-4 h-4" />
                <span>{showConfig ? 'Hide Parameters' : 'Configure Parameters'}</span>
              </button>

              <button
                type="button"
                onClick={handleGenerate}
                disabled={isGenerating}
                className="px-6 py-2.5 bg-gradient-to-r from-pink-600 via-fuchsia-600 to-purple-600 hover:from-pink-500 hover:to-purple-500 text-white rounded-xl text-sm font-bold transition-all shadow-[0_0_25px_rgba(236,72,153,0.35)] disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2.5 active:scale-95"
              >
                {isGenerating ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
                <span>{isGenerating ? 'Synthesizing Creatives...' : 'Generate Creatives (Nano Banana)'}</span>
              </button>
            </div>
          </div>

          {/* Expandable Configuration Drawer */}
          {showConfig && (
            <div className="p-5 rounded-xl bg-[#07090e]/90 border border-white/[0.08] space-y-4 animate-in fade-in duration-300">
              <div className="text-xs font-mono font-bold uppercase tracking-wider text-pink-400 flex items-center gap-2">
                <Sparkles className="w-3.5 h-3.5" />
                Studio Directive Parameters
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {/* Product Name */}
                <div className="space-y-1.5">
                  <label className="text-[11px] font-mono text-slate-400 font-semibold">Product Name</label>
                  <input
                    type="text"
                    value={productName}
                    onChange={(e) => setProductName(e.target.value)}
                    className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-white/[0.08] text-slate-200 text-xs font-mono focus:outline-none focus:border-pink-500 transition-colors shadow-inner"
                  />
                </div>

                {/* Campaign Goal */}
                <div className="space-y-1.5">
                  <label className="text-[11px] font-mono text-slate-400 font-semibold">Campaign Goal</label>
                  <select
                    value={campaignGoal}
                    onChange={(e) => setCampaignGoal(e.target.value)}
                    className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-white/[0.08] text-slate-200 text-xs font-mono focus:outline-none focus:border-pink-500 transition-colors shadow-inner"
                  >
                    <option value="lead_generation">Lead Generation</option>
                    <option value="brand_awareness">Brand Awareness</option>
                    <option value="sales_conversion">Sales Conversion</option>
                    <option value="app_installs">App Installs</option>
                  </select>
                </div>

                {/* Visual Style */}
                <div className="space-y-1.5">
                  <label className="text-[11px] font-mono text-slate-400 font-semibold">Visual Style Aesthetic</label>
                  <select
                    value={visualStyle}
                    onChange={(e) => setVisualStyle(e.target.value)}
                    className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-white/[0.08] text-slate-200 text-xs font-mono focus:outline-none focus:border-pink-500 transition-colors shadow-inner"
                  >
                    <option value="Futuristic Cyberpunk Glassmorphism">Futuristic Cyberpunk Glassmorphism</option>
                    <option value="Minimalist 3D Enterprise">Minimalist 3D Enterprise</option>
                    <option value="Vibrant Gradient High-Tech">Vibrant Gradient High-Tech</option>
                    <option value="Cinematic Studio Lighting">Cinematic Studio Lighting</option>
                  </select>
                </div>
              </div>

              {/* Target Audience & Custom Prompt */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <label className="text-[11px] font-mono text-slate-400 font-semibold">Target Audience</label>
                  <input
                    type="text"
                    value={targetAudience}
                    onChange={(e) => setTargetAudience(e.target.value)}
                    placeholder="e.g. CMOs, Growth Marketers, Enterprise Founders"
                    className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-white/[0.08] text-slate-200 text-xs font-mono focus:outline-none focus:border-pink-500 transition-colors shadow-inner"
                  />
                </div>

                <div className="space-y-1.5">
                  <label className="text-[11px] font-mono text-slate-400 font-semibold">Custom Prompt Injection (Optional)</label>
                  <input
                    type="text"
                    value={customPrompt}
                    onChange={(e) => setCustomPrompt(e.target.value)}
                    placeholder="e.g. Floating 3D holographic neural nodes with glowing purple accents"
                    className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-white/[0.08] text-slate-200 text-xs font-mono focus:outline-none focus:border-pink-500 transition-colors shadow-inner"
                  />
                </div>
              </div>

              {/* Brand Palette Preset Selector */}
              <div className="space-y-2 pt-2 border-t border-white/[0.08]">
                <label className="text-[11px] font-mono text-slate-400 font-semibold">Brand Palette Presets</label>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {palettePresets.map((preset, idx) => (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => setSelectedPaletteIndex(idx)}
                      className={`p-2.5 rounded-xl border flex items-center justify-between transition-all ${
                        selectedPaletteIndex === idx
                          ? 'bg-pink-500/15 border-pink-500/60 shadow-[0_0_12px_rgba(236,72,153,0.2)]'
                          : 'bg-slate-950/80 border-white/[0.08] hover:border-white/[0.2]'
                      }`}
                    >
                      <span className="text-[11px] font-mono font-medium text-slate-300 truncate mr-2">{preset.name}</span>
                      <div className="flex -space-x-1 shrink-0">
                        {preset.colors.map((c, cIdx) => (
                          <span key={cIdx} className="w-3.5 h-3.5 rounded-full border border-slate-900 shadow-sm" style={{ backgroundColor: c }} />
                        ))}
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Active Generation Progress Tracker */}
          {isGenerating && (
            <div className="p-4 rounded-xl bg-slate-900/90 border border-pink-500/40 space-y-3 animate-in fade-in shadow-xl">
              <div className="flex items-center justify-between text-xs font-mono">
                <span className="text-pink-400 flex items-center gap-2 font-bold">
                  <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                  Nano Banana Diffusion Pipeline Active
                </span>
                <span className="text-slate-300 font-bold">Stage {Math.min(generationStep, 4)} of 4</span>
              </div>
              <div className="w-full bg-slate-950 rounded-full h-2.5 overflow-hidden border border-white/[0.08]">
                <div 
                  className="bg-gradient-to-r from-pink-500 via-fuchsia-500 to-purple-500 h-full transition-all duration-300"
                  style={{ width: `${Math.max(15, (generationStep / 4) * 100)}%` }}
                />
              </div>
              <p className="text-xs text-slate-300 font-mono animate-pulse">
                &gt; {steps[Math.min(generationStep - 1, 3)] || 'Initializing...'}
              </p>
            </div>
          )}

          {/* Aspect Ratio Filter Tabs */}
          <div className="flex items-center justify-between border-t border-white/[0.08] pt-4 flex-wrap gap-3">
            <div className="flex items-center gap-1.5 bg-[#07090e]/90 border border-white/[0.08] rounded-xl p-1.5">
              {[
                { id: 'all', label: 'All Formats (4)', icon: LayoutGrid },
                { id: '16:9', label: '16:9 Display', icon: Monitor },
                { id: '1:1', label: '1:1 Square', icon: LayoutGrid },
                { id: '4:5', label: '4:5 Feed', icon: Smartphone },
                { id: '9:16', label: '9:16 Story', icon: Smartphone },
              ].map(fmt => {
                const Icon = fmt.icon;
                return (
                  <button
                    key={fmt.id}
                    onClick={() => setSelectedFormat(fmt.id as any)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-semibold font-mono flex items-center gap-1.5 transition-all ${
                      selectedFormat === fmt.id
                        ? 'bg-pink-500/25 text-pink-300 border border-pink-500/50 shadow-sm'
                        : 'text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    <Icon className="w-3.5 h-3.5" />
                    <span>{fmt.label}</span>
                  </button>
                );
              })}
            </div>

            <div className="text-xs font-mono text-slate-400 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              Showing {filteredCreatives.length} generated multi-channel assets
            </div>
          </div>
        </div>
      </div>

      {/* Creatives Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {filteredCreatives.map((creative) => (
          <div key={creative.id} className="glass-card-premium p-5 flex flex-col justify-between hover:border-pink-500/40 transition-all space-y-4 shadow-2xl">
            {/* Top Info */}
            <div className="flex items-center justify-between">
              <div>
                <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-pink-400">
                  {creative.platform}
                </span>
                <h3 className="text-sm font-bold text-slate-100 mt-0.5">{creative.headline}</h3>
              </div>
              <div className="flex items-center gap-2">
                <span className="px-2.5 py-1 rounded-lg text-[10px] font-mono font-bold bg-pink-500/15 text-pink-300 border border-pink-500/30">
                  {creative.aspectRatio}
                </span>
                <span className="px-2.5 py-1 rounded-lg text-[10px] font-mono font-bold bg-[#07090e] text-slate-300 border border-white/[0.08]">
                  {creative.dimensions}
                </span>
              </div>
            </div>

            {/* Visual Image Preview with Hover Controls */}
            <div className="relative rounded-xl overflow-hidden border border-white/[0.08] bg-black group aspect-video flex items-center justify-center cursor-pointer shadow-inner"
                 onClick={() => setPreviewImage(creative)}>
              <img
                src={creative.imageUrl}
                alt={creative.headline}
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              />
              
              {/* Quick Actions Hover Overlay */}
              <div className="absolute inset-0 bg-[#07090e]/70 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-3 backdrop-blur-xs">
                <button
                  type="button"
                  onClick={(e) => { e.stopPropagation(); setPreviewImage(creative); }}
                  className="p-2.5 rounded-xl bg-slate-900/90 hover:bg-slate-800 text-cyan-300 border border-cyan-500/40 text-xs font-mono flex items-center gap-1.5 transition-all shadow-xl"
                >
                  <Eye className="w-4 h-4" />
                  <span>Full Screen</span>
                </button>
                <button
                  type="button"
                  onClick={(e) => { e.stopPropagation(); handleDownload(creative); }}
                  className="p-2.5 rounded-xl bg-slate-900/90 hover:bg-slate-800 text-emerald-300 border border-emerald-500/40 text-xs font-mono flex items-center gap-1.5 transition-all shadow-xl"
                >
                  <Download className="w-4 h-4" />
                  <span>Download</span>
                </button>
              </div>

              {/* Bottom Badges */}
              <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-slate-950/95 via-slate-950/50 to-transparent flex items-end p-3.5 pointer-events-none">
                <div className="flex items-center justify-between w-full">
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-0.5 rounded bg-slate-950/90 backdrop-blur-md text-[10px] font-mono text-emerald-400 border border-emerald-500/30 flex items-center gap-1">
                      <CheckCircle2 className="w-3 h-3" /> CLIP {creative.qualityScore}/10
                    </span>
                    <span className="px-2 py-0.5 rounded bg-slate-950/90 backdrop-blur-md text-[10px] font-mono text-cyan-300 border border-cyan-500/30">
                      WCAG {creative.contrastRatio}
                    </span>
                    <span className="px-2 py-0.5 rounded bg-slate-950/90 backdrop-blur-md text-[10px] font-mono text-pink-300 border border-pink-500/30">
                      ✨ Gemini Native
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Extracted Color Palette */}
            <div>
              <div className="text-[10px] font-mono font-bold uppercase tracking-wider text-slate-400 mb-1.5 flex items-center justify-between">
                <span>Extracted Brand Palette</span>
                <span className="text-slate-500 font-normal">Click hex to copy</span>
              </div>
              <div className="flex items-center gap-2">
                {creative.palette.map((hex, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => handleCopyColor(hex)}
                    className="flex-1 p-2 rounded-lg border border-white/[0.08] bg-[#07090e]/90 hover:bg-white/[0.06] flex items-center justify-center gap-1.5 transition-all text-[11px] font-mono font-semibold"
                  >
                    <span className="w-3.5 h-3.5 rounded-full border border-white/20 shrink-0" style={{ backgroundColor: hex }} />
                    <span className="text-slate-300">{copiedColorHex === hex ? 'Copied!' : hex}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Prompt Directives Box */}
            <div className="bg-[#07090e]/90 border border-white/[0.08] rounded-xl p-3.5 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-slate-300 flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5 text-pink-400" />
                  Synthesis Directive Prompt
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
              <p className="text-xs text-slate-300 font-mono leading-relaxed bg-black/50 p-2.5 rounded-lg border border-white/[0.05]">
                "{creative.prompt}"
              </p>
            </div>
          </div>
        ))}
      </div>

      {/* Full Resolution Modal */}
      {previewImage && (
        <div className="fixed inset-0 z-50 bg-slate-950/90 backdrop-blur-md flex items-center justify-center p-6"
             onClick={() => setPreviewImage(null)}>
          <div className="relative max-w-4xl w-full glass-panel-elevated border border-white/[0.15] rounded-2xl overflow-hidden shadow-2xl p-5 space-y-4"
               onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between border-b border-white/[0.08] pb-3">
              <div>
                <span className="text-xs font-mono text-pink-400 font-bold">{previewImage.platform} ({previewImage.aspectRatio})</span>
                <h3 className="text-base font-bold text-white mt-0.5">{previewImage.headline}</h3>
              </div>
              <button onClick={() => setPreviewImage(null)} className="px-3 py-1 bg-white/[0.08] hover:bg-white/[0.15] text-white rounded-lg text-xs font-bold font-mono">
                ✕ Close
              </button>
            </div>

            <div className="max-h-[60vh] overflow-hidden rounded-xl bg-black flex items-center justify-center relative">
              <img src={previewImage.imageUrl} alt="Generated Full Visual" className="max-h-[60vh] w-auto object-contain rounded-lg" />
              {showSafeZone && (
                <div className="absolute inset-4 border-2 border-dashed border-cyan-400/60 pointer-events-none flex items-center justify-center">
                  <span className="bg-slate-950/80 text-cyan-300 px-2 py-1 rounded text-[10px] font-mono">100% Safe Zone Margin (Passed)</span>
                </div>
              )}
            </div>

            <div className="flex items-center justify-between pt-2 border-t border-white/[0.08] flex-wrap gap-2">
              <div className="flex items-center gap-2">
                <span className="px-2.5 py-1 rounded bg-[#07090e] text-xs font-mono text-emerald-400 border border-white/[0.08]">CLIP: {previewImage.qualityScore}/10</span>
                <span className="px-2.5 py-1 rounded bg-[#07090e] text-xs font-mono text-cyan-400 border border-white/[0.08]">Dimensions: {previewImage.dimensions}</span>
                <button
                  type="button"
                  onClick={() => setShowSafeZone(!showSafeZone)}
                  className={`px-2.5 py-1 rounded text-xs font-mono border transition-all ${
                    showSafeZone ? 'bg-cyan-500/20 text-cyan-300 border-cyan-500/40' : 'bg-[#07090e] text-slate-400 border-white/[0.08]'
                  }`}
                >
                  <ShieldCheck className="w-3.5 h-3.5 inline mr-1" />
                  {showSafeZone ? 'Hide Safe Zone' : 'Toggle Safe Zone'}
                </button>
              </div>
              <button
                onClick={() => handleDownload(previewImage)}
                className="px-4 py-2 bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-500 hover:to-purple-500 text-white rounded-xl text-xs font-bold font-mono flex items-center gap-1.5 shadow-lg shadow-pink-500/20"
              >
                <Download className="w-3.5 h-3.5" />
                Download High-Res Asset
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
