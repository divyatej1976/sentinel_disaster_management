# Sentinel v2 — Literature & Technical Synthesis

**Status:** Research in progress  
**Date:** 2026-08-14  
**Decision:** Use this synthesis to constrain Sentinel's technical model before architecture is frozen.

## 1. Executive conclusion

The research does **not** support making Sentinel primarily a prediction model, a generic chatbot, or an autonomous emergency agent.

The strongest technical direction is a **tool-grounded, geospatial, evidence-aware human-AI decision-support system** that combines deterministic analytical services with LLM/VLM reasoning.

The key design principle is:

> **AI should synthesize, reason, plan and explain; deterministic systems should measure, calculate, route, validate and enforce constraints.**

This conclusion is reinforced by three independent lines of evidence:

1. Current international guidance says AI should enhance multi-hazard early-warning systems while retaining human oversight for life-safety decisions and relying on strong observational infrastructure and interoperable architecture.
2. Human-AI disaster research consistently identifies decision support, task/resource coordination, trust/transparency and simulation as major application patterns, while interpretability, interoperability and scalability remain difficult.
3. New 2026 benchmarks show that realistic geospatial/disaster agent tasks remain difficult for current LLMs and that deterministic ground-truth evaluation is essential.

## 2. Research stream: AI in multi-hazard early warning

The July 2026 UNDRR/WMO/ITU/IFRC report on leveraging AI for multi-hazard early warning is highly relevant. It evaluates AI across all four early-warning pillars and explicitly describes AI as an enabling technology rather than a replacement for institutions and human expertise.

The report highlights:

- robust observation infrastructure using ground networks, satellites and in-situ sensors;
- governance, human oversight and accountability for life-safety decisions;
- human-centred and equity-driven design;
- multilingual and low-connectivity compatibility;
- modular/interoperable architectures;
- feedback loops across risk models, forecasts, communication and preparedness;
- the need to address existing system gaps rather than adding AI for its own sake.

**Sentinel implication:**

Sentinel should be an interoperable intelligence/decision layer and should consume authoritative warning/observation systems rather than pretending to replace them.

## 3. Research stream: human-AI disaster decision making

A 2025 systematic review of 51 peer-reviewed studies identifies four major Human-AI use patterns:

1. Human-AI decision-support systems
2. Task and resource coordination
3. Trust and transparency
4. Simulation and training

The review reports benefits in situational awareness and complex decision-making while identifying scalability, interpretability and interoperability as persistent challenges.

**Sentinel implication:**

The product should be designed around human decisions and workflows, with explicit evidence, uncertainty and approval. This is a better research position than claiming full autonomy.

## 4. Research stream: realistic disaster agents

DORA (2026) evaluates disaster-response agents on realistic multi-step tasks including disaster perception, spatial reasoning, road-network reasoning, evacuation/rescue planning, temporal evolution and multimodal reporting. Its evaluation highlights failures around tool selection, argument grounding and long-horizon compositional reasoning.

**Sentinel implication:**

Do not create a giant unconstrained agent. Use explicit tools with typed inputs/outputs, deterministic validation, bounded workflows and intermediate state.

Recommended agent boundary:

```text
LLM/VLM
 ├── interpret observations
 ├── choose relevant tools
 ├── synthesize evidence
 ├── generate candidate plans
 └── explain recommendations

Deterministic services
 ├── GIS operations
 ├── exposure calculations
 ├── routing
 ├── resource arithmetic/optimization
 ├── temporal aggregation
 ├── constraint validation
 └── policy/SOP checks
```

## 5. Research stream: GIS agents

GISAgentBench (August 2026) is particularly important because it uses 349 practitioner-sourced multi-step GIS tasks, real public data, executable reference trajectories and exact ground-truth output files. The best evaluated agent completed only 32.7% of tasks under strict tolerance-aware scoring.

This is a strong warning against allowing an LLM to perform unverified spatial analysis.

**Sentinel implication:**

Every important geospatial operation should have deterministic tooling and a machine-checkable output. The LLM should request/compose spatial operations, not invent their results.

Potential tool contract examples:

```text
get_affected_population(hazard_geometry)
intersect_infrastructure(hazard_geometry)
find_nearest_shelters(origin, constraints)
calculate_route(origin, destination, road_graph)
calculate_exposure(hazard, population, infrastructure)
```

## 6. Research stream: multimodal disaster geolocation

DisasterTD (2026) demonstrates a useful pattern for noisy disaster imagery: use multimodal reasoning to generate candidate locations, then verify them using cross-view evidence from remote sensing/street imagery.

**Sentinel implication:**

Multimodal AI should not be treated as authoritative from a single image. Use cross-source verification when a visual observation changes an operational decision.

Potential workflow:

```text
Image/social report
      ↓
VLM extracts clues
      ↓
Candidate locations
      ↓
GIS / remote-sensing verification
      ↓
Confidence + provenance
      ↓
Operational impact
```

## 7. Research stream: geospatial foundation models

Recent comparison work on TerraMind and THOR shows that geospatial foundation-model performance depends substantially on architecture, patch size, decoder design, modality and dataset characteristics rather than there being one universally superior model.

**Sentinel implication:**

Do not select a geospatial foundation model merely because it tops a general leaderboard. Select models by hazard/use case, available imagery, compute budget and measurable downstream performance.

For the initial product, using established remote-sensing APIs/models may be more defensible than training a new foundation model.

## 8. Research stream: VLM + human/UAV coordination

Recent 2026 systems-engineering work explores VLMs as coordination agents in human-UAV disaster response, combining natural-language interaction, mission-level coordination, task allocation and human-factors evaluation.

**Sentinel implication:**

The future architecture can expose a mission/task interface, but direct physical-actuator control should be outside the first production scope. Sentinel should initially produce validated plans and tasks for human or external mission-control systems.

## 9. Technical pattern that emerges

Across the literature, the strongest common architecture is:

```text
             MULTI-SOURCE WORLD STATE
                      ↓
             DATA NORMALIZATION
                      ↓
              SITUATION MODEL
                      ↓
          ┌───────────┴───────────┐
          ↓                       ↓
   Deterministic analytics      AI reasoning
          ↓                       ↓
   Exposure / GIS / route    Synthesis / planning
   resource / validation     / explanation
          └───────────┬───────────┘
                      ↓
              OPTION GENERATION
                      ↓
          CONSTRAINT + SAFETY CHECK
                      ↓
             EVIDENCE + UNCERTAINTY
                      ↓
               HUMAN APPROVAL
                      ↓
                OPERATIONAL PLAN
                      ↓
                 FEEDBACK LOOP
```

## 10. What Sentinel should build

### P0

- Multi-source situation model
- Map-first geospatial operational picture
- Deterministic impact/exposure engine
- Tool-grounded AI reasoning
- Evidence/provenance for recommendations
- Uncertainty and confidence representation
- Human approve/modify/reject workflow
- Deterministic resource and routing services
- Scenario/what-if comparison
- Evaluation harness with ground truth

### P1

- Satellite/SAR integration
- Multimodal field/image evidence
- Temporal change detection
- Cross-source verification
- After-action learning
- Low-connectivity field experience
- Additional hazards

### P2

- UAV/robot coordination
- More advanced geospatial foundation models
- Predictive digital-twin style simulation
- Autonomous task execution

## 11. What Sentinel should explicitly avoid

### Avoid: LLM-only GIS
Current benchmark results show realistic GIS reasoning is not reliable enough to treat unconstrained LLM spatial output as authoritative.

### Avoid: fully autonomous life-safety decisions
Current international guidance explicitly emphasizes human oversight and accountability.

### Avoid: giant multi-agent graphs
More agents do not automatically create more intelligence. Agent boundaries should correspond to distinct capabilities, data ownership or decision responsibilities.

### Avoid: training a new foundation model initially
The available evidence favors use-case-specific evaluation and strong data/tool grounding before expensive model training.

### Avoid: generic multimodal demo
Image captioning or a chatbot over satellite images is not enough. A visual input must feed a validated operational workflow.

## 12. Evaluation implications

Sentinel needs a layered evaluation strategy.

### AI quality
- groundedness
- citation correctness
- tool selection accuracy
- plan validity
- uncertainty calibration

### Geospatial quality
- exact/tolerance-aware output comparison
- exposure estimation error
- route feasibility
- affected-area intersection correctness

### Operational quality
- time to useful situation update
- resource allocation quality
- plan completeness
- decision-maker workload
- human override rate

### Reliability
- stale data detection
- conflicting source handling
- tool failure recovery
- hallucination containment
- reproducibility

The evaluation system itself should be a first-class product component, not an afterthought.

## 13. Key technical decisions emerging from research

| Decision | Current recommendation | Confidence |
|---|---|---:|
| Core AI role | Reasoning/planning/synthesis | High |
| Core deterministic role | GIS/routing/resources/validation | High |
| Agent architecture | Small bounded agents/tools | High |
| Map | First-class operational UI | High |
| RAG | Evidence/provenance layer | High |
| Human approval | Required for consequential actions | High |
| Satellite | Integrate selectively | Medium-high |
| Foundation model training | Defer | High |
| Autonomous action | Defer/avoid in first release | High |
| Digital twin | Research later | Medium |
| UAV integration | Future extension | Medium |

## 14. Research gap worth pursuing

A credible Sentinel research contribution could be:

> **Can a tool-grounded, evidence-aware AI system improve the speed and quality of disaster operational decision-making while preserving deterministic spatial correctness and human authority?**

This is more defensible than claiming to invent a new disaster predictor.

Potential experimental comparison:

```text
Baseline A: human-only workflow
Baseline B: generic LLM
Baseline C: LLM + RAG
Baseline D: Sentinel tool-grounded architecture
```

Measure:

- task completion
- spatial correctness
- plan feasibility
- evidence quality
- time
- human workload
- unsafe recommendation rate

## 15. Bottom line

The literature strengthens, rather than weakens, the current Sentinel hypothesis — but it changes the emphasis.

Sentinel should be **less about adding AI agents** and more about building a reliable **human-AI operational decision system** where AI is constrained by tools, authoritative evidence, geospatial computation, resource constraints and human approval.

That should become the central criterion for the next model-scoring stage.

## Sources

- UNDRR/WMO/ITU/IFRC, *Leveraging AI to enhance multi-hazard early warning systems* (2026): https://www.undrr.org/publication/documents-and-publications/leveraging-ai-enhance-multi-hazard-early-warning-systems
- UNDRR, *Early Warning Systems for mobile populations* (2026): https://www.undrr.org/publication/documents-and-publications/early-warning-systems-mobile-populations-operational
- UNDRR, *Early Warning System* terminology: https://www.undrr.org/terminology/early-warning-system
- Domfeh & Dancy, *Human-AI Use Patterns for Decision-Making in Disaster Scenarios* (2025): https://arxiv.org/abs/2509.12034
- *DORA: A Benchmark for Disaster Response Agents* (2026): https://arxiv.org/abs/2605.11633
- *GeoDisaster* (2026): https://arxiv.org/abs/2606.17246
- *GISAgentBench* (2026): https://arxiv.org/abs/2608.01645
- *DisasterTD* (2026): https://arxiv.org/abs/2607.24856
- *Now We Know? A Systematic Comparison of TerraMind and THOR* (2026): https://arxiv.org/abs/2607.18504
- *A Systems Engineering Framework for Vision-Language-Enabled UAV Triage and Disaster Response* (2026): https://arxiv.org/abs/2607.27597
