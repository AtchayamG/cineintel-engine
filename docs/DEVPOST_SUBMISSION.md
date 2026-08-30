# 🎬 Devpost Submission: CineIntel Engine (Parallel Track)

## Project Name
**CineIntel Engine: Real-Time Web Grounding, Film Trend Research & Autonomous Script Doctor**

## Elevator Pitch
An autonomous film intelligence and research engine that uses live Parallel Search and Gemini 3.7 Flash to generate source-aware screenplays with explicit uncertainty critiques. The public evaluator now runs both providers live and returns URL-bearing Parallel evidence.

## Selected Track
**Parallel Track** ($7,500 1st Place)

## Judge Links
- **Live Application:** https://cineintel-engine.vercel.app/
- **Public Repository:** https://github.com/AtchayamG/cineintel-engine
- **Demo Video:** https://youtu.be/Pc5cY7IAVMA
- **Supplemental Cinematic Evidence:** https://youtu.be/9eLQ5VUnhgs — fixed, pre-generated Veo + Lyria reel; Parallel live search evidence is demonstrated separately in the application and primary demo.
- **Runtime Note:** The public evaluator runs Gemini 3.7 Flash through Vertex AI and Parallel Search through an isolated application credential stored in Google Secret Manager. Public end-to-end proof is recorded in `docs/evidence/PUBLIC_RUNTIME_VERIFICATION_2026-08-30.md`.

## What It Does
1. **Live-Mode Open-Web Market Research**: Uses Parallel Search (`parallel-web`) to extract trending tropes, cinematographic benchmarks, and narrative patterns.
2. **Fact-Grounded Screenplay Architecture**: Ingests real-world excerpts and visual benchmarks via Gemini 3.7 Flash to ground creative screenplay generation.
3. **Audience Archetype & Casting Intelligence**: Evaluates character archetype resonance against genre benchmarks and voice profile recommendations.
4. **Honest Evidence & Strict Live Error Handling**: Ensures demo mode uses self-contained research fixtures with non-clickable fixture IDs, while live mode returns explicit error status on failures without silent fallback.
