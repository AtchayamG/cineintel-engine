# 🎥 3-Minute Demo Video Script: CineIntel Engine (Parallel Track)

- **[0:00 - 0:45] The Problem**: AI screenwriting often hallucinates unrealistic tropes and lacks grounding in real-world open-web research and cinematography reference benchmarks.
- **[0:45 - 1:30] Demo Mode with Fixtures**: Open `http://localhost:8002/`. Ensure the UI explicitly shows "DEMO FIXTURES" mode. Input a cyberpunk detective premise. Trigger the research pipeline. Emphasize that the returned cards are deterministic research fixtures for stable demonstrations, not live sources.
- **[1:30 - 2:15] Gemini 2.5 Fact-Grounded Synthesis**: Show Gemini 2.5 Flash distilling the fixture evidence into a grounded title, scene beats, and a clear market viability critique with an explicit uncertainty rating.
- **[2:15 - 3:00] Live Code Architecture**: Switch to the codebase to show the official `parallel-web` Python SDK code path. Highlight the request structure (`x-api-key`, `objective`, `search_queries`) that executes when in live mode, demonstrating the verifiable integration without needing a live key during the recording.
