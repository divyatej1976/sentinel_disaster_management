# SentinelAI v2 — Market & Ecosystem Research

**Status:** Working research baseline  
**Date:** 13 August 2026  
**Purpose:** Establish the market, technology, research, and differentiation landscape before changing the Sentinel implementation.

> This document is research, not the final product decision. Model selection happens only after the competitive and gap analysis is complete.

---

## 1. Executive Summary

SentinelAI currently combines multi-agent risk assessment, deterministic resource calculation, curated RAG, reporting, multi-hazard plugins, request tracing, and SQLite history. The repository's latest Phase 5 commit is the baseline for this research.

The external landscape shows that disaster management is already crowded with strong systems for **official warning dissemination, geospatial emergency mapping, early warning, exposure mapping, and remote-sensing analysis**. Therefore, Sentinel should not try to become another generic alert portal or another satellite mapping service.

The strongest emerging opportunity is the **operational intelligence layer between an official warning/observation and a human decision-maker**: integrate heterogeneous evidence, assess impact, reason over geography, estimate operational consequences, propose response options, and provide traceable evidence for human approval.

This is strongly supported by current research. The 2026 DORA benchmark defines operational disaster response around perception, spatial reasoning, rescue/evacuation planning, temporal reasoning, and multimodal reporting. GeoDisaster similarly emphasizes tool-grounded geospatial reasoning, exposure estimation, flood-safe routing, damage assessment, and evidence-backed decisions.

### Preliminary strategic direction

> **SentinelAI should evolve from an AI disaster risk/intelligence dashboard into a human-in-the-loop, multi-hazard disaster operations copilot.**

This is a research hypothesis only. It will be formally scored against alternative models before being frozen.

---

## 2. Current Sentinel Baseline

The current repository implements:

- Multi-hazard plugin architecture
- Disease and Flood hazard modules
- Three-persona weighted risk consensus
- Deterministic resource formulas
- Curated RAG with citations
- Report generation for different audiences
- Live weather/environment telemetry integration
- Scenario comparison / delta analysis
- Request-ID observability
- SQLite assessment history
- Deterministic fallbacks when the LLM is unavailable

The current architecture deliberately separates LLM reasoning from deterministic calculations and keeps hazard-specific logic inside hazard modules. This should be preserved unless research proves a better model.

### Current conceptual pipeline

```text
Input telemetry
      ↓
Risk Agent
      ↓
Resource Agent
      ↓
Knowledge Agent
      ↓
Report Agent
```

### Current architectural strength

The strongest existing design decision is separation of concerns:

- LLMs reason over qualitative/uncertain information.
- Deterministic code performs resource calculations.
- RAG grounds knowledge claims.
- Hazard modules contain hazard-specific logic.

The v2 process should build on this rather than replacing it with an indiscriminate agent framework.

---

## 3. Market Landscape

### 3.1 Government early-warning systems

#### India — NDMA SACHET

SACHET is India's National Disaster Alert Portal. NDMA describes it as a CAP-based integrated alert system using geo-intelligence for near-real-time dissemination of early warnings across multiple media. It supports multi-hazard, geo-targeted, multilingual and simultaneous alerts. It also exposes an India CAP RSS feed for downstream dissemination.

**What SACHET already does well**

- Official warning dissemination
- Geo-targeting
- Multi-hazard coverage
- Multi-language communication
- Integration of authorized government warning sources
- Citizen-facing alerts

**What Sentinel should not attempt to duplicate**

- Becoming an official replacement for SACHET
- Issuing authoritative public warnings independently
- Competing on citizen alert distribution

**Potential Sentinel relationship**

Sentinel can consume official alerts and turn them into operational intelligence: impact, affected assets, resource implications, response options, evidence, and human-approved plans.

Source: https://sachet.ndma.gov.in/

---

### 3.2 Copernicus Emergency Management Service

Copernicus EMS provides geospatial information for emergency response and disaster risk management. Its mapping component uses satellite imagery and other geospatial data and supports preparedness, rapid response, and recovery. It provides event extent, infrastructure damage assessment, exposure-related information, maps and reports.

**Strengths**

- High-quality Earth observation workflows
- Satellite and geospatial data
- Rapid mapping
- Damage assessment
- Preparedness and recovery mapping
- Operational emergency-management orientation
- Mature validation processes

**Implication for Sentinel**

Sentinel should not attempt to become a full replacement for Copernicus-style remote-sensing mapping. Instead, it can consume geospatial products and use them as evidence for operational reasoning and response planning.

Source: https://emergency.copernicus.eu/  
Mapping: https://mapping.emergency.copernicus.eu/

---

### 3.3 Existing early-warning / hazard-monitoring ecosystems

Modern disaster ecosystems already contain specialized forecasting and monitoring systems for floods, fires, weather, oceans, droughts and other hazards.

This means Sentinel's differentiation should not be "we have a weather API" or "we predict floods." Those capabilities are inputs to a larger decision-support workflow.

The opportunity is **cross-source synthesis and operational reasoning**.

---

## 4. Research Landscape — 2026

### 4.1 DORA: Disaster Operational Response Agent benchmark

The May 2026 DORA paper is highly relevant to Sentinel.

DORA defines end-to-end disaster-response tasks across:

1. Disaster perception
2. Spatial relational analysis
3. Rescue and evacuation planning
4. Temporal evolution reasoning
5. Multimodal report synthesis

It uses 515 expert-authored tasks across 45 real-world disaster events and 3,500 tool-call steps. The benchmark uses heterogeneous geospatial tools and data including optical, SAR, multispectral imagery, elevation and social vector layers.

A major finding is that agents suffer from tool-selection and argument-grounding problems, and long compositional workflows become substantially more fragile.

**Direct implication for Sentinel:**

Do not build an LLM that is expected to "know" geography. Build deterministic, typed tools for geography and make the agent reason over their results.

Source: https://arxiv.org/abs/2605.11633

---

### 4.2 GeoDisaster benchmark

GeoDisaster evaluates operational disaster geo-intelligence using heterogeneous EO/GIS evidence and deterministic consistency checks.

Its task families include:

- Deforestation monitoring
- Multi-hazard analysis
- Building-damage assessment
- Flood-safe routing
- Sentinel-1 SAR flood monitoring

The work emphasizes that operational geo-intelligence requires tool-grounded spatial reasoning and structured, evidence-backed decisions rather than visual interpretation alone.

**Direct implication for Sentinel:**

A strong v2 should include a geospatial tool layer, exposure analysis, route reasoning, evidence provenance, and structured execution contracts.

Source: https://arxiv.org/abs/2606.17246

---

## 5. Technology / Data Ecosystem

### Earth observation

Satellite and remote-sensing data are increasingly central to emergency mapping. Copernicus EMS explicitly uses Sentinel missions and other Earth-observation sources for emergency mapping.

**Potential Sentinel use:**

- Flood extent evidence
- Burn-area evidence
- Damage evidence
- Before/after comparison
- Change detection

Important: satellite analysis should be treated as an evidence pipeline, not as a generic LLM image prompt.

---

### Fire data — NASA FIRMS

NASA FIRMS provides active-fire observations from satellite instruments and supports programmatic access.

Potential Sentinel use:

```text
FIRMS observations
      ↓
Fire cluster / event detection
      ↓
Weather + wind
      ↓
Exposure analysis
      ↓
Operational risk
```

Source: https://firms.modaps.eosdis.nasa.gov/

---

### Flood data — GloFAS

The Copernicus Emergency Management Service / ECMWF ecosystem provides global flood forecasting and flood-risk products.

Potential Sentinel use:

```text
Flood forecast
      +
Observed flood evidence
      +
Elevation
      +
Population
      +
Road network
      ↓
Impact assessment
```

Source: https://confluence.ecmwf.int/

---

### Geospatial APIs / standards

OGC API Features provides standardized building blocks for querying and accessing geographic features over the web.

**Implication:** Sentinel should prefer interoperable geospatial data structures over proprietary ad-hoc formats where practical.

Source: https://www.ogc.org/standards/ogcapi-features/

Potential future standards to evaluate:

- OGC API Features
- STAC for spatiotemporal Earth-observation assets
- GeoJSON
- Cloud Optimized GeoTIFF
- GeoParquet
- Common Alerting Protocol (CAP)

---

## 6. Competitive Capability Matrix — Preliminary

| Capability | Official Alert Platforms | EO / Mapping Platforms | Typical EOC | Current Sentinel | Candidate Sentinel v2 |
|---|---:|---:|---:|---:|---:|
| Official alerts | Strong | Limited | Strong | Limited | Consume, don't replace |
| Multi-hazard | Strong | Strong | Strong | Strong | Strong |
| Risk assessment | Strong | Partial | Strong | Strong | Strong |
| Satellite analysis | Partial | Strong | Partial | Limited | Evidence integration |
| Geospatial analysis | Strong | Strong | Strong | Limited | Core capability |
| Population exposure | Partial | Strong | Strong | Limited | Core capability |
| Infrastructure impact | Partial | Strong | Strong | Limited | Core capability |
| Resource calculation | Limited | Limited | Strong | Strong | Dynamic allocation |
| Evacuation planning | Limited | Partial | Strong | Limited | Core capability |
| Route optimization | Limited | Partial | Strong | Limited | Deterministic tool |
| RAG / evidence grounding | Limited | Limited | Partial | Strong | Strong |
| Multi-agent reasoning | Limited | Emerging | Emerging | Strong | Tool-grounded |
| Scenario simulation | Limited | Partial | Strong | Strong | Temporal what-if |
| Human approval workflow | Strong | Strong | Strong | Limited | Core capability |
| Operational reports | Strong | Strong | Strong | Strong | Evidence-backed |
| Citizen dissemination | Strong | Limited | Strong | Limited | Not primary scope |

This table is intentionally marked preliminary. Each cell will be validated during the detailed competitive research stage.

---

## 7. Major Market Gaps Identified

### Gap A — Warning-to-action translation

Official warning systems are optimized for getting warnings to people. Mapping systems are optimized for producing geospatial information. Emergency operations centers coordinate response.

There is an opportunity for a system that explicitly bridges:

```text
Official warning / observation
            ↓
     What does it mean here?
            ↓
     Who / what is exposed?
            ↓
     What will be affected next?
            ↓
     What response options exist?
            ↓
     Which option should a human approve?
```

### Gap B — Tool-grounded AI operations

Current research shows that disaster agents need access to specialized tools and structured workflows. A general LLM alone is insufficient.

### Gap C — Cross-domain synthesis

The useful decision often requires combining:

- hazard information
- weather
- GIS
- roads
- population
- infrastructure
- shelters
- resources
- official guidance

The differentiator can be the synthesis layer rather than ownership of every underlying dataset.

### Gap D — Evidence-backed operational recommendations

A recommendation should expose:

- data used
- timestamp
- source
- spatial evidence
- calculations
- uncertainty
- policy/guideline evidence
- assumptions

This is a natural extension of Sentinel's existing RAG/citation design.

### Gap E — Human-in-the-loop decision support

High-stakes disaster response should not be presented as autonomous authority. A strong product should make the human decision explicit:

```text
AI recommendation
      ↓
Evidence
      ↓
Confidence / uncertainty
      ↓
Human approve / modify / reject
      ↓
Audit trail
```

---

## 8. Product Model Candidates

These are candidate models to score before freezing Sentinel v2.

### Model A — AI Disaster Risk Intelligence

**Concept:** Improve the current product primarily as a multi-hazard risk and knowledge platform.

**Pros**
- Lowest implementation risk
- Reuses most existing code
- Clear extension of current Sentinel
- Easier to validate

**Cons**
- Crowded positioning
- Less differentiated from existing risk dashboards
- Limited operational value after the risk score
- Less aligned with emerging geospatial-agent research

---

### Model B — AI Disaster Operations Copilot

**Concept:** Turn observations and warnings into impact analysis, response options, resource planning, evacuation planning, evidence and human-approved actions.

**Pros**
- Strong alignment with current research
- Builds naturally on current Sentinel architecture
- Clear human-in-the-loop story
- Strong full-stack + AI + GIS portfolio value
- Can consume existing government/EO systems instead of competing with them

**Cons**
- More complex
- Requires geospatial data and deterministic tools
- Requires careful evaluation
- Higher safety/reliability burden

---

### Model C — Geospatial Disaster Intelligence Platform

**Concept:** Make Sentinel primarily a GIS/EO disaster analysis platform.

**Pros**
- Strong technical depth
- Satellite + GIS is highly relevant
- Strong research potential

**Cons**
- Directly overlaps mature mapping ecosystems
- Remote sensing pipeline can become the whole project
- Less differentiated on the AI decision-support side

---

### Model D — Autonomous Multi-Agent Emergency Response System

**Concept:** Agents autonomously coordinate detection, planning and response.

**Pros**
- Technically ambitious
- Strong research interest
- Demonstrates advanced agent orchestration

**Cons**
- Safety concerns
- Hard to validate
- Current research shows long agent trajectories are fragile
- Too much autonomy is inappropriate for a portfolio system intended to model real emergency operations

**Recommendation:** Do not choose this as the primary model.

---

### Model E — AI Early-Warning Platform

**Concept:** Focus on prediction and public warning generation.

**Pros**
- Clear social value
- Strong research domain
- Natural connection to live data

**Cons**
- Major overlap with existing government warning infrastructure
- High safety burden
- Official alert authority cannot be casually replicated

**Recommendation:** Do not make this Sentinel's core identity.

---

### Model F — Multimodal Disaster Intelligence & Decision Support

**Concept:** Combine satellite imagery, structured telemetry, GIS, documents, forecasts and operational data into a multimodal decision-support system.

**Pros**
- Research-aligned
- Strong multimodal story
- High technical depth
- Strong long-term extensibility

**Cons**
- Broad scope
- Easy to become an unfocused platform
- Requires disciplined MVP boundaries

---

## 9. Preliminary Scoring

Score: 1 = weak, 5 = strong. This is a first-pass hypothesis and will be revisited after deeper market research.

| Model | Market Need | Differentiation | Feasibility | Research Value | Portfolio Value | Safety/Control | Overall |
|---|---:|---:|---:|---:|---:|---:|---:|
| A. Risk Intelligence | 4 | 2 | 5 | 3 | 4 | 4 | 22 |
| B. Operations Copilot | 5 | 5 | 4 | 5 | 5 | 4 | **28** |
| C. Geospatial Platform | 4 | 3 | 3 | 5 | 5 | 4 | 24 |
| D. Autonomous Response | 3 | 5 | 2 | 5 | 5 | 1 | 21 |
| E. Early Warning | 4 | 2 | 2 | 4 | 4 | 1 | 17 |
| F. Multimodal Decision Support | 5 | 4 | 3 | 5 | 5 | 3 | 25 |

### Preliminary leader

**Model B — AI Disaster Operations Copilot**

Model F should remain a close alternative and may become the technical architecture underneath Model B.

---

## 10. Proposed Strategic Positioning — NOT YET FROZEN

> **SentinelAI is a human-in-the-loop disaster operations copilot that converts heterogeneous hazard, geospatial, environmental and knowledge signals into evidence-backed impact assessments and actionable response options.**

The product should sit **between information systems and operational decision-making**.

It should consume and integrate authoritative data rather than attempting to replace official warning authorities.

---

## 11. Candidate Sentinel v2 Capability Model

If Model B survives the next research stage, the candidate capability stack becomes:

### Situation Awareness

- ingest live/near-live signals
- normalize observations
- maintain current incident state
- track changes over time

### Risk

- multi-persona reasoning
- deterministic risk factors where appropriate
- uncertainty and disagreement

### Impact

- affected geography
- population exposure
- infrastructure exposure
- road/shelter/hospital impact

### Geospatial Intelligence

- spatial intersection
- proximity analysis
- network analysis
- route feasibility
- hazard layers

### Response Planning

- evacuation options
- shelter allocation
- resource allocation
- priority zones
- alternative plans

### Evidence

- RAG
- source provenance
- timestamps
- citations
- evidence strength

### Human Decision Support

- recommendation
- assumptions
- confidence
- approve / modify / reject
- audit trail

### Reporting

- officer
- executive
- citizen-safe summary
- machine-readable operational output

---

## 12. What Sentinel Should NOT Become

The research indicates several areas where scope should remain deliberately bounded.

1. **Not an official warning authority.** Consume official alerts where possible.
2. **Not a replacement for Copernicus/ISRO/NASA/IMD/CWC/INCOIS.** Integrate their data/products.
3. **Not a fully autonomous emergency commander.** Keep human authorization.
4. **Not an LLM-only GIS engine.** Use deterministic geospatial tooling.
5. **Not a generic chatbot with a disaster theme.** The primary UI should represent operational state.
6. **Not a collection of agents with no measurable benefit.** Every agent must own a distinct capability.
7. **Not every hazard at once.** Start with a small number of deeply implemented hazards.

---

## 13. Research Questions Still Open

Before freezing the product model, the following must be investigated:

- Which user persona should be primary: emergency officer, municipal operator, NGO, analyst, or field responder?
- Which first hazard gives the strongest combination of data availability, demonstrability and value?
- Which Indian data sources can be legally and reliably accessed programmatically?
- Which satellite datasets are feasible for an MVP?
- Should Sentinel use PostGIS?
- Should a vector database remain separate from geospatial storage?
- Which routing engine should be used?
- How should uncertainty be represented?
- How should recommendations be evaluated?
- What historical disaster cases can become a benchmark?
- Which capabilities require real ML versus rules versus LLM reasoning?
- What is the smallest differentiated MVP?
- What should remain future research rather than implementation scope?

---

## 14. Preliminary Decision

**Do not implement the proposed v2 yet.**

The evidence currently favors:

> **SentinelAI — Human-in-the-loop AI Disaster Operations Copilot**

with geospatial reasoning, impact assessment, response planning, evidence grounding and human approval as the core differentiators.

However, this remains a **provisional product hypothesis** until the following artifacts are completed:

1. Detailed competitive landscape
2. Research/literature review
3. Data/API feasibility matrix
4. User/persona analysis
5. Gap/opportunity matrix
6. Model scoring and final selection
7. Sentinel v1 → v2 gap analysis
8. Final Product Requirements Document

Only then should the v2 architecture be frozen.

---

## 15. Sources / Research Starting Set

- NDMA SACHET: https://sachet.ndma.gov.in/
- Copernicus Emergency Management Service: https://emergency.copernicus.eu/
- Copernicus EMS Mapping: https://mapping.emergency.copernicus.eu/
- NASA FIRMS: https://firms.modaps.eosdis.nasa.gov/
- ECMWF / GloFAS information: https://confluence.ecmwf.int/
- OGC API Features: https://www.ogc.org/standards/ogcapi-features/
- DORA benchmark: https://arxiv.org/abs/2605.11633
- GeoDisaster benchmark: https://arxiv.org/abs/2606.17246
- UNDRR early-warning systems: https://www.undrr.org/

---

## Decision Log

| Date | Decision | Status | Reason |
|---|---|---|---|
| 2026-08-13 | Do not modify implementation before market research | Accepted | Product model must be evidence-driven |
| 2026-08-13 | Keep current Sentinel as v1 baseline | Accepted | Current architecture provides a strong foundation |
| 2026-08-13 | Preliminary preference for Operations Copilot | Provisional | Best balance of need, differentiation, research and portfolio value |
| 2026-08-13 | Do not duplicate official alert authority | Provisional | SACHET and other official systems already occupy this role |
| 2026-08-13 | Prefer tool-grounded geospatial reasoning | Provisional | Supported by current disaster-agent research |
