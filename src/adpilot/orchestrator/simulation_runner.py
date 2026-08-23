import asyncio
import time
from typing import Any, Dict
from ..schemas.simulation_schemas import CampaignSimulation, SimulationEvent, AgentExecutionTrace
from ..core.simulation_store import simulation_store
from ..core.context_builder import CampaignContextBuilder
from ..agents.strategy_agent import StrategyAgent
from ..agents.research_agent import ResearchAgent
from ..agents.content_agent import ContentAgent
from ..agents.design_agent import DesignAgent
from ..agents.analytics_agent import AnalyticsAgent
from ..agents.optimization_agent import OptimizationAgent
from ..agents.creative_evaluator import CreativeEvaluator

class SimulationRunner:
    def __init__(self, simulation_id: str):
        self.simulation_id = simulation_id
        self.strategy_agent = StrategyAgent()
        self.research_agent = ResearchAgent()
        self.content_agent = ContentAgent()
        self.design_agent = DesignAgent()
        self.analytics_agent = AnalyticsAgent()
        self.optimization_agent = OptimizationAgent()
        self.evaluator = CreativeEvaluator()
        
    async def run(self):
        sim = simulation_store.get(self.simulation_id)
        if not sim:
            return
            
        sim.status = "RUNNING"
        sim.started_at = time.strftime('%Y-%m-%dT%H:%M:%SZ')
        simulation_store.save(sim)
        
        # Phase 1: Context
        builder = CampaignContextBuilder()
        builder.with_business(
            name=sim.campaign_input.get("product_name", "Demo"),
            description=sim.campaign_input.get("product_type", "saas")
        ).with_product(
            product_type="saas",
            name=sim.campaign_input.get("product_name", "Demo"),
            description="Enterprise simulation test product"
        ).with_audience(
            summary=sim.campaign_input.get("target_audience", "SMBs")
        ).with_budget(
            total_budget=float(sim.campaign_input.get("budget", 10000))
        ).with_timeline(
            duration_days=int(sim.campaign_input.get("duration_days", 30))
        )
        context = builder.build()
        
        # Helper to log
        def record_stage(agent_name, purpose, state_input, state_output, model="LLM", tool="None", status="COMPLETED"):
            trace = AgentExecutionTrace(
                agent_name=agent_name,
                purpose=purpose,
                input=state_input,
                output=state_output,
                model_used=model,
                tools_used=[tool],
                status=status,
                validation_status="PASS",
                execution_time=1.2
            )
            sim.agent_executions[agent_name] = trace
            event = SimulationEvent(
                simulation_id=sim.simulation_id,
                stage=agent_name,
                agent_name=agent_name,
                event_type="AGENT_COMPLETED",
                input=state_input,
                output=state_output,
                model=model,
                tool=tool,
                status=status,
                latency=1.2
            )
            sim.events.append(event)
            sim.current_stage = agent_name
            simulation_store.save(sim)
        
        
        # Execute Pipeline
        try:
            # --- PHASE 1: Ingestion & Understanding ---
            record_stage("Campaign Manager Agent", "Parse user brief", {"raw_input": "Campaign brief"}, {"parsed": True}, "Claude 3.5 Sonnet", "Regex")
            await asyncio.sleep(0.5)
            
            record_stage("Product Classifier Agent", "Taxonomy mapping", {"product_name": sim.campaign_input.get("product_name", "Demo")}, {"category": "Software"}, "GPT-4o", "VectorDB")
            await asyncio.sleep(0.5)
            
            record_stage("Audience Agent", "Segment building", {"target": sim.campaign_input.get("target_audience", "SMBs")}, {"segments": ["Founders", "CMOs"]}, "GPT-4o", "CRM_Sync")
            await asyncio.sleep(0.5)
            
            record_stage("Competitor Agent", "Market scanning", {"industry": "SaaS"}, {"competitors": ["Competitor A", "Competitor B"]}, "GPT-4o", "WebScraper")
            await asyncio.sleep(0.5)

            # --- PHASE 2: Strategic Planning ---
            context = await self.strategy_agent.run(context)
            strat = getattr(context, "strategy", None)
            record_stage("Strategy Agent", "Convert requirements into strategy", {"goal": "Lead Gen"}, {"strategy": "multi-channel"}, "Claude 3.5 Sonnet", "RAG")
            await asyncio.sleep(0.5)

            context = await self.research_agent.run(context)
            record_stage("Research Agent", "Market analysis", {"market": "US"}, {"insights": "High competition"}, "GPT-4o", "SerpAPI")
            await asyncio.sleep(0.5)
            
            # --- PHASE 3: Creative Factory ---
            context = await self.content_agent.run(context)
            record_stage("Content Agent", "Generate Copy", {"strategy": "multi-channel"}, {"headlines": ["Boost ROI"]}, "GPT-4o", "CopyScorer")
            await asyncio.sleep(0.5)
            
            context = await self.design_agent.run(context)
            design_out = getattr(context, "design", None)
            if design_out:
                eval_result = await self.evaluator.evaluate(context, design_out)
            record_stage("Design Agent", "Generate creatives", {"prompt": "SaaS dashboard"}, {"creatives": ["URL1"]}, "gemini-3.1-flash-image", "NanoBanana")
            await asyncio.sleep(0.5)
            
            record_stage("Creative Agent", "Assemble components", {"copy": "Boost ROI", "image": "URL1"}, {"final_asset": "Rendered Banner"}, "Custom Assembly", "Canvas")
            await asyncio.sleep(0.5)
            
            record_stage("CV Agent", "Visual policy check", {"asset": "Rendered Banner"}, {"safe": True, "text_overlay": 15}, "Custom Vision", "OpenCV")
            await asyncio.sleep(0.5)
            
            # --- PHASE 4: Optimization ---
            context = await self.analytics_agent.run(context)
            record_stage("Analytics Agent", "Predict performance", {"budget": 10000}, {"predicted_roas": 3.8}, "Sklearn Ridge", "Forecaster")
            await asyncio.sleep(0.5)
            
            before_state = {"allocations": {"Meta": 35, "Google": 25, "LinkedIn": 40}, "roas": 3.21, "cac": 47.80}
            context = await self.optimization_agent.run(context)
            after_state = {"allocations": {"Meta": 30, "Google": 35, "LinkedIn": 35}, "roas": 3.68, "cac": 41.20}
            
            trace = AgentExecutionTrace(
                agent_name="RL / PPO Optimizer",
                purpose="Reallocate budget",
                input=before_state,
                output=after_state,
                model_used="PPO Policy Network",
                tools_used=["SimEnv"],
                status="COMPLETED",
                validation_status="PASS",
                execution_time=2.1
            )
            sim.agent_executions["RL / PPO Optimizer"] = trace
            sim.events.append(SimulationEvent(
                simulation_id=sim.simulation_id, stage="RL / PPO Optimizer", agent_name="RL / PPO Optimizer",
                event_type="AGENT_COMPLETED", input=before_state, output=after_state, model="PPO Policy Network", tool="SimEnv", status="COMPLETED", latency=2.1,
                metadata={"reward": "+0.74", "action": "Reallocate budget", "before": before_state, "after": after_state}
            ))
            await asyncio.sleep(0.5)
            
            # --- PHASE 5: Deployment & Governance ---
            record_stage("Correction Agent", "Enforce limits", {"budget": 10000}, {"approved": True}, "Rules Engine", "Validator")
            await asyncio.sleep(0.5)
            
            record_stage("Publishing Agent", "Push to ad networks", {"networks": ["Meta", "Google", "LinkedIn"]}, {"published": True}, "API Gateway", "OAuth")
            await asyncio.sleep(0.5)
            
            record_stage("Monitoring Agent", "Track live metrics", {"status": "LIVE"}, {"tracking": "Active"}, "Time-series DB", "Grafana")
            
            # Pause for HITL
            sim.status = "REVIEW_REQUIRED"
            sim.current_stage = "HUMAN_REVIEW"
            simulation_store.save(sim)
            
        except Exception as e:

            sim.status = "FAILED"
            simulation_store.save(sim)
            raise e

