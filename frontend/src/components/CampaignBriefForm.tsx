import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import type { CampaignBrief } from '../types';
import { campaignService } from '../services/api';
import { Sparkles, Rocket, AlertCircle, RefreshCw, Building2, ShoppingBag, Home, Briefcase, Zap, CheckCircle2 } from 'lucide-react';

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

  // Watch form fields to compute live quality score
  const watchedBusiness = watch('businessName');
  const watchedProduct = watch('productName');
  const watchedDesc = watch('productDescription');
  const watchedAudience = watch('targetAudience');
  const watchedBudget = watch('budget');
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

  const labelClass = 'block text-[11px] font-mono font-bold text-slate-400 uppercase tracking-wider mb-1.5';
  const inputClass = 'w-full bg-slate-950/40 border border-slate-800/60 shadow-2xl rounded-xl px-3.5 py-2.5 text-xs text-slate-100 placeholder:text-slate-600 focus:ring-1 focus:ring-cyan-500 focus:border-cyan-500 outline-none transition-all font-sans';

  return (
    <div className="w-full space-y-6">
      {/* Top Presets Banner */}
      <div className="bg-slate-950/60 border border-slate-800/80 rounded-2xl p-4 space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-cyan-400" />
            <span className="text-xs font-bold text-slate-200 uppercase tracking-wider font-mono">1-Click Vertical Presets</span>
          </div>
          <span className="text-[11px] text-slate-500 font-mono">Load calibrated parameters</span>
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
                    ? 'bg-cyan-500/15 border-cyan-500/50 text-cyan-200 shadow-md shadow-cyan-500/10'
                    : 'bg-slate-900/50 border-slate-800 hover:border-slate-700 hover:bg-slate-900 text-slate-300'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <Icon className={`w-4 h-4 ${isSelected ? 'text-cyan-400' : 'text-slate-500 group-hover:text-slate-300'}`} />
                  {isSelected && <CheckCircle2 className="w-3.5 h-3.5 text-cyan-400" />}
                </div>
                <div>
                  <div className="text-xs font-bold leading-tight">{preset.name}</div>
                  <div className="text-[10px] text-slate-500 font-mono mt-0.5 leading-tight">{preset.category}</div>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Brief Completeness Indicator */}
      <div className="bg-slate-950/40 border border-slate-800/60 rounded-xl p-3.5 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-cyan-500/20 to-blue-500/20 border border-cyan-500/30 flex items-center justify-center text-cyan-300 text-xs font-mono font-bold">
            {qualityScore}%
          </div>
          <div>
            <div className="text-xs font-bold text-slate-200">Brief Completeness Score</div>
            <div className="text-[10px] text-slate-500 font-mono">
              {qualityScore >= 80 ? 'ðŸŽ¯ Excellent readiness for 18-agent pipeline' : 'âš ï¸ Add more detail to optimize agent accuracy'}
            </div>
          </div>
        </div>

        <div className="w-32 bg-slate-900 h-2 rounded-full overflow-hidden border border-slate-800">
          <div
            className={`h-full transition-all duration-500 rounded-full ${
              qualityScore >= 80 ? 'bg-gradient-to-r from-cyan-400 to-emerald-400' : 'bg-gradient-to-r from-amber-400 to-cyan-400'
            }`}
            style={{ width: `${qualityScore}%` }}
          />
        </div>
      </div>

      {submitError && (
        <div className="p-3.5 bg-rose-500/10 border border-rose-500/30 rounded-xl text-rose-300 text-xs flex items-start gap-2.5">
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
            {errors.businessName && <span className="text-[10px] text-rose-400 mt-1 block">{errors.businessName.message}</span>}
          </div>

          <div>
            <label className={labelClass}>Product / Offering *</label>
            <input
              type="text"
              {...register('productName', { required: 'Product name is required' })}
              className={inputClass}
              placeholder="e.g. Enterprise Security Platform"
            />
            {errors.productName && <span className="text-[10px] text-rose-400 mt-1 block">{errors.productName.message}</span>}
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
          {errors.productDescription && <span className="text-[10px] text-rose-400 mt-1 block">{errors.productDescription.message}</span>}
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
          {errors.targetAudience && <span className="text-[10px] text-rose-400 mt-1 block">{errors.targetAudience.message}</span>}
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
              { id: 'lead_generation', label: 'ðŸŽ¯ Lead Generation' },
              { id: 'sales_conversion', label: 'âš¡ Direct Sales / ROAS' },
              { id: 'brand_awareness', label: 'ðŸš€ Brand Awareness' },
              { id: 'retargeting', label: 'ðŸ”„ BOFU Retargeting' },
            ].map((goal) => {
              const isChecked = selectedGoals.includes(goal.id);
              return (
                <button
                  key={goal.id}
                  type="button"
                  onClick={() => handleGoalToggle(goal.id)}
                  className={`px-3 py-1.5 rounded-xl text-xs font-semibold border transition-all ${
                    isChecked
                      ? 'bg-cyan-500/20 border-cyan-500/50 text-cyan-300 shadow-sm'
                      : 'bg-slate-900/60 border-slate-800 text-slate-400 hover:text-slate-300'
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
            className="w-full py-3 px-4 rounded-xl font-bold text-xs uppercase tracking-wider bg-gradient-to-r from-cyan-500 via-blue-600 to-purple-600 hover:from-cyan-400 hover:to-purple-500 text-white shadow-lg shadow-cyan-500/20 active:scale-[0.99] transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
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

