import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import type { CampaignBrief } from '../types';
import { campaignService } from '../services/api';
import { Sparkles, Rocket, AlertCircle, RefreshCw, Building2, ShoppingBag, Home, Briefcase, Zap, CheckCircle2, TrendingUp } from 'lucide-react';

interface CampaignBriefFormProps {
  onSubmit: (taskId: string) => void;
  isLoading?: boolean;
}

interface VerticalPreset {
  id: string;
  name: string;
  category: string;
  icon: React.ComponentType<{ className?: string }>;
  data: CampaignBrief;
}

const VERTICAL_PRESETS: VerticalPreset[] = [
  {
    id: 'saas',
    name: 'VisionGuard AI',
    category: 'B2B Enterprise SaaS',
    icon: Building2,
    data: {
      businessName: 'VisionGuard AI',
      productName: 'Autonomous Security Analytics',
      productDescription: 'Enterprise AI video analytics and edge computing platform for corporate security and automated compliance monitoring.',
      targetAudience: 'CISOs, VP of IT Security, Enterprise Operations Directors at Fortune 500 companies.',
      goals: ['lead_generation', 'brand_awareness'],
      budget: 10000,
      duration: '30-days',
      tone: 'professional',
    },
  },
  {
    id: 'd2c',
    name: 'AeroPulse ANC',
    category: 'D2C Consumer Tech',
    icon: ShoppingBag,
    data: {
      businessName: 'AeroPulse Audio',
      productName: 'AeroPulse Pro ANC Earbuds',
      productDescription: 'Audiophile-grade wireless active noise-cancelling earbuds with 48-hour battery life and spatial audio calibration.',
      targetAudience: 'Tech commuters, audio enthusiasts, gym goers, and hybrid remote professionals aged 22-40.',
      goals: ['sales_conversion', 'lead_generation'],
      budget: 5000,
      duration: '14-days',
      tone: 'bold',
    },
  },
  {
    id: 'realestate',
    name: 'Skyline Luxury',
    category: 'Ultra-Luxury Real Estate',
    icon: Home,
    data: {
      businessName: 'Skyline Residences',
      productName: 'The Penthouse Collection',
      productDescription: 'Panoramic glass penthouses with private infinity pools, smart home automation, and private helipad access in prime downtown.',
      targetAudience: 'High-net-worth individuals, tech executives, global luxury investors, and family offices.',
      goals: ['lead_generation', 'sales_conversion'],
      budget: 25000,
      duration: '60-days',
      tone: 'premium',
    },
  },
  {
    id: 'services',
    name: 'Apex Consulting',
    category: 'Cloud Engineering',
    icon: Briefcase,
    data: {
      businessName: 'Apex Cloud Systems',
      productName: 'Enterprise Cloud Modernization',
      productDescription: 'Turnkey cloud migration, Kubernetes microservices architecture, and automated FinOps cost optimization services.',
      targetAudience: 'CTOs, Engineering Directors, and Head of Infrastructure managing legacy on-prem workloads.',
      goals: ['lead_generation'],
      budget: 7500,
      duration: '30-days',
      tone: 'professional',
    },
  },
];

export const CampaignBriefForm: React.FC<CampaignBriefFormProps> = ({ onSubmit, isLoading = false }) => {
  const { register, handleSubmit, setValue, watch, formState: { errors } } = useForm<CampaignBrief>({
    defaultValues: {
      businessName: '',
      productName: '',
      productDescription: '',
      targetAudience: '',
      goals: ['lead_generation', 'sales_conversion'],
      budget: 10000,
      duration: '30-days',
      tone: 'professional',
    },
  });

  const [submitError, setSubmitError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [activePreset, setActivePreset] = useState<string | null>(null);

  // Watch form fields to compute live quality score & reach estimation
  const watchedBusiness = watch('businessName');
  const watchedProduct = watch('productName');
  const watchedDesc = watch('productDescription');
  const watchedAudience = watch('targetAudience');
  const watchedBudget = watch('budget') || 10000;
  const selectedTone = watch('tone');
  const selectedGoals = watch('goals') || [];

  // Compute Brief Quality & Completeness Score (0 - 100%)
  const computeQualityScore = (): number => {
    let score = 0;
    if (watchedBusiness && watchedBusiness.length >= 3) score += 20;
    if (watchedProduct && watchedProduct.length >= 3) score += 20;
    if (watchedDesc && watchedDesc.length >= 25) score += 25;
    if (watchedAudience && watchedAudience.length >= 15) score += 20;
    if (watchedBudget && watchedBudget >= 500) score += 15;
    return Math.min(100, score);
  };

  const qualityScore = computeQualityScore();

  // Dynamic estimate calculations
  const estimatedImpressions = Math.round(watchedBudget * 14.5).toLocaleString();
  const estimatedClicks = Math.round(watchedBudget * 0.42).toLocaleString();

  const handleGoalToggle = (goal: string) => {
    const current = selectedGoals;
    if (current.includes(goal)) {
      setValue('goals', current.filter((g) => g !== goal));
    } else {
      setValue('goals', [...current, goal]);
    }
  };

  const applyPreset = (preset: VerticalPreset) => {
    setActivePreset(preset.id);
    setValue('businessName', preset.data.businessName);
    setValue('productName', preset.data.productName);
    setValue('productDescription', preset.data.productDescription);
    setValue('targetAudience', preset.data.targetAudience);
    setValue('goals', preset.data.goals);
    setValue('budget', preset.data.budget);
    setValue('duration', preset.data.duration);
    setValue('tone', preset.data.tone);
    setSubmitError(null);
  };

  const handleFormSubmit = async (data: CampaignBrief) => {
    setIsSubmitting(true);
    setSubmitError(null);
    try {
      if (!data.goals || data.goals.length === 0) {
        data.goals = ['lead_generation'];
      }
      const response = await campaignService.submitCampaign(data);
      onSubmit(response.taskId);
    } catch (error) {
      setSubmitError(error instanceof Error ? error.message : 'Failed to submit campaign');
    } finally {
      setIsSubmitting(false);
    }
  };

  const labelClass = 'block text-[11px] font-mono font-bold text-slate-300 uppercase tracking-wider mb-1.5';
  const inputClass = 'w-full bg-[#07090e]/90 border border-white/[0.1] shadow-inner rounded-xl px-3.5 py-2.5 text-xs text-slate-100 placeholder:text-slate-500 focus:ring-1 focus:ring-cyan-400 focus:border-cyan-400 outline-none transition-all font-sans';

  return (
    <div className="w-full space-y-6">
      {/* Top Presets Banner */}
      <div className="glass-panel-elevated rounded-2xl p-4 space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-cyan-400" />
            <span className="text-xs font-bold text-slate-100 uppercase tracking-wider font-mono">1-Click Vertical Presets</span>
          </div>
          <span className="text-[11px] text-cyan-300 font-mono font-semibold">Load calibrated parameters</span>
        </div>

        <div className="grid grid-cols-2 gap-2.5">
          {VERTICAL_PRESETS.map((preset) => {
            const Icon = preset.icon;
            const isSelected = activePreset === preset.id;
            return (
              <button
                key={preset.id}
                type="button"
                onClick={() => applyPreset(preset)}
                className={`p-3 rounded-xl border text-left transition-all relative group flex flex-col justify-between ${
                  isSelected
                    ? 'bg-gradient-to-r from-cyan-500/20 to-blue-500/20 border-cyan-400 text-cyan-200 shadow-md shadow-cyan-500/15'
                    : 'bg-[#07090e]/80 border-white/[0.08] hover:border-white/[0.2] hover:bg-white/[0.04] text-slate-300'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className={`p-1.5 rounded-lg ${isSelected ? 'bg-cyan-500/20 text-cyan-300' : 'bg-white/[0.05] text-slate-400 group-hover:text-slate-200'}`}>
                    <Icon className="w-4 h-4" />
                  </div>
                  {isSelected && <CheckCircle2 className="w-4 h-4 text-cyan-400" />}
                </div>
                <div>
                  <div className="text-xs font-bold leading-tight text-white">{preset.name}</div>
                  <div className="text-[10px] text-slate-400 font-mono mt-0.5 leading-tight">{preset.category}</div>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Brief Completeness & Reach Estimates */}
      <div className="glass-panel-elevated rounded-xl p-4 space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500/25 to-blue-500/25 border border-cyan-500/40 flex items-center justify-center text-cyan-300 text-xs font-mono font-bold shadow-md shadow-cyan-500/10">
              {qualityScore}%
            </div>
            <div>
              <div className="text-xs font-bold text-slate-100">Brief Completeness Score</div>
              <div className="text-[10px] text-slate-400 font-mono">
                {qualityScore >= 80 ? 'Target: Optimized for 18-agent fleet' : 'Add more detail for higher synthesis precision'}
              </div>
            </div>
          </div>

          <div className="w-32 bg-slate-900 h-2.5 rounded-full overflow-hidden border border-white/[0.08] p-0.5">
            <div
              className={`h-full transition-all duration-500 rounded-full ${
                qualityScore >= 80 ? 'bg-gradient-to-r from-cyan-400 to-emerald-400' : 'bg-gradient-to-r from-amber-400 to-cyan-400'
              }`}
              style={{ width: `${qualityScore}%` }}
            />
          </div>
        </div>

        {/* Dynamic Reach Pill Bar */}
        <div className="grid grid-cols-2 gap-2 pt-2 border-t border-white/[0.08] text-[11px] font-mono">
          <div className="flex items-center justify-between px-2.5 py-1.5 rounded-lg bg-[#07090e]/80 border border-white/[0.06]">
            <span className="text-slate-400">Est. Impressions:</span>
            <span className="text-cyan-300 font-bold">~{estimatedImpressions}</span>
          </div>
          <div className="flex items-center justify-between px-2.5 py-1.5 rounded-lg bg-[#07090e]/80 border border-white/[0.06]">
            <span className="text-slate-400">Est. Clicks:</span>
            <span className="text-emerald-300 font-bold">~{estimatedClicks}</span>
          </div>
        </div>
      </div>

      {submitError && (
        <div className="p-3.5 bg-rose-500/15 border border-rose-500/40 rounded-xl text-rose-300 text-xs flex items-start gap-2.5 shadow-lg shadow-rose-500/10">
          <AlertCircle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
          <div className="flex-1">
            <p className="font-semibold">{submitError}</p>
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-4">
        {/* Row 1: Business & Product */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className={labelClass}>Company / Brand Name *</label>
            <input
              type="text"
              {...register('businessName', { required: 'Business name is required' })}
              className={inputClass}
              placeholder="e.g. VisionGuard AI"
            />
            {errors.businessName && <span className="text-[10px] text-rose-400 mt-1 block font-mono">{errors.businessName.message}</span>}
          </div>

          <div>
            <label className={labelClass}>Product / Offering *</label>
            <input
              type="text"
              {...register('productName', { required: 'Product name is required' })}
              className={inputClass}
              placeholder="e.g. Enterprise Security Platform"
            />
            {errors.productName && <span className="text-[10px] text-rose-400 mt-1 block font-mono">{errors.productName.message}</span>}
          </div>
        </div>

        {/* Product Description */}
        <div>
          <label className={labelClass}>Value Proposition & Product Details *</label>
          <textarea
            rows={3}
            {...register('productDescription', { required: 'Product description is required' })}
            className={`${inputClass} resize-none`}
            placeholder="Describe key features, primary differentiators, and value proposition..."
          />
          {errors.productDescription && <span className="text-[10px] text-rose-400 mt-1 block font-mono">{errors.productDescription.message}</span>}
        </div>

        {/* Target Audience */}
        <div>
          <label className={labelClass}>Target Audience (Ideal Customer Profile) *</label>
          <input
            type="text"
            {...register('targetAudience', { required: 'Target audience is required' })}
            className={inputClass}
            placeholder="e.g. CISOs, VP of IT Security, Enterprise Operations Directors"
          />
          {errors.targetAudience && <span className="text-[10px] text-rose-400 mt-1 block font-mono">{errors.targetAudience.message}</span>}
        </div>

        {/* Row 2: Goals, Budget & Duration */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className={labelClass}>Campaign Budget ($ USD)</label>
            <input
              type="number"
              {...register('budget', { valueAsNumber: true, min: { value: 100, message: 'Minimum budget is $100' } })}
              className={inputClass}
              placeholder="10000"
            />
          </div>

          <div>
            <label className={labelClass}>Campaign Duration</label>
            <select {...register('duration')} className={inputClass}>
              <option value="7-days">7 Days (Sprint Launch)</option>
              <option value="14-days">14 Days (Standard Test)</option>
              <option value="30-days">30 Days (Growth Campaign)</option>
              <option value="60-days">60 Days (Quarterly Scale)</option>
            </select>
          </div>

          <div>
            <label className={labelClass}>Brand Voice Tone</label>
            <select {...register('tone')} className={inputClass}>
              <option value="professional">Professional & Authoritative</option>
              <option value="bold">Bold & Disruptive</option>
              <option value="conversational">Conversational & Friendly</option>
              <option value="premium">Ultra-Luxury & Exclusive</option>
              <option value="technical">Technical & Data-Driven</option>
            </select>
          </div>
        </div>

        {/* Campaign Goals Multi-Select Chips */}
        <div>
          <label className={labelClass}>Optimization Goals</label>
          <div className="flex flex-wrap gap-2">
            {[
              { id: 'lead_generation', label: '🎯 Lead Generation' },
              { id: 'sales_conversion', label: '⚡ Direct Sales / ROAS' },
              { id: 'brand_awareness', label: '🚀 Brand Awareness' },
              { id: 'retargeting', label: '🔄 BOFU Retargeting' },
            ].map((goal) => {
              const isChecked = selectedGoals.includes(goal.id);
              return (
                <button
                  key={goal.id}
                  type="button"
                  onClick={() => handleGoalToggle(goal.id)}
                  className={`px-3 py-1.5 rounded-xl text-xs font-semibold border transition-all duration-200 ${
                    isChecked
                      ? 'bg-gradient-to-r from-cyan-500/25 to-blue-500/25 border-cyan-400 text-cyan-300 shadow-sm shadow-cyan-500/20'
                      : 'bg-[#07090e]/80 border-white/[0.08] text-slate-400 hover:text-slate-200 hover:border-white/[0.2]'
                  }`}
                >
                  {goal.label}
                </button>
              );
            })}
          </div>
        </div>

        {/* Submit Action Button */}
        <div className="pt-2">
          <button
            type="submit"
            disabled={isSubmitting || isLoading}
            className="w-full py-3.5 px-4 rounded-xl font-bold text-xs uppercase tracking-wider bg-gradient-to-r from-cyan-500 via-blue-600 to-indigo-600 hover:from-cyan-400 hover:via-blue-500 hover:to-indigo-500 text-white shadow-xl shadow-cyan-500/25 active:scale-[0.99] transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
          >
            {isSubmitting || isLoading ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin text-white" />
                <span>Orchestrating 18 AI Agents...</span>
              </>
            ) : (
              <>
                <Rocket className="w-4 h-4 text-white" />
                <span>Launch 18-Stage Autonomous Pipeline</span>
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};
