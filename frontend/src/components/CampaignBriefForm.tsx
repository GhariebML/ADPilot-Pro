import React from 'react';
import { useForm } from 'react-hook-form';
import type { CampaignBrief } from '../types';
import { campaignService } from '../services/api';
import { Sparkles, Rocket, AlertCircle, RefreshCw } from 'lucide-react';

interface CampaignBriefFormProps {
  onSubmit: (taskId: string) => void;
  isLoading?: boolean;
}

export const CampaignBriefForm: React.FC<CampaignBriefFormProps> = ({ onSubmit, isLoading = false }) => {
  const { register, handleSubmit, setValue, watch, formState: { errors } } = useForm<CampaignBrief>({
    defaultValues: {
      businessName: '',
      productName: '',
      productDescription: '',
      targetAudience: '',
      goals: ['lead_generation', 'sales_conversion'],
      budget: 0,
      duration: '1-week',
      tone: 'professional',
    },
  });

  const [submitError, setSubmitError] = React.useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = React.useState(false);

  const selectedTone = watch('tone');
  const selectedGoals = watch('goals') || [];

  const handleGoalToggle = (goal: string) => {
    const current = selectedGoals;
    if (current.includes(goal)) {
      setValue('goals', current.filter((g) => g !== goal));
    } else {
      setValue('goals', [...current, goal]);
    }
  };

  const handleLoadSample = () => {
    setValue('businessName', 'FutureCorp AI');
    setValue('productName', 'NeuralLink v2 Platform');
    setValue('productDescription', 'Value proposition & key features of autonomous AI marketing orchestrator.');
    setValue('targetAudience', 'Tech enthusiasts, early adopters, B2B SaaS Founders');
    setValue('goals', ['lead_generation', 'sales_conversion']);
    setValue('budget', 5000);
    setValue('duration', '1-month');
    setValue('tone', 'professional');
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

  const labelClass = 'block text-[10px] font-mono font-bold text-slate-400 uppercase tracking-wider mb-1.5';
  const inputClass = 'w-full bg-slate-950/80 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-slate-100 placeholder:text-slate-600 focus:ring-1 focus:ring-cyan-500 focus:border-cyan-500 outline-none transition-all font-sans';

  return (
    <div className="w-full space-y-5">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800/80 pb-4">
        <div>
          <h2 className="text-base font-bold text-slate-100 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-cyan-400" />
            Campaign Brief
          </h2>
          <p className="text-[11px] text-slate-400 mt-0.5">Define mission parameters for AI orchestration.</p>
        </div>

        <button
          type="button"
          onClick={handleLoadSample}
          className="px-2.5 py-1 rounded-lg text-[10px] font-mono font-semibold bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 flex items-center gap-1 transition-colors"
        >
          <Sparkles className="w-3 h-3" />
          <span>Load Preset</span>
        </button>
      </div>

      {submitError && (
        <div className="p-3 bg-rose-500/10 border border-rose-500/30 rounded-xl text-rose-300 text-xs flex items-start gap-2.5">
          <AlertCircle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
          <div className="flex-1">
            <p className="font-semibold">{submitError}</p>
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-4">
        {/* Business Name */}
        <div>
          <label className={labelClass}>Business Name</label>
          <input
            type="text"
            {...register('businessName', { required: 'Business name is required' })}
            className={inputClass}
            placeholder="e.g. FutureCorp"
          />
          {errors.businessName && <span className="text-[10px] text-rose-400 mt-1 block">{errors.businessName.message}</span>}
        </div>

        {/* Product Name */}
        <div>
          <label className={labelClass}>Product / Service</label>
          <input
            type="text"
            {...register('productName', { required: 'Product name is required' })}
            className={inputClass}
            placeholder="e.g. NeuralLink v2"
          />
          {errors.productName && <span className="text-[10px] text-rose-400 mt-1 block">{errors.productName.message}</span>}
        </div>

        {/* Product Description */}
        <div>
          <label className={labelClass}>Product Description</label>
          <textarea
            rows={3}
            {...register('productDescription', { required: 'Description is required' })}
            className={`${inputClass} resize-none`}
            placeholder="Value proposition & key features..."
          />
          {errors.productDescription && <span className="text-[10px] text-rose-400 mt-1 block">{errors.productDescription.message}</span>}
        </div>

        {/* Target Audience */}
        <div>
          <label className={labelClass}>Target Audience</label>
          <input
            type="text"
            {...register('targetAudience', { required: 'Target audience is required' })}
            className={inputClass}
            placeholder="e.g. Tech enthusiasts, early adopters"
          />
        </div>

        {/* Campaign Goals */}
        <div>
          <label className={labelClass}>Campaign Goals</label>
          <div className="grid grid-cols-2 gap-1.5">
            {[
              { id: 'lead_generation', label: 'Lead Generation' },
              { id: 'sales_conversion', label: 'Sales & Revenue' },
              { id: 'brand_awareness', label: 'Brand Awareness' },
              { id: 'engagement', label: 'Engagement' },
            ].map((g) => {
              const active = selectedGoals.includes(g.id);
              return (
                <button
                  type="button"
                  key={g.id}
                  onClick={() => handleGoalToggle(g.id)}
                  className={`p-2 rounded-lg text-[11px] font-medium border text-left transition-all ${
                    active
                      ? 'bg-cyan-500/20 text-cyan-300 border-cyan-500/50 shadow-sm'
                      : 'bg-slate-950/60 text-slate-400 border-slate-800 hover:border-slate-700'
                  }`}
                >
                  {g.label}
                </button>
              );
            })}
          </div>
        </div>

        {/* Budget & Duration */}
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className={labelClass}>Budget ($ USD)</label>
            <input
              type="number"
              {...register('budget', { valueAsNumber: true, required: true })}
              className={inputClass}
              placeholder="5000"
            />
          </div>
          <div>
            <label className={labelClass}>Duration</label>
            <select
              {...register('duration')}
              className={inputClass}
            >
              <option value="1-week">1 Week</option>
              <option value="2-weeks">2 Weeks</option>
              <option value="1-month">1 Month</option>
              <option value="3-months">3 Months</option>
            </select>
          </div>
        </div>

        {/* Brand Tone */}
        <div>
          <label className={labelClass}>Brand Persona & Tone</label>
          <div className="grid grid-cols-3 gap-1.5">
            {[
              { id: 'professional', label: 'Professional' },
              { id: 'casual', label: 'Casual' },
              { id: 'playful', label: 'Playful' },
              { id: 'luxury', label: 'Luxury' },
              { id: 'technical', label: 'Technical' },
              { id: 'modern', label: 'Modern & Edgy' },
            ].map((t) => (
              <button
                type="button"
                key={t.id}
                onClick={() => setValue('tone', t.id)}
                className={`py-1.5 px-2 rounded-lg text-[11px] font-medium border transition-all text-center ${
                  selectedTone === t.id
                    ? 'bg-purple-500/20 text-purple-300 border-purple-500/50 shadow-sm'
                    : 'bg-slate-950/60 text-slate-400 border-slate-800 hover:border-slate-700'
                }`}
              >
                {t.label}
              </button>
            ))}
          </div>
        </div>

        {/* Launch Button */}
        <button
          type="submit"
          aria-label="Initialize Campaign Generation"
          disabled={isSubmitting || isLoading}
          className="w-full py-3 px-4 rounded-xl text-xs font-bold font-mono tracking-wider uppercase bg-gradient-to-r from-cyan-500 via-blue-600 to-purple-600 hover:from-cyan-400 hover:to-purple-500 text-white shadow-lg shadow-cyan-500/25 transition-all flex items-center justify-center gap-2 disabled:opacity-50 active:scale-[0.98] mt-2"
        >
          {isSubmitting || isLoading ? (
            <>
              <RefreshCw className="w-4 h-4 animate-spin" />
              <span>Initialize Campaign Generation (Orchestrating...)</span>
            </>
          ) : (
            <>
              <Rocket className="w-4 h-4" />
              <span>Initialize Campaign Generation</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
};
