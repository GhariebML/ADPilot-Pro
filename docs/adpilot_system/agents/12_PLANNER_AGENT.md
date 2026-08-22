# Planner Agent

## 1. Purpose
The **Planner Agent** constructs the strategic campaign execution roadmap, schedules milestones, assigns required agent dependencies, and defines the validation criteria for campaign delivery.

## 2. Business Responsibility
Provides structural project planning and resource coordination, ensuring all dependent creative and research deliverables are sequenced correctly before launching.

## 3. Technical Responsibility
Ingests `CampaignContext` and `ProductClassification`, builds a directed acyclic graph (DAG) of pipeline milestones, verifies dependencies, and emits `ExecutionPlan`.

## 4. Source Code
- `src/adpilot/orchestrator/planner.py`
- System Prompt: `src/adpilot/prompts/orchestrator_system_prompt.md`

## 5. Input
- `CampaignContext` (Budget, Goals, Timeline)
- `ProductClassification` (Vertical, Complexity)

## 6. Processing Flow
1. Determine required agent execution stages based on vertical complexity.
2. Formulate execution milestones with expected completion time estimates.
3. Validate dependency ordering (e.g., `Strategy` must precede `Content`).
4. Output structured `ExecutionPlan`.

## 7. Models Used
- Foundation LLM: OpenAI GPT-4o Router / Planner Heuristics.

## 8. Tools Used
- Dependency Validator (`src/adpilot/orchestrator/pipeline_runner.py`)

## 9. Output
- **Schema:** `ExecutionPlan`
  - `milestones: List[Dict[str, Any]]` (Stage, Agent, Dependencies, EstDurationMs)
  - `critical_path: List[str]`
  - `total_estimated_latency_ms: int`

## 10. Downstream Consumers
- `MasterOrchestrator` (controls stage execution sequence)
- `InteractivePipelineDAG` (renders live progress nodes in UI)

## 11. Error Handling
- Circular dependency detection with automatic topological sort resolution.

## 12. Validation
- Verifies that all 18 master pipeline stages have defined predecessor relationships.

## 13. Corrective Actions
- Auto-inserts missing prerequisites if an agent requires upstream context.

## 14. Human-in-the-Loop
- Displayed in the Interactive Pipeline DAG before campaign initialization.

## 15. Example Execution
```json
{
  "milestones": [
    { "stage": "Strategy", "agent": "StrategyAgent", "dependencies": ["Classifier"] },
    { "stage": "Research", "agent": "ResearchAgent", "dependencies": ["Strategy"] },
    { "stage": "Content", "agent": "ContentAgent", "dependencies": ["Research", "Competitor"] }
  ],
  "critical_path": ["Classifier", "Strategy", "Research", "Content", "Design", "Analytics", "Optimizer", "HITL", "Publishing"],
  "total_estimated_latency_ms": 18400
}
```

## 16. Implementation Status
[IMPLEMENTED]
