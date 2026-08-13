# Sentinel v2 — Research Evidence Matrix

This matrix converts the literature review into design evidence. Scores are directional, not statistical meta-analysis.

| Capability | Evidence strength | Sentinel relevance | Recommended treatment |
|---|---|---:|---|
| Human-AI decision support | High | Very high | Core |
| Evidence/provenance | High | Very high | Core |
| Geospatial tool grounding | High/emerging | Very high | Core |
| Deterministic GIS validation | High | Very high | Core |
| Resource/task coordination | High | Very high | Core |
| Multimodal disaster evidence | Emerging | High | P1 |
| Satellite/SAR analysis | High domain evidence | High | P1 |
| Autonomous emergency action | Low suitability | Very high risk | Exclude initially |
| Generic LLM-only spatial reasoning | Weak reliability | High risk | Exclude |
| Large multi-agent graphs | Mixed | Medium | Keep bounded |
| New foundation-model training | High cost/uncertain ROI | Medium | Defer |
| Scenario simulation | Moderate-high | High | P0/P1 |
| Human/UAV coordination | Emerging | Medium | Future |
| Digital twin | Emerging | Medium | Future |

## Design rule

A feature should enter Sentinel v2 only when it has a clear user job, evidence of operational value, a feasible data path, and a validation method.

## Evidence quality hierarchy

1. Government / international operational guidance
2. Peer-reviewed or systematic-review evidence
3. Reproducible benchmark studies with explicit tasks/ground truth
4. Established operational datasets/platform documentation
5. Practitioner/community evidence
6. Vendor marketing claims

Vendor capabilities can inform competitive analysis but should not be treated as proof of effectiveness.
