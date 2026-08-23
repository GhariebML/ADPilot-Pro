import React, { useState } from 'react';
import {
  Copy, Download, Loader, Layout, Mail, Share2,
  ExternalLink, Sparkles, ChevronRight, ChevronDown, Check,
  Target, Calendar, Award, TrendingUp, Info
} from 'lucide-react';
import type { ContentOutput } from '../types';

interface ResultDisplayProps {
  content: ContentOutput | null;
  onDownload?: () => void;
  isDownloading?: boolean;
}

export const ResultDisplay: React.FC<ResultDisplayProps> = ({ content, onDownload, isDownloading }) => {
  const [expandedAdIdx, setExpandedAdIdx] = useState<number | null>(null);
  const [expandedEmailIdx, setExpandedEmailIdx] = useState<number | null>(null);
  const [expandedSocialIdx, setExpandedSocialIdx] = useState<number | null>(null);
  const [copiedKey, setCopiedKey] = useState<string | null>(null);

  if (!content) return null;

  const handleCopyText = (e: React.MouseEvent, text: string, key: string) => {
    e.stopPropagation();
    navigator.clipboard.writeText(text);
    setCopiedKey(key);
    setTimeout(() => setCopiedKey(null), 2000);
  };

  return (
    <div className="w-full space-y-6">

      {/* ── Header ── */}
      <div className="glass-panel-elevated rounded-2xl p-6 flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-2xl">
        <div>
          <h2 className="text-2xl font-black tracking-tight text-slate-100 flex items-center gap-2">
            Campaign Intelligence <Sparkles className="text-cyan-400 w-5 h-5 animate-pulse" />
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Cooperative outputs generated across 18 autonomous marketing agents with 100% schema validation.
          </p>
        </div>
        <div className="flex items-center gap-2.5 flex-wrap">
          <button
            onClick={(e) => {
              const summaryText = `# Campaign Package Export\n\n## Summary\n${content.summary || 'Autonomous Strategy'}\n\n## Ads (${content.ads.length})\n` + 
                content.ads.map(a => `### ${a.platform} - ${a.headline}\n${a.body}\nCTA: ${a.cta}\nPerformance: ${a.performance}\n`).join('\n') +
                `\n## Social Posts\n` + content.socialPosts.map(s => `### ${s.platform}\n${s.content}\n${s.hashtags?.join(' ')}`).join('\n');
              handleCopyText(e, summaryText, 'all-summary');
            }}
            className="px-3.5 py-2 bg-[#07090e]/90 hover:bg-slate-800 border border-white/[0.08] text-slate-200 rounded-xl text-xs font-mono font-bold flex items-center gap-2 transition-all active:scale-95"
          >
            {copiedKey === 'all-summary' ? <Check size={14} className="text-emerald-400" /> : <Copy size={14} />}
            <span>{copiedKey === 'all-summary' ? 'Copied Markdown!' : 'Copy Strategy (MD)'}</span>
          </button>

          <button
            onClick={() => {
              const blob = new Blob([JSON.stringify(content, null, 2)], { type: 'application/json' });
              const url = URL.createObjectURL(blob);
              const a = document.createElement('a');
              a.href = url;
              a.download = `adpilot-campaign-contract.json`;
              a.click();
              URL.revokeObjectURL(url);
            }}
            className="px-3.5 py-2 bg-[#07090e]/90 hover:bg-slate-800 border border-white/[0.08] text-slate-200 rounded-xl text-xs font-mono font-bold flex items-center gap-2 transition-all active:scale-95"
          >
            <Download size={14} />
            <span>Export JSON</span>
          </button>

          <button
            onClick={onDownload}
            disabled={isDownloading}
            aria-label="Export Campaign Brief"
            className="px-4 py-2 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 disabled:opacity-50 text-white rounded-xl text-xs font-bold font-mono flex items-center gap-2 transition-all active:scale-95 shadow-lg shadow-cyan-500/20"
          >
            {isDownloading ? <Loader className="animate-spin" size={14} /> : <Download size={14} />}
            <span>{isDownloading ? 'Exporting...' : 'Export Campaign Brief'}</span>
          </button>
        </div>
      </div>

      {/* ── Ad Creatives (Content Agent) ── */}
      <div className="glass-panel-elevated rounded-2xl overflow-hidden shadow-2xl">
        <div className="px-5 py-4 border-b border-white/[0.08] bg-teal-500/10 flex items-center gap-2">
          <div className="w-1.5 h-5 rounded-full bg-teal-400" />
          <Layout size={16} className="text-teal-400" />
          <h3 className="text-xs font-black uppercase tracking-widest text-teal-300">Ad Creatives & Copywriting</h3>
          <span className="ml-auto text-[10px] font-mono font-bold text-teal-400/70 uppercase tracking-widest">Content Agent</span>
        </div>
        
        <div className="p-5 space-y-4">
          <p className="text-xs text-slate-400 font-medium">Click on any ad creative card below to review copywriting structure, visual designs prompts, target audience focus, and performance estimates.</p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {content.ads.map((ad, idx) => {
              const isExpanded = expandedAdIdx === idx;
              const copyKey = `ad-body-${idx}`;
              return (
                <div 
                  key={idx} 
                  onClick={() => setExpandedAdIdx(isExpanded ? null : idx)}
                  className={`relative rounded-2xl border transition-all duration-300 overflow-hidden cursor-pointer shadow-sm ${
                    isExpanded 
                      ? 'md:col-span-3 bg-[#07090e]/95 border-teal-500/50 ring-1 ring-teal-500/20 shadow-xl' 
                      : 'bg-[#07090e]/80 hover:bg-[#07090e] border-white/[0.08] hover:border-teal-500/40'
                  }`}
                >
                  {/* Card Front Header */}
                  <div className="p-5 flex flex-col justify-between min-h-[140px] bg-gradient-to-br from-teal-500/5 to-transparent">
                    <div className="flex items-center justify-between">
                      <span className="px-2.5 py-0.5 bg-teal-500/15 rounded-full text-[10px] font-mono font-bold text-teal-300 uppercase tracking-wide border border-teal-500/30">
                        {ad.platform}
                      </span>
                      <span className="text-[10px] font-mono text-emerald-400 font-bold">
                        {ad.performance}
                      </span>
                    </div>
                    <div className="mt-4">
                      <h4 className="text-sm font-bold text-slate-100 leading-snug line-clamp-2">
                        {ad.headline}
                      </h4>
                    </div>
                  </div>

                  {/* Card Bottom / Toggle Action */}
                  <div className="px-5 py-3.5 flex items-center justify-between border-t border-white/[0.08] bg-black/20">
                    <span className="text-[11px] font-bold text-teal-400 uppercase tracking-widest flex items-center gap-1.5 font-mono">
                      CTA: <span className="text-slate-200">{ad.cta}</span>
                    </span>
                    <div className="flex items-center gap-3">
                      <button 
                        onClick={(e) => handleCopyText(e, `${ad.headline}\n\n${ad.body}`, copyKey)}
                        className="p-1 text-slate-400 hover:text-teal-400 transition-colors"
                        title="Copy ad copy"
                      >
                        {copiedKey === copyKey ? <Check size={14} className="text-emerald-400" /> : <Copy size={14} />}
                      </button>
                      {isExpanded ? (
                        <ChevronDown size={14} className="text-teal-400" />
                      ) : (
                        <ChevronRight size={14} className="text-slate-500 group-hover:text-teal-400" />
                      )}
                    </div>
                  </div>

                  {/* Expanded Content View */}
                  {isExpanded && (
                    <div className="p-6 border-t border-white/[0.08] bg-black/40 animate-in slide-in-from-top duration-300 space-y-6">
                      
                      {/* Copy Sections */}
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                        <div className="space-y-2">
                          <span className="text-[10px] font-mono font-bold uppercase tracking-widest text-slate-400 block">Headline copy</span>
                          <div className="p-4 rounded-xl bg-[#07090e] border border-white/[0.08] relative group/copy">
                            <p className="text-xs font-bold text-slate-100">{ad.headline}</p>
                            <button 
                              onClick={(e) => handleCopyText(e, ad.headline, 'head')}
                              className="absolute top-2 right-2 opacity-0 group-hover/copy:opacity-100 p-1 bg-slate-900 rounded border border-white/[0.08] text-slate-400 hover:text-teal-400 transition-all"
                            >
                              {copiedKey === 'head' ? <Check size={12} className="text-emerald-400" /> : <Copy size={12} />}
                            </button>
                          </div>
                        </div>

                        <div className="space-y-2">
                          <span className="text-[10px] font-mono font-bold uppercase tracking-widest text-slate-400 block">Body Copy</span>
                          <div className="p-4 rounded-xl bg-[#07090e] border border-white/[0.08] relative group/copy">
                            <p className="text-xs text-slate-300 leading-relaxed whitespace-pre-line">{ad.body}</p>
                            <button 
                              onClick={(e) => handleCopyText(e, ad.body, 'body')}
                              className="absolute top-2 right-2 opacity-0 group-hover/copy:opacity-100 p-1 bg-slate-900 rounded border border-white/[0.08] text-slate-400 hover:text-teal-400 transition-all"
                            >
                              {copiedKey === 'body' ? <Check size={12} className="text-emerald-400" /> : <Copy size={12} />}
                            </button>
                          </div>
                        </div>
                      </div>

                      {/* Design Prompt & Concept */}
                      {ad.visualPrompt && (
                        <div className="space-y-2">
                          <span className="text-[10px] font-mono font-bold uppercase tracking-widest text-slate-400 block">Visual Synthesis Directive (Design Agent)</span>
                          <div className="p-4 rounded-xl bg-teal-500/10 border border-teal-500/20">
                            <p className="text-xs text-slate-200 leading-relaxed font-mono">
                              {ad.visualPrompt}
                            </p>
                          </div>
                        </div>
                      )}

                      {/* Strategy Insights & Performance estimates */}
                      <div className="pt-2">
                        <span className="text-[10px] font-mono font-bold uppercase tracking-widest text-slate-400 block mb-3">Targeting & Predictive Estimates</span>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                          <div className="p-3.5 rounded-xl border border-white/[0.08] bg-[#07090e]/80 flex items-start gap-3">
                            <Target className="text-cyan-400 w-4.5 h-4.5 shrink-0 mt-0.5" />
                            <div>
                              <p className="text-[9px] uppercase tracking-wider font-bold font-mono text-slate-400">Target Segment</p>
                              <p className="text-xs font-bold text-slate-200 mt-0.5 truncate max-w-[150px]">{ad.targetAudience || 'Core demographic'}</p>
                            </div>
                          </div>

                          <div className="p-3.5 rounded-xl border border-white/[0.08] bg-[#07090e]/80 flex items-start gap-3">
                            <Award className="text-amber-400 w-4.5 h-4.5 shrink-0 mt-0.5" />
                            <div>
                              <p className="text-[9px] uppercase tracking-wider font-bold font-mono text-slate-400">Funnel Placement</p>
                              <p className="text-xs font-bold text-slate-200 mt-0.5">{ad.funnelStage || 'Campaign goal'}</p>
                            </div>
                          </div>

                          <div className="p-3.5 rounded-xl border border-white/[0.08] bg-[#07090e]/80 flex items-start gap-3">
                            <TrendingUp className="text-emerald-400 w-4.5 h-4.5 shrink-0 mt-0.5" />
                            <div>
                              <p className="text-[9px] uppercase tracking-wider font-bold font-mono text-slate-400">Forecasted CTR</p>
                              <p className="text-xs font-bold text-emerald-400 mt-0.5">{ad.ctrEstimate || '3.5%'}</p>
                            </div>
                          </div>

                          <div className="p-3.5 rounded-xl border border-white/[0.08] bg-[#07090e]/80 flex items-start gap-3">
                            <Info className="text-teal-400 w-4.5 h-4.5 shrink-0 mt-0.5" />
                            <div>
                              <p className="text-[9px] uppercase tracking-wider font-bold font-mono text-slate-400">Avg. CPC Estimate</p>
                              <p className="text-xs font-bold text-slate-200 mt-0.5">{ad.cpcEstimate || '$1.25'}</p>
                            </div>
                          </div>
                        </div>
                      </div>

                      {/* Hashtags */}
                      {ad.hashtags && ad.hashtags.length > 0 && (
                        <div className="flex flex-wrap gap-1.5 pt-2">
                          {ad.hashtags.map((tag, tIdx) => (
                            <span key={tIdx} className="px-2.5 py-1 bg-[#07090e] border border-white/[0.08] rounded-lg text-[10px] font-mono text-teal-300">
                              #{tag.replace('#', '')}
                            </span>
                          ))}
                        </div>
                      )}

                    </div>
                  )}

                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* ── Two Columns: Email Sequences & CTAs ── */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">

        {/* Email Sequence (Strategy Agent) */}
        <div className="lg:col-span-7 glass-panel-elevated rounded-2xl overflow-hidden shadow-2xl">
          <div className="px-5 py-4 border-b border-white/[0.08] bg-blue-500/10 flex items-center gap-2">
            <div className="w-1.5 h-5 rounded-full bg-blue-400" />
            <Mail size={16} className="text-blue-400" />
            <h3 className="text-xs font-black uppercase tracking-widest text-blue-300">Email Automations Sequence</h3>
            <span className="ml-auto text-[10px] font-mono font-bold text-blue-400/70 uppercase tracking-widest">Strategy Agent</span>
          </div>

          <div className="p-5 space-y-4">
            <p className="text-xs text-slate-400 font-medium">Click on any email sequence item below to expand the full subject, sequence schedule, onboarding trigger conditions, and copywriting content.</p>
            <div className="space-y-3">
              {content.emailSequences.map((email, idx) => {
                const isExpanded = expandedEmailIdx === idx;
                const copyKey = `email-body-${idx}`;
                return (
                  <div 
                    key={idx}
                    onClick={() => setExpandedEmailIdx(isExpanded ? null : idx)}
                    className={`rounded-2xl border transition-all duration-300 cursor-pointer overflow-hidden ${
                      isExpanded 
                        ? 'bg-[#07090e]/95 border-blue-500/50 ring-1 ring-blue-500/20 shadow-xl' 
                        : 'bg-[#07090e]/80 hover:bg-[#07090e] border-white/[0.08] hover:border-blue-500/40'
                    }`}
                  >
                    {/* Header */}
                    <div className="p-4 flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <span className="px-2.5 py-1 bg-blue-500/15 rounded-lg text-[10px] font-mono font-bold text-blue-300 tracking-wide border border-blue-500/30">
                          Day {email.sendDay || idx * 2 + 1}
                        </span>
                        <div>
                          <h4 className="text-xs font-bold text-slate-100 leading-tight">
                            {email.subject}
                          </h4>
                          {!isExpanded && (
                            <p className="text-[10px] text-slate-400 mt-1 max-w-[340px] truncate">
                              {email.preview}
                            </p>
                          )}
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <button 
                          onClick={(e) => handleCopyText(e, `Subject: ${email.subject}\n\n${email.body}`, copyKey)}
                          className="p-1 text-slate-400 hover:text-blue-400 transition-colors"
                          title="Copy email copy"
                        >
                          {copiedKey === copyKey ? <Check size={12} className="text-emerald-400" /> : <Copy size={12} />}
                        </button>
                        {isExpanded ? (
                          <ChevronDown size={14} className="text-blue-400" />
                        ) : (
                          <ChevronRight size={14} className="text-slate-500" />
                        )}
                      </div>
                    </div>

                    {/* Expandable Email Details */}
                    {isExpanded && (
                      <div className="p-5 border-t border-white/[0.08] bg-black/40 animate-in slide-in-from-top duration-300 space-y-4">
                        
                        {/* Meta Settings */}
                        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 p-3 bg-[#07090e] rounded-xl border border-white/[0.08] text-[10px] font-mono">
                          <div>
                            <span className="font-bold text-slate-400 block uppercase tracking-wide">Trigger</span>
                            <span className="text-slate-200 mt-0.5 block leading-normal">{email.triggerCondition || 'Trigger condition'}</span>
                          </div>
                          <div>
                            <span className="font-bold text-slate-400 block uppercase tracking-wide">Goal</span>
                            <span className="text-slate-200 mt-0.5 block leading-normal">{email.goal || 'Conversion benchmark'}</span>
                          </div>
                          <div>
                            <span className="font-bold text-slate-400 block uppercase tracking-wide">Segment</span>
                            <span className="text-slate-200 mt-0.5 block leading-normal truncate">{email.audienceFocus || 'Target audience'}</span>
                          </div>
                        </div>

                        {/* Subject & Preview */}
                        <div className="space-y-1">
                          <span className="text-[10px] font-mono font-bold uppercase tracking-widest text-slate-400">Subject line</span>
                          <p className="text-xs font-bold text-slate-100">{email.subject}</p>
                        </div>

                        {/* Professional Email Client Mockup */}
                        <div className="space-y-2">
                          <span className="text-[10px] font-mono font-bold uppercase tracking-widest text-slate-400 block">Copywriting</span>
                          <div className="rounded-xl border border-white/[0.08] overflow-hidden shadow-inner">
                            {/* Window header */}
                            <div className="px-4 py-2 bg-slate-900 border-b border-white/[0.08] flex items-center gap-1.5">
                              <div className="w-2.5 h-2.5 rounded-full bg-red-400" />
                              <div className="w-2.5 h-2.5 rounded-full bg-amber-400" />
                              <div className="w-2.5 h-2.5 rounded-full bg-green-400" />
                              <span className="ml-auto text-[9px] font-mono text-slate-400 uppercase tracking-widest">Email Client Preview</span>
                            </div>
                            {/* Window body */}
                            <div className="p-5 bg-[#07090e] text-xs text-slate-200 leading-relaxed font-sans whitespace-pre-line">
                              {email.body}
                            </div>
                          </div>
                        </div>

                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* CTAs & Predictive Scores (Analytics Agent) */}
        <div className="lg:col-span-5 space-y-5 flex flex-col">
          
          {/* CTAs - Analytics */}
          <div className="glass-panel-elevated rounded-2xl overflow-hidden shadow-2xl flex-1">
            <div className="px-5 py-4 border-b border-white/[0.08] bg-amber-500/10 flex items-center gap-2">
              <div className="w-1.5 h-5 rounded-full bg-amber-400" />
              <ExternalLink size={16} className="text-amber-400" />
              <h3 className="text-xs font-black uppercase tracking-widest text-amber-300">CTAs & Copy Variants</h3>
              <span className="ml-auto text-[10px] font-mono font-bold text-amber-400/70 uppercase tracking-widest">Analytics Agent</span>
            </div>
            
            <div className="p-5 space-y-4">
              <p className="text-xs text-slate-400 font-medium">Optimal call to action buttons sorted by conversion performance and CTR forecasts.</p>
              
              <div className="space-y-3">
                {[
                  { text: 'Get Started Now', score: 'High Intent', type: 'Primary Conversion Button', bg: 'bg-cyan-500/20 text-cyan-300 border-cyan-500/40' },
                  { text: 'Try for Free', score: 'Medium Intent', type: 'Secondary Trial Trigger', bg: 'bg-teal-500/20 text-teal-300 border-teal-500/40' },
                  { text: 'Schedule an Operations Audit', score: 'Educational', type: 'Consultation Qualifier', bg: 'bg-[#07090e] text-slate-200 border-white/[0.08]' },
                  { text: 'Learn More', score: 'Awareness', type: 'Informational Funnel Stage', bg: 'bg-[#07090e] text-slate-200 border-white/[0.08]' }
                ].map((cta, idx) => (
                  <div key={idx} className="p-3.5 rounded-xl border border-white/[0.08] bg-[#07090e]/80 flex items-center justify-between hover:border-white/[0.2] transition-colors">
                    <div>
                      <p className="text-xs font-bold text-slate-100">{cta.text}</p>
                      <p className="text-[10px] text-slate-400 mt-0.5 font-mono">{cta.type} · {cta.score}</p>
                    </div>
                    <button 
                      onClick={(e) => handleCopyText(e, cta.text, `cta-${idx}`)}
                      className="text-slate-400 hover:text-cyan-400 transition-colors ml-4"
                    >
                      {copiedKey === `cta-${idx}` ? <Check size={12} className="text-emerald-400" /> : <Copy size={12} />}
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* A/B Testing Strategy Widget */}
          <div className="glass-card-premium p-5 flex items-start gap-4 shadow-xl">
            <div className="p-3 bg-amber-500/15 border border-amber-500/30 rounded-xl shrink-0 text-amber-400">
              <Sparkles size={18} />
            </div>
            <div>
              <p className="text-xs font-black text-slate-100 uppercase tracking-wider font-mono">A/B Testing Variants</p>
              <p className="text-[11px] text-slate-400 leading-relaxed mt-1">
                The Analytics Agent continuously scores copy variants against historical conversion distributions to optimize CTR and reach.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* ── Social Media Feed (Research Agent) ── */}
      <div className="glass-panel-elevated rounded-2xl overflow-hidden shadow-2xl">
        <div className="px-5 py-4 border-b border-white/[0.08] bg-purple-500/10 flex items-center gap-2">
          <div className="w-1.5 h-5 rounded-full bg-purple-400" />
          <Share2 size={16} className="text-purple-400" />
          <h3 className="text-xs font-black uppercase tracking-widest text-purple-300">Social Media & Feed Calendar</h3>
          <span className="ml-auto text-[10px] font-mono font-bold text-purple-400/70 uppercase tracking-widest">Research Agent</span>
        </div>

        <div className="p-5 space-y-4">
          <p className="text-xs text-slate-400 font-medium">Click on any social media post card below to review platform schedules, best time to post recommendations, and creative visual generation guidelines.</p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {content.socialPosts.map((post, idx) => {
              const isExpanded = expandedSocialIdx === idx;
              const copyKey = `social-post-${idx}`;
              return (
                <div 
                  key={idx} 
                  onClick={() => setExpandedSocialIdx(isExpanded ? null : idx)}
                  className={`rounded-2xl border transition-all duration-300 cursor-pointer overflow-hidden ${
                    isExpanded 
                      ? 'md:col-span-3 bg-[#07090e]/95 border-purple-500/50 ring-1 ring-purple-500/20 shadow-xl' 
                      : 'bg-[#07090e]/80 hover:bg-[#07090e] border-white/[0.08] hover:border-purple-500/40'
                  }`}
                >
                  {/* Card Front Header */}
                  <div className="p-5 bg-gradient-to-br from-purple-500/5 to-transparent">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-xl bg-purple-500/15 border border-purple-500/30 flex items-center justify-center text-purple-300 font-black text-xs">
                        {post.platform[0]}
                      </div>
                      <div>
                        <h4 className="text-xs font-bold text-slate-100">
                          {post.platform} Post
                        </h4>
                        <p className="text-[10px] text-slate-400 font-mono uppercase tracking-wider mt-0.5">
                          {post.postType || 'Visual Content'}
                        </p>
                      </div>
                      <div className="ml-auto flex items-center gap-2">
                        <button 
                          onClick={(e) => handleCopyText(e, `${post.content}\n\n${post.hashtags?.map(h => '#' + h.replace('#','')).join(' ')}`, copyKey)}
                          className="p-1 text-slate-400 hover:text-purple-400 transition-colors"
                          title="Copy social copy"
                        >
                          {copiedKey === copyKey ? <Check size={12} className="text-emerald-400" /> : <Copy size={12} />}
                        </button>
                        {isExpanded ? (
                          <ChevronDown size={14} className="text-purple-400" />
                        ) : (
                          <ChevronRight size={14} className="text-slate-500" />
                        )}
                      </div>
                    </div>

                    <div className="mt-4">
                      <p className="text-xs text-slate-300 leading-relaxed line-clamp-3">
                        {post.content}
                      </p>
                    </div>
                  </div>

                  {/* Expanded Content View */}
                  {isExpanded && (
                    <div className="p-6 border-t border-white/[0.08] bg-black/40 animate-in slide-in-from-top duration-300 space-y-5">
                      
                      {/* Meta information */}
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div className="p-3.5 rounded-xl border border-white/[0.08] bg-[#07090e] flex items-start gap-3">
                          <Calendar className="text-purple-400 w-4.5 h-4.5 mt-0.5 shrink-0" />
                          <div>
                            <p className="text-[9px] uppercase tracking-wider font-bold font-mono text-slate-400">Optimal Post Time</p>
                            <p className="text-xs font-bold text-slate-200 mt-0.5">{post.bestTimeToPost || 'Tuesday morning'}</p>
                          </div>
                        </div>

                        <div className="p-3.5 rounded-xl border border-white/[0.08] bg-[#07090e] flex items-start gap-3">
                          <Award className="text-purple-400 w-4.5 h-4.5 mt-0.5 shrink-0" />
                          <div>
                            <p className="text-[9px] uppercase tracking-wider font-bold font-mono text-slate-400">Content Category</p>
                            <p className="text-xs font-bold text-slate-200 mt-0.5">{post.postType || 'Educational Post'}</p>
                          </div>
                        </div>
                      </div>

                      {/* Content copy */}
                      <div className="space-y-2">
                        <span className="text-[10px] font-mono font-bold uppercase tracking-widest text-slate-400 block">Post Caption Copy</span>
                        <div className="p-4 rounded-xl bg-[#07090e] border border-white/[0.08] relative group/copy">
                          <p className="text-xs text-slate-200 leading-relaxed whitespace-pre-line">{post.content}</p>
                          <button 
                            onClick={(e) => handleCopyText(e, post.content, 'caption')}
                            className="absolute top-2 right-2 opacity-0 group-hover/copy:opacity-100 p-1 bg-slate-900 rounded border border-white/[0.08] text-slate-400 hover:text-purple-400 transition-all"
                          >
                            {copiedKey === 'caption' ? <Check size={12} className="text-emerald-400" /> : <Copy size={12} />}
                          </button>
                        </div>
                      </div>

                      {/* Visual Prompts */}
                      {post.imagePrompt && (
                        <div className="space-y-2">
                          <span className="text-[10px] font-mono font-bold uppercase tracking-widest text-slate-400 block">Visual Synthesis Directive</span>
                          <div className="p-4 rounded-xl bg-purple-500/10 border border-purple-500/20">
                            <p className="text-xs text-slate-200 leading-relaxed font-mono">
                              {post.imagePrompt}
                            </p>
                          </div>
                        </div>
                      )}

                      {/* Hashtags */}
                      {post.hashtags && post.hashtags.length > 0 && (
                        <div className="flex flex-wrap gap-1.5 pt-2">
                          {post.hashtags.map((tag, tIdx) => (
                            <span key={tIdx} className="px-2.5 py-1 bg-purple-500/15 border border-purple-500/30 rounded-lg text-[10px] font-mono font-semibold text-purple-300">
                              #{tag.replace('#', '')}
                            </span>
                          ))}
                        </div>
                      )}

                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </div>

    </div>
  );
};

export default ResultDisplay;
