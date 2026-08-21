# 🤝 Agent Handoff Document: Track 3 (Parallel Track)

**Target Hackathon:** Google Cloud "Agentic Cinema: The Blockbuster Hackathon" (Devpost)  
**Assigned Category:** **Parallel Track** ($7,500 1st Place)  
**Application Name:** **`CineIntel Engine`**  
**Submitting Status:** ✅ READY FOR SUBMISSION  

---

## 1. Executive Summary & Purpose
**CineIntel Engine** is an autonomous film intelligence and research platform powered by **Parallel Web Systems Search & Extract MCP** and **Gemini 2.0**. Before studio greenlights occur, autonomous agents crawl entertainment news, box office comps, audience sentiment, and cinematography reference LUTs to ground movie creation in real-world cultural and commercial data.

---

## 2. Devpost Submission Fields (Copy-Paste Ready)
- **Project Title:** `CineIntel Engine: Real-Time Web Grounding, Viral Film Trend Forecasting & Autonomous Script Research Agent`
- **Elevator Pitch:** `An autonomous film intelligence and research engine powered by Parallel Web Systems MCP and Gemini 2.0 that crawls live web datasets, box office comps, and audience sentiment to generate culturally grounded screenplays optimized for commercial and critical resonance.`
- **Partner Track:** `Parallel Track`
- **License:** `Apache 2.0` (Included at root)

---

## 3. Codebase Architecture & File Map
```
Track3_Parallel_CineIntel_Engine/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── trend_analyst_agent.py     # Live market viability & viral trope researcher
│   │   │   ├── grounded_writer_agent.py   # Fact-grounded screenplay generation
│   │   │   └── casting_intel_agent.py     # Demographic appeal & casting affinity
│   │   ├── mcp/
│   │   │   └── parallel_mcp_server.py     # MCP tools (parallel_search_web, parallel_extract_url)
│   │   ├── services/
│   │   │   └── parallel_service.py        # Parallel Web HTTP client & grounding
│   │   ├── routes/intel_routes.py         # API endpoints (/intel/analyze/trends, /intel/script/grounded)
│   │   ├── config.py & main.py            # Configuration & FastAPI entrypoint
│   │   └── run_backend.py                 # Runner script
│   └── tests/test_parallel_intel.py       # 4 Automated pytest suites (100% Passed)
├── docs/
│   ├── DEVPOST_SUBMISSION.md              # Full Devpost submission details
│   └── AGENT_HANDOFF.md                   # This handoff guide
├── LICENSE                                # Apache 2.0
└── README.md                              # Main documentation
```

---

## 4. Verification & Testing Commands for Codex

### A. Run Automated Backend Tests
```bash
cd "d:\Work\Gemini\Hackathon\Agentic Cinema\Track3_Parallel_CineIntel_Engine\backend"
python -m pytest tests/ -v
# Output expectation: 4 passed in ~0.20s
```

### B. Run Backend Server
```bash
python run_backend.py
# Server starts on http://localhost:8002 (Swagger docs at /docs)
```

### C. Test Sample Trend Analysis API Call
```bash
curl -X POST "http://localhost:8002/api/v1/intel/analyze/trends" -H "Content-Type: application/json" -d "{\"premise\": \"A rogue cyber detective\", \"genre\": \"Cyberpunk Noir\"}"
```

---

## 5. Hackathon Judging Rubric Alignment Checklist
- [x] **Technological Implementation (25%)**: Live Parallel MCP search and URL extraction pipelines integrated with Gemini 2.0 multimodal reasoning.
- [x] **Design (25%)**: Structured data models for trends, tropes, and demographic affinity scores.
- [x] **Potential Impact (25%)**: Replaces subjective script greenlighting with data-backed audience intelligence.
- [x] **Quality of the Idea (25%)**: First AI script development engine grounded in live open-web datasets.
