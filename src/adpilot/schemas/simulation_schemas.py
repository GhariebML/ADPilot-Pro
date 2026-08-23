import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class AgentExecutionTrace(BaseModel):
    agent_name: str
    purpose: str
    input: Dict[str, Any]
    output: Dict[str, Any]
    model_used: str
    tools_used: List[str]
    status: str
    validation_status: str
    execution_time: float
    error: Optional[str] = None
    corrective_action: Optional[str] = None

class SimulationEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    simulation_id: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    stage: str
    agent_name: str
    event_type: str
    input: Dict[str, Any]
    output: Dict[str, Any]
    model: str
    tool: str
    status: str
    latency: float
    metadata: Dict[str, Any] = Field(default_factory=dict)

class CampaignSimulation(BaseModel):
    simulation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    campaign_id: str
    campaign_input: Dict[str, Any]
    current_stage: str = "PENDING"
    status: str = "WAITING"
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    events: List[SimulationEvent] = Field(default_factory=list)
    agent_executions: Dict[str, AgentExecutionTrace] = Field(default_factory=dict)
    metrics: Dict[str, Any] = Field(default_factory=dict)
    decisions: List[Dict[str, Any]] = Field(default_factory=list)
    human_review: Optional[Dict[str, Any]] = None
    final_result: Optional[Dict[str, Any]] = None
