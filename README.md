# SentinelAI: Disaster Intelligence Platform

![Epidemic.Intel Dashboard](https://raw.githubusercontent.com/placeholder-path/screenshot.png) *(Replace with actual screenshot)*

## 📌 Problem Statement
Disaster management and outbreak prediction often rely on rigid, single-model risk assessments that fail to capture the nuance of real-world emergencies. When an alert fires, decision-makers don't just need a black-box "risk score"—they need to know *why* the score is high, what resources are required, and what established guidelines recommend. 

SentinelAI solves this by orchestrating a team of specialized AI agents that debate telemetry, calculate necessary resources, and ground their recommendations in curated authoritative documents, providing a transparent, multi-faceted intelligence briefing.

---

## 🏗 Architecture
SentinelAI is built as a modular multi-agent platform. The core reasoning pipeline is written once, while hazard-specific logic (e.g., disease vs. flood) is injected via a strict plugin system.

```text
API layer (api/routes.py)
    │
    ▼
Orchestrator (orchestrator/workflow.py)
    │
    ▼
Risk Agent  →  Resource Agent  →  Knowledge Agent  →  Report Agent
    │               │                    │                  │
    └───────── each agent calls the ACTIVE hazard module for its
               hazard-specific data (prompts, formulas, corpus path)
```

For a complete breakdown of the project structure, component responsibilities, testing strategies, and the design decision log, please refer to the comprehensive **[Architecture Document](ARCHITECTURE.md)**.

---

## 🤖 Agent Workflow
The orchestrator sequences four distinct agents to build a complete intelligence report:

1. **Risk Agent**: Uses a 3-persona weighted consensus model. Instead of a single LLM call, it simulates independent experts (e.g., an Epidemiologist and an Environmental Scientist) who evaluate the same telemetry. A deterministic math engine then calculates final confidence and risk levels based on their agreement.
2. **Resource Agent**: A purely deterministic rules-engine that calculates required material resources (e.g., vaccines, sandbags, pumps) based on the computed risk level and affected population.
3. **Knowledge Agent**: Queries a hazard-specific corpus of authoritative guidelines to retrieve contextual advice and historical precedence.
4. **Report Agent**: Synthesizes the outputs of the previous three agents into targeted, human-readable templates tailored to specific audiences (Citizen, Officer, Executive).

---

## 🧩 Plugin Architecture
The system strictly separates reasoning logic from hazard-specific data to prevent codebase entanglement. Adding a new hazard (like Wildfires or Chemical Spills) does not require modifying the orchestrator or agents.

Instead, developers implement a single `HazardModule` protocol. This plugin supplies:
- The `input_schema` (what telemetry the hazard requires)
- The persona prompts and weightings for the Risk Agent
- The resource calculation formulas
- The path to the hazard's knowledge corpus
- A deterministic fallback opinion if the LLM fails

---

## 🧠 RAG Pipeline
SentinelAI features a precision Retrieval-Augmented Generation (RAG) pipeline built for high-stakes explainability:
- **Curated Corpora**: Uses small, highly authoritative datasets per hazard (e.g., WHO, CDC, NDMA manuals) rather than bulk scraping.
- **Strict Citations**: Every generated claim is anchored to a specific source document and verified page number.
- **Clean Extraction**: Front matter (copyrights, ToCs) is manually stripped via a `content_start_page` manifest to prevent heuristic dilution and ensure only actionable guidelines are retrieved.

---

## 🚀 Features
- **Explainable Consensus**: Understand exactly what drove a risk score by viewing expert disagreement indexes and factor weightings.
- **Live Telemetry Integration**: Auto-fetches live weather and environmental data via the Open-Meteo API based on geolocation.
- **Scenario Comparison (Delta View)**: Modify parameters on the fly to quantify the exact impact of hypothetical interventions.
- **Traceable Observability**: End-to-end request tracing across the multi-agent pipeline using injected `request_id` context logging.
- **Lightweight Persistence**: Built-in SQLite database automatically logs the risk-step results of all assessments for historical auditing.
- **Graceful Degradation**: Built-in deterministic fallbacks ensure the app functions even when API keys are missing or rate-limited.

---

## 🛣 Roadmap
- ✅ **Phase 1**: Consensus engine refactor and `HazardModule` plugin architecture definition.
- ✅ **Phase 2**: Precision RAG pipeline and UI integration.
- ✅ **Phase 3**: Deterministic Resource Agent and templated Report Agent.
- ✅ **Phase 4**: Multi-hazard validation (successfully integrated the Flood plugin).
- ✅ **Phase 5**: Observability logging and lightweight SQLite assessment history.
- ⏳ **Future**: Additional hazard modules (Earthquake, Wildfire), automated communication/alerting agents, and multi-user authentication.

---

## 🛠️ Getting Started

### Prerequisites
- Node.js (v18+)
- Python (v3.11+)
- A **Google Gemini API Key** (Get one at [Google AI Studio](https://aistudio.google.com/))

### 1. Clone & Setup
```bash
git clone https://github.com/your-username/epidemic-intel.git
cd epidemic-intel

# Create environment file
echo "GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE" > .env
```

### 2. Install Dependencies
```bash
npm install                     # Frontend dependencies
pip install -r requirements.txt # Backend dependencies
```

### 3. Run the Application
You will need two terminals running simultaneously:

**Terminal 1 (Backend):**
```bash
python -m uvicorn server.main:app --reload --port 8000
```

**Terminal 2 (Frontend):**
```bash
npm run dev
```
Open your browser and navigate to `http://localhost:3000`.
