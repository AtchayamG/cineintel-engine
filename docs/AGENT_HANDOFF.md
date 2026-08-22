# 🤝 Agent Handoff Document: Track 3 (Parallel Track)

**Target Hackathon:** Google Cloud "Agentic Cinema: The Blockbuster Hackathon" (Devpost)  
**Assigned Category:** **Parallel Track** ($7,500 1st Place)  
**Application Name:** **`CineIntel Engine`**  
**Submitting Status:** ✅ READY FOR SUBMISSION  

---

## 1. Executive Summary & Purpose
**CineIntel Engine** is an autonomous film research and screenplay grounding platform that uses official Parallel Search and Gemini integration paths. Before production greenlights occur, autonomous agents ground movie creation in evidence and explicit uncertainty bounds. The default public evaluator uses deterministic fixtures; independent authenticated smoke evidence proves both live services.

---

## 2. Devpost Submission Fields (Copy-Paste Ready)
- **Project Title:** `CineIntel Engine: Real-Time Web Grounding, Film Trend Research & Autonomous Script Doctor`
- **Elevator Pitch:** `An autonomous film intelligence engine that uses official Parallel Search and Gemini to turn a premise into a source-aware treatment, uncertainty critique, and actionable scene beats.`
- **Partner Track:** `Parallel Track`
- **License:** `MIT` (Included at root)

---

## 3. Codebase Architecture & File Map
```
Track3_Parallel_CineIntel_Engine/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── trend_analyst_agent.py     # Open-web trend evidence & trope researcher
│   │   │   ├── grounded_writer_agent.py   # Fact-grounded screenplay generation
│   │   │   └── casting_intel_agent.py     # Audience archetype & casting affinity
│   │   ├── mcp/
│   │   │   └── parallel_mcp_server.py     # MCP tool adapter for agents (parallel_search_web, parallel_extract_url)
│   │   ├── services/
│   │   │   ├── parallel_service.py        # Official Parallel Search SDK/API integration (parallel-web)
│   │   │   └── gemini_service.py          # Google GenAI SDK & Gemini 3.7 Flash synthesis
│   │   ├── routes/intel_routes.py         # API endpoints (/intel/analyze/trends, /intel/script/grounded)
│   │   ├── static/index.html              # self-contained judge Web UI (no external CDNs, embedded favicon)
│   │   ├── config.py & main.py            # Configuration & FastAPI entrypoint
│   │   └── run_backend.py                 # Server runner script
│   └── tests/test_parallel_intel.py       # 8 Automated pytest suites (100% Passed)
├── docs/
│   ├── DEVPOST_SUBMISSION.md              # Full Devpost submission details
│   ├── AGENT_HANDOFF.md                   # This handoff guide
│   ├── AGY_HANDOFF.md                     # Technical handoff document
│   ├── ARCHITECTURE.md                    # Architecture whitepaper
│   ├── SUBMISSION_EVIDENCE.md             # Evidence matrix & verification
│   └── VIDEO_DEMO_SCRIPT.md               # 3-minute video demo script
├── LICENSE                                # MIT
└── README.md                              # Main documentation
```

---

## 4. Verification & Testing Commands

### A. Run Automated Backend Tests
```bash
cd backend
python -m pytest -v
# Output expectation: 8 passed in ~0.45s
```

### B. Run Backend Server
```bash
python run_backend.py
# Server starts on http://localhost:8002 (Swagger docs at /docs, Web UI at /)
```

### C. Test Grounded Script API Call
```bash
curl -X POST "http://localhost:8002/api/v1/intel/script/grounded" -H "Content-Type: application/json" -d "{\"premise\": \"A rogue cyber detective\", \"genre\": \"Cyberpunk Noir\"}"
```

---

## 5. Hackathon Judging Rubric Alignment Checklist
- [x] **Technological Implementation (25%)**: Official Parallel Search API / SDK (`parallel-web`) integration with `x-api-key` header and `objective`/`search_queries` request structure, integrated with Gemini 3.7 Flash reasoning.
- [x] **Design (25%)**: self-contained judge UI with no external CDN dependencies, embedded favicon, and clean source card rendering.
- [x] **Potential Impact (25%)**: Replaces subjective greenlighting with evidence-grounded research and explicit uncertainty bounds.
- [x] **Quality of the Idea (25%)**: Groundbreaking AI script development engine backed by open-web evidence.
