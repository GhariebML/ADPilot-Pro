from typing import Dict, Optional
from ..schemas.simulation_schemas import CampaignSimulation

class SimulationStore:
    def __init__(self):
        self._simulations: Dict[str, CampaignSimulation] = {}
        
    def save(self, sim: CampaignSimulation):
        self._simulations[sim.simulation_id] = sim
        
    def get(self, sim_id: str) -> Optional[CampaignSimulation]:
        return self._simulations.get(sim_id)

    def list_all(self):
        return list(self._simulations.values())

simulation_store = SimulationStore()
