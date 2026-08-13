# Sentinel v2 — User Personas & Jobs-to-be-Done

**Status:** Research in progress  
**Date:** 2026-08-13  
**Decision:** Personas are evidence-based hypotheses, not validated customer requirements.

## 1. Why this research matters

Sentinel should be designed around the decisions people must make during an incident, not around the AI capabilities available to the developer.

Current emergency-management doctrine strongly emphasizes shared situational awareness, information management, resource management, prioritization, coordination and planning. FEMA's EOC guidance describes EOCs as coordination functions that collect/distribute information, evaluate priorities, manage additional resource needs and support multi-jurisdiction/multi-agency coordination. FEMA also identifies situational awareness, planning support and resource support as distinct EOC functions.

UNDRR's 2026 guidance on AI for multi-hazard early warning similarly emphasizes human oversight for life-safety decisions, human-centred design, interoperability, multilingual/low-connectivity considerations and co-design with affected communities.

## 2. Primary persona — Emergency Operations / Situation Officer

### Role
The person responsible for maintaining the operational picture inside an EOC/control room and turning fragmented incoming information into a usable situation update.

### Core job
> When an incident is changing quickly, help me understand what has changed, what information is trustworthy, what areas/people/assets are affected, and what the response team needs to know next.

### Pain points
- Multiple feeds with different timestamps and reliability.
- Information arrives in incompatible formats.
- Important changes can be buried in reports.
- GIS, weather, alerts, field reports and resource systems may be separate.
- Situation reports require repeated manual synthesis.
- Decision-makers need concise updates, but analysts need drill-down evidence.

### Sentinel opportunity
- Multi-source situation synthesis.
- Data freshness and provenance.
- Change detection between situation updates.
- Map-linked evidence.
- Automatic briefing drafts with citations.
- Confidence/uncertainty indicators.

### Must not do
- Present an AI summary without source/time context.
- Hide contradictory information.
- Automatically publish an authoritative warning.

## 3. Primary persona — Incident / Response Decision-Maker

### Role
Incident commander, emergency manager, district/state response lead, or equivalent decision-maker who establishes priorities and approves operational actions.

### Core job
> Given incomplete and changing information, help me compare response options, understand consequences and resource constraints, and make a defensible decision quickly.

### Pain points
- High consequence decisions under uncertainty.
- Need to balance life safety, infrastructure, access and limited resources.
- Need to understand why a recommendation was generated.
- Cannot spend time reading every source document.
- Recommendations must remain compatible with established SOPs and authority structures.

### Sentinel opportunity
- Prioritized decision cards.
- Option comparison and what-if analysis.
- Impact estimates.
- Resource constraints.
- Route/shelter alternatives.
- Evidence and assumptions shown alongside recommendations.
- Explicit approve/modify/reject workflow.

### Must not do
- Replace the authorized decision-maker.
- Turn probabilistic model output into an unconditional command.
- Recommend an action without surfacing material uncertainty.

## 4. Primary persona — Planning / Logistics Officer

### Role
Person responsible for identifying resource requirements, requests, staging, deployment, tracking and gaps.

### Core job
> Given incident priorities and expected impacts, help me determine what resources are needed, where they should be positioned, what is already available, and what gaps require escalation or mutual aid.

### Pain points
- Resource inventories are distributed.
- Requirements change as the incident evolves.
- Static quantities do not capture location, timing or capacity.
- Requests must be justified and prioritized.
- Resources may be shared across jurisdictions.

### Sentinel opportunity
- Deterministic resource calculations.
- Location-aware resource matching.
- Resource gap detection.
- Prioritization based on incident objectives.
- Scenario-based staging recommendations.
- Request/audit history.

### Important design rule
The LLM should not invent quantities. Resource arithmetic, constraints and optimization should remain deterministic and auditable.

## 5. Secondary persona — Field Responder / Field Coordinator

### Role
Responder, search-and-rescue coordinator, public works/fire/medical coordinator, or field team lead.

### Core job
> Give me a concise, current picture of the hazard, mission, safe access routes, nearby resources and changes that affect my team's safety and assignment.

### Pain points
- Information overload.
- Connectivity can be unreliable.
- Field conditions change faster than central reports.
- Maps must remain readable under stress.
- Tactical information must be immediately actionable.

### Sentinel opportunity
- Mission-specific views.
- Offline/low-bandwidth fallback.
- Simple map layers.
- Route and hazard warnings.
- Recent changes rather than long narrative.

### Product implication
Do not make the same dashboard serve every persona. The officer, commander and field responder need different information density and interaction patterns.

## 6. Secondary persona — Public Information / Communication Officer

### Role
Person who converts verified operational information into public-facing updates.

### Core job
> Help me turn approved, evidence-backed operational information into clear, audience-appropriate communication without accidentally publishing uncertain or unapproved claims.

### Sentinel opportunity
- Draft communication from approved facts.
- Source links and timestamps.
- Audience variants.
- Multilingual drafts.
- Approval gates.
- Change tracking between versions.

### Safety requirement
AI may draft. An authorized human should approve life-safety public communication.

## 7. Tertiary persona — Analyst / Preparedness Planner

### Role
Risk analyst, preparedness planner, researcher, or disaster-management professional working before an incident.

### Core job
> Help me understand recurring risk patterns, test scenarios, identify capability gaps and improve preparedness plans before the next incident.

### Sentinel opportunity
- Historical incident analysis.
- Scenario simulation.
- What-if planning.
- Resource gap analysis.
- After-action learning.
- Model/evaluation dashboards.

This persona is important because Sentinel should eventually support the full preparedness-to-response learning loop, not only live incidents.

## 8. Persona priority

| Persona | Priority | Reason |
|---|---:|---|
| EOC / Situation Officer | P0 | Strongest match to Sentinel's proposed information-synthesis wedge |
| Incident / Response Decision-Maker | P0 | Owns high-value decisions Sentinel should support |
| Planning / Logistics Officer | P0 | Directly connects to existing deterministic Resource Agent |
| Field Coordinator | P1 | High operational value but stronger connectivity/usability constraints |
| Public Information Officer | P1 | Valuable communication layer but official approval is essential |
| Preparedness Analyst | P1 | Enables simulation and learning beyond active incidents |
| General citizen | P2 | Important ecosystem stakeholder, but not the primary Sentinel operator |

## 9. Jobs-to-be-Done hierarchy

### Job 1 — Know what is happening
Collect, normalize, timestamp and summarize relevant observations and alerts.

### Job 2 — Know what changed
Detect meaningful changes since the last operational update.

### Job 3 — Know what is affected
Estimate affected people, infrastructure, roads, services and vulnerable groups.

### Job 4 — Know what can be done
Generate feasible response options subject to real constraints.

### Job 5 — Know why the recommendation exists
Show evidence, assumptions, uncertainty and model/tool outputs.

### Job 6 — Decide and document
Allow an authorized person to approve, modify or reject a recommendation and record the decision.

### Job 7 — Learn
Compare predicted conditions and planned actions with observed outcomes after the event.

## 10. Highest-value workflow

The evidence suggests the core workflow should be:

```text
Observe
  ↓
Orient
  ↓
Assess impact
  ↓
Generate response options
  ↓
Compare options + constraints
  ↓
Show evidence + uncertainty
  ↓
Human decision
  ↓
Track action
  ↓
Observe outcome
  ↓
Learn
```

This aligns with the OODA-style disaster-agent research direction while preserving human authority.

## 11. Product implications

### Sentinel should optimize for
- Decision speed without hiding uncertainty.
- Information provenance.
- Shared situational awareness.
- Map-first understanding.
- Resource and constraint awareness.
- Explicit human approval.
- Interoperability with existing systems.
- Different views for different roles.
- Low-bandwidth/operational resilience where feasible.

### Sentinel should not optimize for
- Maximum number of agents.
- Maximum number of dashboards.
- Fully autonomous emergency action.
- Replacing authoritative forecasting/warning agencies.
- A generic citizen chatbot as the core product.

## 12. Research-backed observations

FEMA EOC guidance identifies information collection/sharing, priority evaluation, resource management, planning and coordination as central EOC functions. FEMA also describes situational awareness, planning support and resource support as distinct operational functions.

UNDRR's 2026 AI guidance emphasizes human oversight for life-safety decisions, human-centred and equity-driven design, multilingual/low-connectivity compatibility, interoperability, and co-design with affected communities.

A 2025 systematic review of 51 peer-reviewed studies on Human-AI use in disaster decision-making groups major patterns into decision support, task/resource coordination, trust/transparency, and simulation/training, while identifying interpretability, interoperability and scalability as persistent challenges.

Community discussions from emergency-management practitioners also reinforce that information flow, resource visibility and usability under pressure are practical constraints; these discussions are directional evidence, not formal requirements.

## 13. Open validation questions

Before freezing the product model, we still need evidence for:

1. Which persona has the strongest unmet need that Sentinel can realistically address?
2. Which operational decisions are safe and useful for AI assistance?
3. What data can be accessed reliably in India?
4. What information is actually available during the first 10–30 minutes of an incident?
5. Which decisions require deterministic optimization versus human judgment?
6. What latency is acceptable for situation updates?
7. What connectivity constraints must the product tolerate?
8. What evidence/provenance must be shown for a recommendation to be trusted?
9. Which existing EOC/GIS systems would Sentinel need to integrate with?
10. What measurable outcome should define Sentinel success?

## Sources

- FEMA IS-2200 EOC functions: https://emilms.fema.gov/is_2200/index.html
- FEMA EOC coordination functions: https://emilms.fema.gov/is_0552/groups/230.html
- FEMA NIMS resource management: https://www.usfa.fema.gov/a-z/nims/resource-management.html
- FEMA command and coordination: https://www.usfa.fema.gov/a-z/nims/command-and-coordination.html
- FEMA EOC Toolkit: https://preptoolkit.fema.gov/web/nims-toolkit/eoc
- NDMA India ERSS: https://ndmindia.mha.gov.in/ndmi/programs
- UNDRR AI and multi-hazard early warning: https://www.undrr.org/publication/documents-and-publications/leveraging-ai-enhance-multi-hazard-early-warning-systems
- UNDRR Early Warning for All risk knowledge: https://www.undrr.org/building-risk-knowledge/early-warnings-for-all-risk-knowledge-resource-package
- Human-AI Use Patterns systematic review: https://arxiv.org/abs/2509.12034
- Emergency response decision support systems: https://arxiv.org/abs/2202.11268
- RAPTOR-AI disaster OODA loop: https://arxiv.org/abs/2602.00030
