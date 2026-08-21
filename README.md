<div align="center">

# 🌐 CineIntel Engine
### Real-Time Web Grounding, Viral Film Trend Forecasting & Autonomous Script Research Agent
**Built for the Parallel Track — Google Cloud "Agentic Cinema: The Blockbuster Hackathon"**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Parallel MCP](https://img.shields.io/badge/Parallel%20Web-MCP%20Server-00F0FF)](https://parallel.ai)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-2.0%20Flash-4285F4?logo=google&logoColor=white)](https://cloud.google.com/vertex-ai)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)

</div>

---

## 🌟 Overview
**CineIntel Engine** is an autonomous film market intelligence and fact-grounded screenplay generation engine powered by **Parallel Web Systems Search & Extract MCP** and **Gemini 2.0**. Before production begins, autonomous agents crawl entertainment news, box office comps, audience sentiment, and cinematography reference LUTs to ground movie creation in real-world cultural and commercial data.

---

## 🚀 Key Features

1. **🔍 Live Open-Web Trend Extraction**:
   - Uses Parallel Search MCP (`parallel_search_web`) to discover high-performing narrative tropes and audience sentiment.
2. **✍️ Fact-Grounded Screenwriting**:
   - Employs Parallel Extract MCP (`parallel_extract_url`) to extract scientific concepts, historical context, and reference lookups directly into screenplay scenes.
3. **🎭 Casting & Persona Match Intelligence**:
   - Evaluates archetype resonance and audience appeal across target demographics.
4. **🤖 Specialized Gemini 2.0 Agent Crew**:
   - **TrendAnalystAgent**: Scans viral trends and competitor ROI.
   - **GroundedWriterAgent**: Converts raw research into grounded dialogue and sluglines.
   - **CastingIntelAgent**: Optimizes character appeal.

---

## ⚡ Quickstart

```bash
cd backend
pip install -r requirements.txt
python run_backend.py
```
*API docs at `http://localhost:8002/docs`.*

---

## 🧪 Testing

```bash
cd backend
pytest tests/ -v
```

---

## 📄 License
Licensed under the **[Apache License 2.0](LICENSE)**.
