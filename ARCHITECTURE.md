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

    personas: List[Dict[str, Any]]         # one entry per prompt returned by risk_prompts(),
                                            # same order — each has at least "id" and "weight"

    def risk_prompts(self, data: dict) -> list[str]:
        """Prompts for each consensus persona, tailored to this hazard."""

    def deterministic_opinion(self, persona_id: str, data: dict) -> dict:
        """Rule-based fallback for one persona, used when the LLM call fails or no key is
        configured. Same shape the Risk Agent expects from an LLM response: opinion,
        risk_rating, primary_factors, recommendation, factor_impacts."""

    def resource_formulas(self, risk_level: str, population: int) -> dict:
        """Deterministic resource calculation for this hazard."""

    knowledge_corpus_path: str              # where this hazard's source docs live

    def report_context(self, risk, resources, knowledge) -> dict:
        """Any hazard-specific framing for the report templates."""
```

Adding a new hazard means writing one file that implements this interface. No changes to
`agents/`, `orchestrator/`, or `api/`.

`personas` and `deterministic_opinion` were added after the interface was first committed —
weighted consensus and graceful LLM fallback aren't hazard-specific edge cases, every hazard
needs both, so they belong in the shared contract rather than something each hazard module
would otherwise invent independently. See the Decision log.

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
- Every answer cites its source (`According to NDMA Flood Guidelines, page 42...`) —
  this is what makes the tool traceable rather than just persuasive

**Front matter is curated out per document, not filtered heuristically.** Copyright pages,
acknowledgements, tables of contents, and glossaries extract as valid, correctly-formed text —
there's nothing for an automated filter to catch — but they dilute a deliberately small,
high-quality corpus and can surface as retrieved "guidance" (e.g. a named staff member's
acknowledgement paragraph). Each document gets one manually-verified `content_start_page` in
`rag/corpus_manifest.py`; pages before it are excluded before chunking ever runs. This is an
editorial judgment call, made once per document and recorded, not a heuristic that has to
generalize.

**Citations key on document title + page number, not the extracted `section` field.**
`section` is font-size/bold heuristic detection over real PDF content — it correctly finds true
headings most of the time, but it has no way to distinguish "a real heading" from "a signature
line, credential list, or ToC entry that happens to be formatted the same way." A citation like
*"according to the credentials line under the foreword"* is a worse failure than no section name
at all, since it's a citation that actively erodes trust rather than one that's merely plain.
Page number, once verified against the real document, is reliable; `section` is included as
optional supplementary context only, not asserted as fact.

## 8. Persistence — resolved

**Lightweight SQLite.** No auth — `AssessmentRecord` stores the risk-step result (hazard,
risk_level, final_probability, template, full risk result as JSON) after every `/assess` and
`/report` call, exposed via `GET /history`. Note the scope precisely: it logs the risk
assessment, not the final resource/citation-enriched report — `/report`'s fuller output isn't
persisted, only the risk step that feeds it. A save failure logs a warning and never fails the
actual request — a broken history write must not break a real assessment response.

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
request_id=8f2e...  stage=risk_calculated
request_id=8f2e...  stage=resources_generated
request_id=8f2e...  stage=knowledge_retrieved   (only when a knowledge_question is given)
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

- **Phase 1** ✅: Refactored the 3-persona consensus engine into `risk_agent.py`; defined
  `HazardModule`; migrated disease outbreak logic into `hazards/disease.py`
- **Phase 2** ✅: RAG pipeline + `knowledge_agent.py`, wired into the chat UI
- **Phase 3** ✅: `resource_agent.py` (deterministic) + `report_agent.py` (templated)
- **Phase 4** ✅: `hazards/flood.py` — second module, plugin design validated end to end,
  hand-verified against the real UI
- **Phase 5** ✅: request-correlated logging, SQLite assessment history — this document
- **Future**: additional hazard modules, communication/alerting agent, auth if the app ever
  needs multi-user separation

## 13. Decision log

| Decision | Choice | Rationale |
|---|---|---|
| Orchestration framework | Plain functions, not LangGraph | No branching logic yet; avoid premature complexity |
| Hazard dispatch | Dict registry, not dynamic discovery | Only 2 hazards planned; simplicity over generality |
| Explainability | Field on each agent's output, not a separate agent | Avoids a redundant LLM call with no new information |
| Report variants | One agent, template parameter | Avoids duplicating near-identical agent classes |
| Persistence | Lightweight SQLite, no auth — logs risk-step results only, not full reports | Closes the "can I see past assessments" gap in a demo without building a second project's worth of auth infrastructure the interview story doesn't need |
| Configuration | External YAML, but only for resource-formula thresholds | Lets policy numbers change without a redeploy, without building a general config system |
| Observability | Structured logs correlated by request_id | Makes a 4-agent pipeline debuggable |
| Testing | Consensus math and resource formulas extracted as pure functions | LLM output isn't unit-testable; the deterministic core is |
| Hazard module size | Single file per hazard until it exceeds ~400 lines, then split into a subpackage | Avoids premature structure |
| HazardModule interface | Amended after first commit to add `personas` and `deterministic_opinion` | Found while implementing disease.py: weighted consensus and LLM fallback aren't optional per-hazard extras, so they belong in the contract, not bolted on ad hoc — fixed while only one hazard existed |
| Front matter in RAG corpus | Per-document manual `content_start_page` manifest, not a heuristic filter | Front matter (copyright, acknowledgements, ToC) extracts as valid text — nothing for an automated filter to catch — but dilutes a deliberately small corpus; this is curation, not a bug fix |
| Citation anchor | Document title + page number, primary; extracted `section` is supplementary only | `section` heuristic can't distinguish real headings from similarly-formatted credential lines or ToC entries; a wrong citation is worse than a plain one |
| Embeddings fallback | Deterministic keyword-overlap retrieval when no API key, mirroring `deterministic_opinion()` | Without this, demo mode (which the rest of the app already supports) would silently break for the Knowledge Agent specifically |
| Contract test input generation | Hardcoded `1` for every input_schema field, not real Pydantic-constraint introspection | Works because disease and flood happen to share a 0-3 bounded-int encoding; documented in-code as a shortcut, not hidden — a hazard with a differently-shaped field (float, enum, string) will need this upgraded, not silently assumed to work |
| Keyword-fallback acronym matching | Accepted limitation, not fixed | "NDMA" vs. "National Disaster Management Authority" won't match under literal token overlap (confirmed: the real "International Cooperation" chunk on NDMA p.95 ranks below chunks using the full term). Real embeddings handle this natively; hardcoding acronym expansion into the fallback path would be solving a problem the primary path doesn't have |
