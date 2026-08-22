export interface CampaignBrief {
  businessName: string;
  productName: string;
  productDescription: string;
  targetAudience: string;
  goals: string[];
  budget: number;
  duration: string;
  tone: string;
}

export interface TaskResponse {
  taskId: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  progress: number;
  message?: string;
}

export interface ContentOutput {
  ads: AdContent[];
  emailSequences: EmailSequence[];
  socialPosts: SocialPost[];
  summary?: string;
}

export interface AdContent {
  platform: string;
  headline: string;
  body: string;
  cta: string;
  performance?: string;
  targetAudience?: string;
  funnelStage?: string;
  adFormat?: string;
  visualPrompt?: string;
  hashtags?: string[];
  cpcEstimate?: string;
  ctrEstimate?: string;
}

export interface EmailSequence {
  subject: string;
  preview: string;
  body: string;
  sequence: number;
  sendDay?: number;
  triggerCondition?: string;
  goal?: string;
  audienceFocus?: string;
}

export interface SocialPost {
  platform: string;
  content: string;
  hashtags: string[];
  imagePrompt?: string;
  postType?: string;
  bestTimeToPost?: string;
  captionCopy?: string;
}

export interface DesignAsset {
  id: number;
  campaign_id: string;
  brief_json: Record<string, unknown>;
  image_url: string;
  created_at: string;
}

export interface DesignAssetsResponse {
  assets: DesignAsset[];
  total: number;
}

export type AgentExecutionStatus = 'idle' | 'running' | 'completed' | 'failed' | 'needs_approval';

export interface AgentContract {
  id: string;
  name: string;
  role: string;
  model: string;
  modelType: 'LLM' | 'Classical ML' | 'RL Neural Policy' | 'Computer Vision' | 'Deterministic Engine' | 'Vector Embeddings';
  inputs: string[];
  outputs: string[];
  tools: string[];
  downstream: string[];
  confidence: number;
  latencyMs: number;
  status: AgentExecutionStatus;
  sampleInput?: Record<string, unknown>;
  sampleOutput?: Record<string, unknown>;
  responsibility: string;
}

export interface HITLDecisionItem {
  id: string;
  stage: 'Strategy' | 'Content Copy' | 'Creative Assets' | 'Budget / Optimizer' | 'Publishing Dispatch';
  agent: string;
  title: string;
  riskLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  recommendation: string;
  predictedImpact: {
    roasDelta?: string;
    cacDelta?: string;
    reachDelta?: string;
  };
  reasoning: string;
  timestamp: string;
  status: 'PENDING' | 'APPROVED' | 'REJECTED' | 'REVISION_REQUESTED';
}

export interface ModelRegistryItem {
  id: string;
  name: string;
  category: 'Reinforcement Learning' | 'Classical ML Regression' | 'Zero-Shot Vision' | 'Vector Embeddings' | 'Foundation LLM Router';
  artifactPath: string;
  responsibleAgent: string;
  framework: 'PyTorch' | 'Scikit-Learn' | 'CLIP-ViT (ONNX)' | 'FastEmbed BGE' | 'OpenAI / Claude Router';
  status: 'PRODUCTION_READY' | 'ACTIVE_ONLINE' | 'STANDBY';
  inputDim: string;
  outputDim: string;
  inferenceLatency: string;
  accuracyOrReward: string;
}

export interface AIActivityEvent {
  id: string;
  timestamp: string;
  agent: string;
  action: string;
  level: 'info' | 'success' | 'warning' | 'error';
  details: string;
  latency?: string;
}
