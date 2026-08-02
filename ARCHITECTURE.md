# SentinelAI — Architecture

*Modular multi-agent disaster intelligence platform. This document is the frozen design.
Changes to this architecture should be deliberate and recorded in the Decision Log at the
bottom, not made ad hoc while writing feature code.*

## 1. Core idea

Two things are true about this system, and the whole design follows from them:

1. **The reasoning pipeline is the same regardless of hazard type.** Every hazard needs a risk
   assessment, a resource estimate, grounded guidance, and a report. That pipeline is written
   once, in the agent layer.
2. **What differs per hazard is data and configuration, not logic.** Disease outbreak and flood
   don't need different code paths — they need different input schemas, prompts, resource
   formulas, and knowledge corpora. That's the hazard plugin layer.

Everything below exists to keep those two layers from bleeding into each other.

## 2. Request flow

```
Dashboard (frontend)
    │
    ▼
API layer            — api/routes.py
    │  validates request, calls orchestrator, returns response
    │  contains NO business logic
    ▼
Orchestrator          — orchestrator/workflow.py
    │  decides agent execution order, passes output of one agent into the next
    ▼
Risk Agent  →  Resource Agent  →  Knowledge Agent  →  Report Agent
    │               │                    │                  │
    └───────── each agent calls the ACTIVE hazard module for its
               hazard-specific data (prompts, formulas, corpus path)
                                                              │
                                                              ▼
                                                          Response
```

## 3. Folder structure

```
server/
  api/
    routes.py            # HTTP layer only
  orchestrator/
    workflow.py           # sequences agent calls; swap-in point for LangGraph later
  agents/
    risk_agent.py          # 3-persona weighted consensus — calls LLM personas, delegates math to consensus.py
    consensus.py            # pure function: persona outputs -> weighted risk result (no I/O, fully unit-testable)
    resource_agent.py       # deterministic, rule-based — not an LLM call
    knowledge_agent.py       # RAG, cited retrieval
    report_agent.py           # templated: officer / citizen / executive
  hazards/
    base.py                    # HazardModule interface — see section 5
    disease.py                  # first implemented module
    flood.py                     # second module, validates the interface
  rag/
    loader.py                     # pulls source PDFs
    chunker.py                     # chunks with overlap, keeps section metadata
    embeddings.py                   # embedding generation
    retriever.py                     # retrieval + citation attachment
  services/
    weather.py                        # Open-Meteo integration
    prediction.py                      # shared numeric/statistical helpers
  db/
    models.py                           # SQLAlchemy models (persistence, if used)
    database.py                          # connection/session setup
  schemas/
    request.py                            # Pydantic request models
    response.py                            # Pydantic response models
  config/
    disease.yaml                            # resource-formula thresholds — data, not hardcoded constants
    flood.yaml                               # same, for flood
  main.py                                   # app entrypoint, wires everything together
tests/
  test_risk.py                                # consensus.py against mocked persona outputs
  test_resources.py                            # resource formulas against known risk/population inputs
  test_hazards.py                               # every HazardModule satisfies the interface contract
  test_api.py                                    # route-level integration tests
```

**Why `db/` and `schemas/` are separate:** `schemas/` describes the shape of an API
request/response. `db/` describes the shape of a stored row. These will diverge the moment you
add a field that's stored but never returned (or vice versa) — keeping them separate from day
one avoids a painful untangle later.

## 4. Component responsibilities

| Component | Responsibility | Does NOT do |
|---|---|---|
| `api/routes.py` | Validate input, call orchestrator, serialize output | Business logic, agent sequencing |
| `orchestrator/workflow.py` | Decide agent order, pass data between agents | HTTP concerns, hazard-specific logic |
| `risk_agent.py` | Run 3-persona consensus, return risk level + confidence + per-persona reasoning | Resource math, document retrieval |
| `resource_agent.py` | Apply the active hazard's resource formulas to risk + population | LLM calls |
| `knowledge_agent.py` | Retrieve from the active hazard's knowledge corpus, answer with citations | Risk scoring |
| `report_agent.py` | Assemble risk + resource + knowledge output into officer/citizen/executive templates | Original analysis — it aggregates, not generates new findings |
| `hazards/<name>.py` | Supply input schema, persona prompts, resource formulas, knowledge corpus path for one hazard | Any of the above agent logic itself |

## 5. HazardModule interface

This is the actual engineering artifact behind "the hazard layer is pluggable" — not just a
diagram, a real contract every hazard module implements:

```python
class HazardModule(Protocol):
    name: str
    input_schema: Type[BaseModel]          # what data this hazard needs

    def risk_prompts(self, data: dict) -> list[str]:
        """Prompts for each of the 3 consensus personas, tailored to this hazard."""

    def resource_formulas(self, risk_level: str, population: int) -> dict:
        """Deterministic resource calculation for this hazard."""

    knowledge_corpus_path: str              # where this hazard's source docs live

    def report_context(self, risk, resources, knowledge) -> dict:
        """Any hazard-specific framing for the report templates."""
```

Adding a new hazard means writing one file that implements this interface. No changes to
`agents/`, `orchestrator/`, or `api/`.

## 6. Explainability (cross-cutting, not a separate agent)

There is no standalone "explainability agent." Every agent's output includes a
`reasoning: list[str]` field:

- Risk Agent: each persona's stated reasoning, plus the consensus weighting
- Resource Agent: which rule/threshold produced each number (free, since it's deterministic)
- Knowledge Agent: the source document + section for every claim

The Report Agent assembles these into the human-readable "why" section. This gets the same
user-facing result as a dedicated agent, without an LLM call whose only job is re-explaining
what already exists elsewhere.

## 7. RAG grounding

- 10–20 curated source documents (WHO / CDC / NDMA), not a bulk corpus
- Chunk with overlap, preserve document + section metadata on every chunk
- Every answer cites its source (`According to NDMA Flood Guidelines, Section 4.2...`) —
  this is what makes the tool traceable rather than just persuasive

## 8. Persistence — open decision

Two options, pick one before writing `db/`:

- **Lightweight**: SQLite, no auth, just stores past assessments/reports for the dashboard's
  history view. Minimal build time, still demonstrates persistence.
- **Full**: PostgreSQL + auth, per the original PRD. More build time, demonstrates more, but
  isn't required to tell a strong architecture story.

Default recommendation: lightweight, unless auth/persistence is itself a skill you want to
showcase.

## 9. Orchestration implementation

Plain Python functions in `orchestrator/workflow.py` for now:

```python
def run_assessment(hazard: str, data: dict):
    module = HAZARDS[hazard]
    risk = risk_agent.run(module, data)
    resources = resource_agent.run(module, risk)
    knowledge = knowledge_agent.run(module, risk)
    return report_agent.run(risk, resources, knowledge)
```

Do not adopt LangGraph until the pipeline has real branching (e.g. "if RAG retrieval confidence
is low, escalate before generating a report"). Introducing a graph framework for a linear
sequence adds complexity without adding capability.

## 10. Observability

Add structured logging correlated by a per-request ID, generated once in `api/routes.py` and
passed through the orchestrator to every agent call:

```
request_id=8f2e...  stage=weather_fetched
request_id=8f2e...  stage=risk_calculated   risk=HIGH confidence=0.91
request_id=8f2e...  stage=resources_generated
request_id=8f2e...  stage=report_created
```

This is what makes a request traceable end to end through 4+ agent calls when something goes
wrong — plain `print()` statements won't cut it once the pipeline has this many stages.

## 11. Testing strategy

The deterministic parts of this system are only testable if they're structurally separated from
the parts that call an LLM:

- `consensus.py` (weighted-consensus math) is a **pure function** — given a list of persona
  outputs, it returns a risk result, with no LLM call inside it. This is what makes `test_risk.py`
  possible without mocking an API or asserting on non-deterministic text.
- `resource_agent.py` formulas are pure functions of `(risk_level, population)` —
  straightforward to test against known inputs.
- `hazards/*.py` — test that every hazard module actually implements the `HazardModule`
  interface (a contract test, run once per hazard, catches a missing method immediately instead
  of at runtime).
- `api/` — integration tests with the agents mocked, checking routing/validation only.

The LLM-calling parts themselves (persona prompts, RAG retrieval quality) aren't unit-tested in
the traditional sense — that's normal, and worth saying explicitly in the README so it doesn't
read as an oversight.

## 12. Roadmap

- **Phase 1**: Refactor existing 3-persona consensus engine into `risk_agent.py`; define
  `HazardModule`; migrate disease outbreak logic into `hazards/disease.py`
- **Phase 2**: RAG pipeline + `knowledge_agent.py`, wire up existing chat UI component
- **Phase 3**: `resource_agent.py` (deterministic) + `report_agent.py` (templated)
- **Phase 4**: `hazards/flood.py` — second module, validates the plugin design end to end
- **Future**: additional hazard modules, communication/alerting agent, persistence upgrade

## 13. Decision log

| Decision | Choice | Rationale |
|---|---|---|
| Orchestration framework | Plain functions, not LangGraph | No branching logic yet; avoid premature complexity |
| Hazard dispatch | Dict registry, not dynamic discovery | Only 2 hazards planned; simplicity over generality |
| Explainability | Field on each agent's output, not a separate agent | Avoids a redundant LLM call with no new information |
| Report variants | One agent, template parameter | Avoids duplicating near-identical agent classes |
| Persistence | TBD — see section 8 | Depends on whether auth/DB is a skill to showcase |
| Configuration | External YAML, but only for resource-formula thresholds | Lets policy numbers change without a redeploy, without building a general config system |
| Observability | Structured logs correlated by request_id | Makes a 4-agent pipeline debuggable |
| Testing | Consensus math and resource formulas extracted as pure functions | LLM output isn't unit-testable; the deterministic core is |
| Hazard module size | Single file per hazard until it exceeds ~400 lines, then split into a subpackage | Avoids premature structure |
