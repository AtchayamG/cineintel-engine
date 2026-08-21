# 🏗️ CineIntel Engine — Architecture Whitepaper (Parallel Track)

## 1. System Overview
**CineIntel Engine** is an autonomous film intelligence and research platform powered by **Parallel Web Systems Search & Extract MCP** and **Google Gemini 2.0**. Before production greenlights, autonomous agents crawl real-world entertainment datasets, audience sentiment, and cinematography reference LUTs to ground movie creation in cultural and commercial reality.

```mermaid
graph TD
    User([🎬 Filmmaker / Development Exec]) --> UI[🖥️ Interactive Web UI<br/>Premise & Genre Input]
    UI --> ParallelAgent[🌐 TrendAnalyst & GroundedWriter Agent]
    ParallelAgent --> ParallelMCP[🔍 Parallel Search MCP Server<br/>(mcp-parallel-web)]
    ParallelMCP --> WebResults[(Live Open Web Evidence<br/>Titles, URLs, Snippets)]
    ParallelAgent --> GeminiAgent[🤖 Gemini 2.0 Flash Grounding Model]
    WebResults --> GeminiAgent
    GeminiAgent --> GroundedTreatment[📄 Fact-Grounded Screenplay & Viability Critique]
    GroundedTreatment --> UI
```

---

## 2. End-to-End Execution Flow
1. **Premise Input**: User provides a high-level creative brief.
2. **Parallel Search Crawl**: Calls `parallel_search_web` to retrieve relevant industry benchmarks and cinematography references.
3. **Source Evidence Preservation**: Retains verifiable source titles, URLs, and snippets without fabrication.
4. **Gemini 2.0 Synthesis**: Deconstructs the research into a grounded concept, recommended scene beats, and an explicit uncertainty rating.
5. **UI Display**: Renders source evidence cards, grounded screenplay treatment, and measured request latency.
