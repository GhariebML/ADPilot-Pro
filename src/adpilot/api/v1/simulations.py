from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, List
import uuid

from ...schemas.simulation_schemas import CampaignSimulation
from ...core.simulation_store import simulation_store
from ...orchestrator.simulation_runner import SimulationRunner

router = APIRouter()

class SimulationCreateReq(BaseModel):
    product_name: str
    product_type: str
    campaign_objective: str
    target_audience: str
    budget: float
    duration_days: int
    platforms: List[str]
    target_cac: float
    target_roas: float

@router.post("")
def create_simulation(req: SimulationCreateReq):
    sim = CampaignSimulation(
        campaign_id=str(uuid.uuid4()),
        campaign_input=req.model_dump()
    )
    simulation_store.save(sim)
    return {"simulation_id": sim.simulation_id}

@router.post("/{sim_id}/run")
def run_simulation(sim_id: str, background_tasks: BackgroundTasks):
    sim = simulation_store.get(sim_id)
    if not sim:
        raise HTTPException(404, "Simulation not found")
        
    runner = SimulationRunner(sim_id)
    background_tasks.add_task(runner.run)
    return {"status": "started"}

@router.get("/{sim_id}")
def get_simulation(sim_id: str):
    sim = simulation_store.get(sim_id)
    if not sim:
        raise HTTPException(404, "Simulation not found")
    return sim.model_dump()

class HITLReq(BaseModel):
    decision: str
    feedback: str = ""

@router.post("/{sim_id}/human-review")
def hitl_review(sim_id: str, req: HITLReq):
    sim = simulation_store.get(sim_id)
    if not sim:
        raise HTTPException(404, "Simulation not found")
    
    sim.human_review = req.model_dump()
    sim.status = "COMPLETED"
    sim.current_stage = "FINAL_DECISION"
    
    # Generate mock final results
    sim.final_result = {
        "roas_before": 3.21,
        "roas_after": 3.68,
        "cac_before": 47.80,
        "cac_after": 41.20,
        "conversion_rate_before": 3.4,
        "conversion_rate_after": 4.2
    }
    simulation_store.save(sim)
    return {"status": "decision_recorded"}

@router.post("/{sim_id}/approve")
def approve_simulation(sim_id: str):
    """Convenience endpoint: approve the simulation with a single click."""
    sim = simulation_store.get(sim_id)
    if not sim:
        raise HTTPException(404, "Simulation not found")

    sim.human_review = {"decision": "APPROVED", "feedback": "Approved via UI"}
    sim.status = "COMPLETED"
    sim.current_stage = "FINAL_DECISION"

    sim.final_result = {
        "roas_before": 3.21,
        "roas_after": 3.68,
        "cac_before": 47.80,
        "cac_after": 41.20,
        "conversion_rate_before": 3.4,
        "conversion_rate_after": 4.2
    }
    simulation_store.save(sim)
    return {"status": "approved"}
