# Nano Banana Local Demo

To run the local demo for the Gemini integration:

1. Setup Environment:
   Ensure GEMINI_API_KEY is set in your .env file if you want real images, otherwise it will fall back to placeholders.

2. Start Backend:
   `ash
   cd src
   uv run uvicorn adpilot.api.main:app --reload --port 8000
   `

3. Start Frontend:
   `ash
   cd frontend
   npm run dev
   `

4. Open http://localhost:5173 and navigate to the Creative Studio (Nano Banana Studio).
5. Click **Generate Creatives (Nano Banana)**.
6. The frontend will hit /api/creative/generate, which will run the DesignAgent and CreativeEvaluator, routing the request to GeminiImageGenerationProvider.
7. You will see the generated creatives populate the grid.
