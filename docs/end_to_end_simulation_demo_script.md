# End-to-End Simulation Demo Script

## Intro
"Welcome to the ADPilot Autonomous Campaign Demo. What you are looking at is the Enterprise AI Control Center. This isn't a mock UI, this is a real-time visualization of the ADPilot orchestration engine running a live campaign simulation."

## Execution
"I'll start the simulation. The system initializes the Campaign Context and kicks off the 18-stage pipeline."

*Click RUN FULL SIMULATION*

## Strategy & Research
"First, the Strategy and Research Agents take the ,000 budget and Lead Generation goal, using our LLM stack to synthesize an audience targeting approach."
*Click the Strategy Agent node to show inputs/outputs*

## Content & Design
"Next, the Content Agent builds the copy, passing it to the Design Agent, which triggers Nano Banana (Google Gemini 3.1 Flash) to construct aligned creatives. You can see the explicit prompts generated in the Agent Inspector on the right."

## Analytics & Optimization (RL/PPO)
"Here is where the real power lies. The Analytics Agent predicts our baseline ROAS. Then, the RL/PPO Optimizer acts on those metrics. It recognizes Meta is underperforming in the simulated environment and reallocates 5% of the budget to Google, resulting in a positive reward of +0.74."
*Click the RL / PPO Optimizer node*

## Human-in-the-loop (HITL)
"The system pauses. It doesn't spend money automatically. It awaits our governance gate."
*Click APPROVE ACTION in the HITL panel*

## Conclusion
"Upon approval, the pipeline finalizes the campaign. Notice the Simulated Performance block: our ROAS improved from 3.21x to 3.68x. This demonstrates autonomous AI optimization paired with strict human governance."
