import type { AgentContract } from '../types';

export const MASTER_AGENTS: AgentContract[] = [
  {
    id: 'strategy',
    name: 'Strategy Planning Agent',
    role: 'Autonomous Strategic Direction & Channel Mix',
    model: 'GPT-4o / Claude 3.5 Sonnet Router',
    modelType: 'LLM',
    inputs: ['CampaignContext', 'Brand Memory', 'Budget Constraint'],
    outputs: ['StrategyPlan', 'ChannelAllocationMatrix', 'TargetingDirectives'],
    tools: ['RAG Knowledge Base', 'Brand Memory Store', 'Epistemic Directives'],
    downstream: ['Research Agent', 'Campaign Planner'],
    confidence: 96,
    latencyMs: 1420,
    status: 'completed',
    responsibility: 'Synthesizes enterprise business objectives, ICP target criteria, and budget constraints into a structured cross-channel marketing roadmap.',
    sampleInput: {
      budget: 10000,
      goals: ['lead_generation', 'sales_conversion'],
      product_type: 'saas',
      target_audience: 'B2B SMBs & SaaS Founders'
    },
    sampleOutput: {
      recommended_channels: ['LinkedIn (45%)', 'Meta Ads (35%)', 'Google Search (20%)'],
      target_cac: '$42.50',
      projected_roas: '3.8x',
      strategic_pillars: ['Efficiency-first workflows', 'Measurable pipeline velocity']
    }
  },
  {
    id: 'research',
    name: 'Audience & Market Research Agent',
    role: 'Deep Demographic & Pain Point Extraction',
    model: 'FastEmbed BGE + Hybrid RRF Reranker',
    modelType: 'Vector Embeddings',
    inputs: ['StrategyPlan', 'Customer Memory', 'Historical Cohorts'],
    outputs: ['AudienceProfile', 'PainPointClusters', 'PurchaseDrivers'],
    tools: ['FastEmbed BGE-small', 'Qdrant Vector DB', 'BM25 Lexical Search'],
    downstream: ['Competitor Agent', 'Content Agent'],
    confidence: 94,
    latencyMs: 820,
    status: 'completed',
    responsibility: 'Retrieves verified market trends, ICP psychological triggers, and customer lifetime value cohorts using dense semantic and lexical hybrid search.',
    sampleInput: {
      icp_segment: 'SaaS Decision Makers',
      niche: 'Autonomous B2B Marketing'
    },
    sampleOutput: {
      primary_decision_triggers: ['Peer Recommendations (67%)', 'ROI Proof (54%)', 'Low-friction Trial (48%)'],
      target_clv: '$12,400',
      pain_points: ['Fragmented tool stacks', 'High manual overhead', 'Unpredictable ROAS']
    }
  },
  {
    id: 'competitor',
    name: 'Competitor Intelligence Agent',
    role: 'Market Whitespace & Positioning Analysis',
    model: 'Market Intelligence Classifier',
    modelType: 'Classical ML',
    inputs: ['AudienceProfile', 'Category Rivals Index'],
    outputs: ['CompetitiveLandscape', 'DifferentiationMatrix', 'WhitespaceReport'],
    tools: ['Competitive Feature Indexer', 'Pricing Benchmark Engine'],
    downstream: ['Content Agent'],
    confidence: 91,
    latencyMs: 650,
    status: 'completed',
    responsibility: 'Identifies competitor messaging blindspots, price-to-value gaps, and counter-positioning angles.',
    sampleInput: {
      industry: 'B2B Marketing Automation',
      market_tier: 'Mid-Market Growth'
    },
    sampleOutput: {
      whitespace_opportunity: 'Enterprise capabilities with self-serve startup agility',
      counter_positioning: 'Native end-to-end multi-agent orchestration vs fragmented point solutions'
    }
  },
  {
    id: 'content',
    name: 'Content Copywriting Agent',
    role: 'Multi-Channel Ad Copy & Nurture Sequences',
    model: 'ML Ridge Copy Quality Scorer + GPT-4o',
    modelType: 'Classical ML',
    inputs: ['StrategyPlan', 'AudienceProfile', 'Brand Voice Directives'],
    outputs: ['AdCreativesSet', 'EmailNurtureSequence', 'SocialCampaignPack'],
    tools: ['ML Ridge Scorer (brand_voice_classifier.pkl)', 'Token Budgeter', 'CTR Estimator'],
    downstream: ['Design Agent', 'Analytics Agent'],
    confidence: 95,
    latencyMs: 1980,
    status: 'completed',
    responsibility: 'Generates high-converting ad headlines, body copies, CTAs, and automated 4-stage email sequences evaluated by Ridge ML quality models.',
    sampleInput: {
      channels: ['LinkedIn', 'Facebook', 'Google Ads'],
      tone: 'Professional & Authoritative'
    },
    sampleOutput: {
      copy_quality_score: 5.43,
      ad_variations_count: 8,
      email_sequences_count: 4,
      top_headline: 'Stop Burning Ad Spend: Meet Your Autonomous Marketing Operating System'
    }
  },
  {
    id: 'design',
    name: 'Design & Visual Creative Agent',
    role: 'AI Image Generation & Multi-Format Canvas',
    model: 'Nano Banana Studio & Diffusion Canvas',
    modelType: 'Computer Vision',
    inputs: ['AdCreativesSet', 'Brand Color Palette', 'Aspect Ratio Matrix'],
    outputs: ['DesignAssetPack', 'VisualPrompts', 'RenderedAdCards'],
    tools: ['NanoBanana Diffusion API', 'ML Aesthetic Scorer', 'Color Harmony Validator'],
    downstream: ['CV Agent'],
    confidence: 92,
    latencyMs: 2450,
    status: 'completed',
    responsibility: 'Generates creative visual prompts and renders platform-optimized multi-aspect visual assets (1:1, 16:9, 9:16) with aesthetic validation.',
    sampleInput: {
      aspect_ratios: ['1:1 (Feed)', '16:9 (Display)', '9:16 (Stories)'],
      brand_palette: ['#030712', '#2563EB', '#00C8A0']
    },
    sampleOutput: {
      aesthetic_prior_score: 3.13,
      rendered_assets: 4,
      formats_delivered: ['LinkedIn Banner', 'Instagram Square', 'Facebook Lead Card', 'Google Display']
    }
  },
  {
    id: 'cv',
    name: 'Computer Vision (CV) Agent',
    role: 'Visual Quality, OCR & Compliance Gate',
    model: 'CLIP-ViT-B/32 Zero-Shot + Quality Regressor',
    modelType: 'Computer Vision',
    inputs: ['DesignAssetPack', 'Brand Guidelines'],
    outputs: ['VisualComplianceReport', 'AestheticScoreCard', 'TextLegibilityScore'],
    tools: ['CLIP-ViT Embedding Head', 'PyTorch Aesthetic Scorer', 'OCR Text Density Checker'],
    downstream: ['Analytics Agent'],
    confidence: 93,
    latencyMs: 410,
    status: 'completed',
    responsibility: 'Inspects rendered visual assets for visual compliance, text overlap, safe margins, and aesthetic quality using zero-shot CLIP vision embeddings.',
    sampleInput: {
      asset_count: 4,
      inspection_criteria: ['Brand Compliance', 'Safe Zone Margins', 'Contrast Ratio']
    },
    sampleOutput: {
      mean_aesthetic_score: 8.7,
      compliance_pass: true,
      text_density_ok: true
    }
  },
  {
    id: 'analytics',
    name: 'Analytics & Performance Forecasting Agent',
    role: 'Predictive ROI, CAC & Conversion Modeling',
    model: 'Sklearn Ridge Multi-Target Forecaster + StandardScaler',
    modelType: 'Classical ML',
    inputs: ['ChannelAllocationMatrix', 'AdCreativesSet', 'Historical Performance Data'],
    outputs: ['ROASForecast', 'CACPrediction', 'ImpressionProjections', 'HealthScore'],
    tools: ['Ridge Multi-Output Regressor (revenue_forecaster.pkl)', 'StandardScaler (scaler.pkl)'],
    downstream: ['RL Optimizer Agent'],
    confidence: 89,
    latencyMs: 310,
    status: 'completed',
    responsibility: 'Computes deterministic econometric predictions for campaign reach, expected conversion rates, ROAS, and composite quality health scores.',
    sampleInput: {
      budget: 10000,
      channel_weights: [0.45, 0.35, 0.20]
    },
    sampleOutput: {
      predicted_roas: 3.84,
      predicted_cac: '$42.10',
      projected_impressions: '145,000 - 180,000',
      composite_health_score: 87.5
    }
  },
  {
    id: 'optimizer',
    name: 'RL Policy Optimizer Agent',
    role: 'Autonomous Continuous Budget & Action Optimizer',
    model: 'PPO Neural Policy Checkpoint (ppo_policy.pt)',
    modelType: 'RL Neural Policy',
    inputs: ['StateVector s_t (12-dim)', 'Budget Constraints', 'Target ROAS'],
    outputs: ['OptimizedActionVector a_t', 'ChannelReallocations', 'BidAdjustments'],
    tools: ['PyTorch PPO Policy Network', 'Constraint Guard Validator', 'Simulated Campaign Env'],
    downstream: ['Correction Engine', 'Human-in-the-Loop Gate'],
    confidence: 94,
    latencyMs: 290,
    status: 'completed',
    responsibility: 'Applies deep reinforcement learning (PPO) over continuous action spaces to rebalance budget allocations and optimize expected rewards.',
    sampleInput: {
      state_vector: [0.45, 0.35, 0.20, 3.84, 42.10, 0.045, 0.062, 0.88, 10000, 30, 0.92, 0.85]
    },
    sampleOutput: {
      recommended_action: 'Increase LinkedIn budget +12%, reduce Google Search -8%',
      expected_roas_delta: '+0.32x',
      cost_efficiency_gain: '+14.2%'
    }
  },
  {
    id: 'correction',
    name: 'Correction & Diagnostic Engine',
    role: 'Multi-Source Defect Detection & Self-Healing',
    model: 'Defect Diagnostic Classifier',
    modelType: 'Deterministic Engine',
    inputs: ['Pre-Execution Outputs', 'Constraint Violations', 'Compliance Checks'],
    outputs: ['DiagnosticReport', 'CorrectiveTaskDispatches', 'SelfHealingStatus'],
    tools: ['ConstraintValidator', 'Corrective Dispatch Router'],
    downstream: ['Human-in-the-Loop Gate'],
    confidence: 96,
    latencyMs: 180,
    status: 'completed',
    responsibility: 'Detects cross-agent inconsistencies, boundary constraint violations, and triggers targeted corrective tasks before publishing.',
    sampleInput: {
      quality_threshold: 80,
      current_scores: { content: 88, design: 85, analytics: 87.5 }
    },
    sampleOutput: {
      defects_detected: 0,
      integrity_status: 'HEALTHY_NOMINAL',
      ready_for_review: true
    }
  },
  {
    id: 'hitl',
    name: 'Human-in-the-Loop Governance Gate',
    role: 'Enterprise Approval, Override & Audit Store',
    model: 'RBAC Policy Guard & HITLAuditStore',
    modelType: 'Deterministic Engine',
    inputs: ['Compiled Campaign Package', 'Optimizer Recommendations', 'User Review Directives'],
    outputs: ['ApprovedPayload', 'HITLAuditRecord', 'RevisionDirectives'],
    tools: ['HITL Review Manager', 'Async SQLite Audit Store', 'Cryptographic Token Validator'],
    downstream: ['Publishing Agent'],
    confidence: 100,
    latencyMs: 50,
    status: 'completed',
    responsibility: 'Ensures no high-risk campaign execution or budget modification occurs without human approval and full immutable audit trail logging.',
    sampleInput: {
      campaign_id: 'camp-2026-saas',
      action_type: 'PUBLISHING_DISPATCH',
      reviewer_role: 'Marketing Director'
    },
    sampleOutput: {
      decision: 'APPROVED',
      audit_id: 'audit-9941a8e2',
      authorized_by: 'Lead Campaign Director',
      status: 'GATE_PASSED'
    }
  }
];
