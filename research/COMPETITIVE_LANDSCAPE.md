# Sentinel v2 — Competitive Landscape

**Status:** Research in progress  
**Date:** 2026-08-13  
**Decision:** Do not freeze the final product model yet.

## 1. Executive finding

The market is already crowded with products that do one or more of the following extremely well: public warning, emergency communications, common operating pictures, geospatial mapping, risk intelligence, response workflows, or resource coordination.

The strongest competitive lesson is therefore **not to build another alert dashboard or generic EOC dashboard**.

The potential whitespace for Sentinel is an **evidence-grounded decision-support layer that sits between incoming hazard intelligence and an approved operational response**. The product should combine multi-source situation awareness, geospatial impact analysis, constrained response planning, authoritative evidence, uncertainty, and human approval.

This is still a hypothesis. It must be validated against user needs and implementation feasibility before being frozen.

## 2. Competitive categories

| Category | Representative systems | Core strength | What Sentinel should learn |
|---|---|---|---|
| Public warning | NDMA SACHET, FEMA IPAWS | Authoritative alert dissemination, geo-targeting, multi-channel communication | Do not compete on public alert delivery; consume/interpret official alerts |
| Earth-observation emergency mapping | Copernicus EMS | Satellite/geospatial mapping, exposure, early warning, response/recovery products | Use geospatial evidence and exposure layers; focus Sentinel on decision synthesis |
| GIS/EOC platforms | Esri ArcGIS Emergency Management | Shared operational picture, real-time feeds, agency collaboration | A map is foundational; Sentinel needs an operational map, not only charts |
| Critical event management | Everbridge | Risk intelligence, workflows, communication, response coordination, after-action learning | Response orchestration and auditability matter; avoid trying to reproduce the entire enterprise suite |
| EOC workflow platforms | Veoci | Plans, activation, tasks, communications, live dashboards, after-action reporting | Human workflows and accountability are core product requirements |
| Specialized early-warning systems | INCOIS ITEWS, weather/flood systems | Domain-specific sensing, forecasting, SOPs, authoritative warnings | Sentinel should integrate specialist systems rather than replace them |
| Research agents | DORA, GeoDisaster and related work | Tool-grounded geospatial reasoning, evacuation, impact analysis, multimodal evidence | This is the most promising technical frontier for Sentinel |

## 3. NDMA SACHET — India benchmark

SACHET is a particularly important benchmark because Sentinel is intended to be India-relevant. SACHET is NDMA's CAP-based integrated alert system. It provides near-real-time geo-targeted alerts, supports multiple disaster types, multiple languages, simultaneous dissemination, and receives warning information from authorized government sources including NDMA, IMD, CWC, INCOIS and FSI.

The SACHET mobile experience also provides weather information, alert-affected areas, dos and don'ts, and multilingual/read-out capabilities.

**Implication:** Sentinel should not position itself as a replacement for SACHET. A better role is to ingest official alerts and turn them into a richer operational picture: what is affected, who is exposed, what resources are constrained, which routes are feasible, what evidence supports an action, and what a human decision-maker should review.

## 4. Copernicus EMS — geospatial benchmark

Copernicus EMS already provides early warning/monitoring, on-demand mapping, and exposure mapping. It uses satellite and other geospatial information to support preparedness, response and recovery. Its exposure products can answer questions such as how many people or settlements are affected.

**Implication:** "AI + satellite map" alone is not a differentiator. Sentinel needs to add an operational reasoning and planning layer over geospatial evidence.

## 5. Esri — GIS/EOC benchmark

Esri's emergency-management solution provides real-time data feeds, shared situational awareness, and a cloud-based operational picture for emergency operations centers and partner agencies.

**Implication:** Sentinel needs a real map and live operational picture, but should not attempt to recreate a mature GIS platform. The differentiator should be AI-assisted synthesis, tool-grounded reasoning, evidence traceability, and scenario/response planning.

## 6. Everbridge — critical-event-management benchmark

Everbridge's current Critical Event Management platform covers risk intelligence, mass notification, crisis management, response management, situational awareness and after-action improvement. Its current positioning explicitly combines AI, risk intelligence, workflows and human-guided response.

**Implication:** The phrase "AI disaster operations copilot" by itself is not sufficient differentiation. Sentinel needs a narrower and technically defensible wedge, such as geospatial evidence-to-action reasoning for disaster operations.

## 7. Veoci — EOC workflow benchmark

Veoci provides planning, activation, response, communications, situational awareness, resource/asset management and after-action reporting. It emphasizes one-click activation, task assignment, live incoming data, and automatic records/timestamps.

**Implication:** Sentinel should include explicit human approval, task/accountability state, audit trails, and after-action evidence if it enters operational planning.

## 8. INCOIS ITEWS — specialist-system benchmark

India's tsunami warning system is a mature 24x7 specialist system with seismic stations, bottom pressure recorders, tide gauges, ocean observations, inundation modelling, scenario databases, decision-support rules and formal SOP-based dissemination.

**Implication:** Sentinel should be an integration/decision layer, not a replacement for specialist hazard-warning authorities. This principle should apply to IMD, CWC, INCOIS and similar systems.

## 9. Research frontier

Two 2026 benchmarks are particularly relevant:

- **DORA** evaluates end-to-end disaster-response agents across disaster perception, spatial reasoning, rescue/evacuation planning, temporal evolution and multimodal report synthesis. It reports persistent problems in tool selection, argument grounding and long-horizon compositional reliability.
- **GeoDisaster** evaluates operational geo-intelligence over optical/SAR imagery, vector geometries, road networks and exposure layers. It explicitly uses tool-grounded workflows and deterministic consistency checks.

**Implication:** Sentinel's architecture should treat LLMs as planners/reasoners that invoke explicit tools, while GIS, routing, exposure, resource arithmetic and validation remain deterministic services.

## 10. Competitive whitespace hypothesis

The strongest current hypothesis is:

> **Sentinel should not own the warning, GIS, forecasting or EOC workflow categories. It should connect them through an evidence-grounded, human-approved operational decision layer.**

Potential core loop:

```text
Official / sensor / EO inputs
          ↓
Situation synthesis
          ↓
Hazard risk + uncertainty
          ↓
Geospatial impact assessment
          ↓
Constrained response planning
          ↓
Evidence + assumptions
          ↓
Human review / approval
          ↓
Operational plan / report
```

## 11. What we should avoid

- Generic chatbot positioning
- Generic "AI predicts disasters" claims
- Building a second public-alert platform
- Rebuilding a full enterprise GIS suite
- Rebuilding a full mass-notification/CEM platform
- Treating LLM-generated geographic calculations as authoritative
- Automatic real-world emergency action without human authorization

## 12. Research conclusion

**Preliminary winner:** a **geospatial, evidence-grounded, human-in-the-loop disaster operations decision-support platform**.

**Confidence:** Medium.  
**Why not final yet:** market research still needs explicit personas, user jobs-to-be-done, feasibility/cost analysis, data-access validation, detailed literature synthesis, and model scoring.

## Sources

- NDMA SACHET: https://sachet.ndma.gov.in/
- Copernicus EMS: https://emergency.copernicus.eu/about/
- Copernicus EMS Mapping: https://mapping.emergency.copernicus.eu/
- Esri Emergency Management: https://www.esri.com/en-us/c/industry/public-safety/emergency-management-operations-solution
- Everbridge CEM: https://www.everbridge.com/platform/critical-event-management/
- Veoci Emergency Management: https://veoci.com/emergency-management/
- INCOIS ITEWS: https://tsunami.incois.gov.in/TEWS/searlywarnings.jsp
- DORA: https://arxiv.org/abs/2605.11633
- GeoDisaster: https://arxiv.org/abs/2606.17246
