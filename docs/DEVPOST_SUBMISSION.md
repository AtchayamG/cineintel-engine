# 🎬 Devpost Submission: CineIntel Engine (Parallel Track)

## Project Name
**CineIntel Engine: Real-Time Web Grounding, Film Trend Research & Autonomous Script Doctor**

## Elevator Pitch
An autonomous film intelligence and research engine that uses Parallel Search and Gemini to generate source-aware screenplays with explicit uncertainty critiques. The public evaluator now runs Gemini 3.7 Flash live through Vertex AI; its Parallel provider remains transparently labeled demo/unconfigured, with separate authenticated Parallel Search evidence in `docs/PARALLEL_LIVE_PROOF.md`.

## Selected Track
**Parallel Track** ($7,500 1st Place)

## Judge Links
- **Live Application:** https://cineintel-engine.vercel.app/
- **Public Repository:** https://github.com/AtchayamG/cineintel-engine
- **Demo Video:** https://youtu.be/Pc5cY7IAVMA
- **Runtime Note:** The public evaluator runs Gemini 3.7 Flash live through Vertex AI. Its Parallel provider remains explicitly labeled demo/unconfigured. `docs/PARALLEL_LIVE_PROOF.md` records a successful authenticated Parallel Search call without storing the credential.

## What It Does
1. **Live-Mode Open-Web Market Research**: Uses Parallel Search (`parallel-web`) to extract trending tropes, cinematographic benchmarks, and narrative patterns.
2. **Fact-Grounded Screenplay Architecture**: Ingests real-world excerpts and visual benchmarks via Gemini 3.7 Flash to ground creative screenplay generation.
3. **Audience Archetype & Casting Intelligence**: Evaluates character archetype resonance against genre benchmarks and voice profile recommendations.
4. **Honest Evidence & Strict Live Error Handling**: Ensures demo mode uses self-contained research fixtures with non-clickable fixture IDs, while live mode returns explicit error status on failures without silent fallback.
