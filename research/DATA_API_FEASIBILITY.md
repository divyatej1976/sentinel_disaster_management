# Sentinel v2 — Data & API Feasibility

**Status:** Research in progress  
**Date:** 2026-08-14  
**Scope:** India-first disaster operations decision support, with global data sources where useful.

## 1. Executive conclusion

The data landscape is strong enough to build a credible Sentinel v2 without inventing a proprietary data platform. However, the research changes the product strategy in an important way:

> **Sentinel should integrate existing authoritative and open data systems rather than recreate their forecasting or warning functions.**

There is also a major India-specific discovery: the Andhra Pradesh State Disaster Management Authority (APSDMA) GIS Portal already exposes a broad operational ecosystem including active hazards, weather, lightning, CWC flood forecasts, road closures, emergency services, shelters, situational awareness, drought, reservoirs, geospatial tools and a 13-tab DSS. Its GIS server exposes queryable feature services for infrastructure and administrative layers. This means a generic "multi-hazard map + dashboard" would have weak differentiation in Andhra Pradesh.

The product must therefore differentiate at the **evidence-to-decision / response-planning layer**, not by simply aggregating maps.

## 2. Feasibility matrix

| Source | Primary use | Access | Freshness | Cost/access concern | Sentinel recommendation |
|---|---|---|---|---|---|
| NDMA SACHET | Official alerts / CAP | Public portal; CAP/RSS dissemination documented | Near real-time | Need to validate machine-ingestion path and terms | P0 integration target |
| IMD API | Weather observations, forecasts, warnings | Official API gateway; authenticated | Real-time/forecast | API registrations temporarily paused while new pricing policy is implemented | P0 adapter, but provide fallback |
| CWC | River/flood forecasts, monitoring | Public portals and dissemination channels | Current + forecast | Programmatic access must be validated per service | P0 for flood use case |
| INCOIS ITEWS | Tsunami/coastal monitoring, advisories | Public monitoring pages; API/RSS links exposed | Real-time | Direct API contract needs validation | P1/specialist integration |
| APSDMA GIS | AP hazards, infrastructure, emergency services, shelters, roads, situational awareness | Public portal + ArcGIS REST feature services | Mix of live/static | Need to respect service policy and operational stability | **P0 research/integration target** |
| NASA FIRMS | Active fire detections | API/web services; MAP_KEY | Near-real-time | Registration/MAP_KEY; satellite limitations | P1 wildfire integration |
| Copernicus Sentinel-1 | SAR EO | CDSE STAC/OData/data products | Depends on acquisition/catalogue | Registration/capacity and processing cost | P1 flood/EO evidence |
| Copernicus CDS/CEMS/GloFAS | Weather/reanalysis/flood forecasts | API after account/terms acceptance | Forecast/reanalysis | Large-data requests and service limits | P1 flood scenario/validation |
| OpenStreetMap / Overpass | Roads/POIs/base infrastructure | Public ecosystem APIs | Changing | Public service fair-use limits; don't use as production backend at scale | P0 prototype, production provider later |
| OpenAQ | Air-quality observations | API v3 with API key | Near-real-time + historical | Key/rate limits and upstream coverage | P2 unless air-quality hazard is prioritized |
| data.gov.in | Historical Indian datasets | Public catalogue/API/downloads vary by dataset | Usually historical/periodic | Dataset-specific freshness/coverage | P0 evaluation/training source |

## 3. Critical India finding — APSDMA already covers much of the obvious product surface

The current APSDMA GIS Portal publicly advertises:

- Active Hazards Dashboard
- Weather Dashboard
- Lightning Dashboard
- Water Levels & Flood Forecast
- Road Closures Dashboard
- Emergency Services Dashboard
- Active Hazards Web Map
- Situational Awareness tool
- Shelter Locator
- Drought Monitor
- Reservoir Levels
- Geo-Spatial Lab
- Publications/Reports
- 13-tab Decision Support System

It also lists integrations/resources including OpenWeather, Open-Meteo, NASA GPM, Sentinel Hub EO Browser, ArcGIS Living Atlas, NASA Worldview, Bhuvan, Survey of India and Copernicus Emergency Management Service.

**Strategic consequence:**

Sentinel cannot claim differentiation from "bringing all disaster data onto one map." The AP government already has a strong example of that pattern.

Sentinel's differentiation should instead be:

```text
Existing systems
     ↓
Evidence normalization
     ↓
Situation model
     ↓
Impact + constraints
     ↓
AI-assisted option generation
     ↓
Deterministic feasibility checks
     ↓
Evidence + uncertainty
     ↓
Human approval
     ↓
Track decision/outcome
```

## 4. NDMA SACHET

SACHET is NDMA's CAP-based integrated alert system. The current portal states that it provides near-real-time dissemination using geo-intelligence, supports natural and man-made disasters, geo-targeted alerts, multiple languages, simultaneous dissemination, SMS, mobile app, browser notifications and an India CAP RSS feed. It identifies NDMA, IMD, CWC, INCOIS and FSI as participating source organizations.

**Use in Sentinel:** official alert input, not alert replacement.

**Integration question to validate before coding:** exact machine-readable feed contract, update cadence, licensing/terms, and whether an official integration endpoint is intended for third-party operational applications.

## 5. IMD

The official IMD API Management platform exposes a unified gateway for real-time observations, forecasts, warnings and specialized bulletins. It uses authenticated JWT access. As of the current page, new API registrations are temporarily on hold while a new API Usage and Pricing Policy is implemented.

**Design decision:** create an `IMDProvider` abstraction now, but don't make production deployment depend exclusively on obtaining a new IMD key. Keep a replay/static dataset adapter for development and evaluation.

## 6. CWC flood data

CWC's recent documentation describes a 7-day advisory flood forecast covering 20 major river basins, with 200 water-level and 138 reservoir-inflow forecast stations, updated every three hours. CWC also publishes short-range forecasts, medium-range advisories, current flood conditions, reservoir information and an inundation forecast service.

CWC's public material also describes the FloodWatch India app and web dissemination.

**Sentinel use:** consume official flood information and combine it with exposure, infrastructure, roads and resource constraints. Do not recreate CWC's hydrological model in v2.

## 7. INCOIS

INCOIS's ITEWS has a 24x7 warning centre and a real-time network of seismic stations, bottom-pressure recorders, tide gauges and other ocean observations. It uses scenario databases, vulnerability modelling, inundation maps and a decision-support system. The current portal explicitly exposes API/RSS feeds in its navigation.

**Sentinel use:** specialist evidence source. Treat INCOIS output as authoritative domain intelligence and add impact/response reasoning above it.

## 8. NASA FIRMS

FIRMS provides MODIS, VIIRS and Landsat active-fire data, with APIs and WMS/WFS/KML services. Global NRT active-fire data are available, and API access uses a MAP_KEY. FIRMS documentation warns that satellite-derived active-fire/thermal-anomaly detections have limited accuracy and should not be used alone for preservation of life/property decisions.

**This is an excellent example of the Sentinel evidence model:** ingest the detection, preserve its timestamp/sensor/confidence, cross-check with other evidence, and show limitations to the decision-maker.

## 9. Copernicus Sentinel-1 / CDSE

The Copernicus Data Space Ecosystem provides Sentinel-1 products and a STAC catalogue. The CDSE documentation describes STAC as a standardized spatiotemporal metadata layer for EO discovery and interoperability. Access to Copernicus data and processing services is designed as an open ecosystem, with registration/capacity requirements depending on service.

**Sentinel use:** use STAC to discover imagery, then retrieve only the spatial/temporal subset needed for an incident. Do not download huge global archives.

## 10. GloFAS / Copernicus Climate Data Store

GloFAS provides global ensemble forecasts of river discharge and related hydrological variables. CDS offers programmatic access through its API after account setup and dataset terms acceptance. Copernicus documentation warns that CDS handles very large volumes and recommends regional subsetting and request strategies.

**Sentinel use:** flood scenario/evidence source and evaluation benchmark; not a replacement for CWC in India.

## 11. OpenStreetMap / Overpass

OpenStreetMap is valuable for roads, buildings and points of interest. The public Overpass ecosystem is useful for prototype querying, but public instances have fair-use constraints and should not become Sentinel's production-scale data backend.

**Recommendation:**

- Prototype: Overpass / OSM extracts.
- Production: use a controlled OSM-derived database or an appropriate commercial/open provider, with local caching and update strategy.

## 12. OpenAQ

OpenAQ v3 provides public global air-quality data through a REST API with API-key authentication, including PM2.5, PM10, SO2, NO2, CO, O3, black carbon, humidity and temperature. It supports geospatial queries and historical/near-real-time measurements.

**Recommendation:** optional hazard/health context, not core v2 unless an air-quality use case is explicitly selected.

## 13. India Open Government Data

data.gov.in provides historical and government datasets including rainfall data. Dataset quality, update frequency and API availability are dataset-specific. Historical rainfall and disaster-damage data are useful for evaluation, scenario replay and model benchmarking even when they are not suitable for live operations.

**Recommendation:** build a replay/evaluation data layer separately from live ingestion.

## 14. Data architecture implication

Do not let the frontend call external sources directly.

Use provider adapters:

```text
Provider interfaces
 ├── AlertProvider
 │    ├── SACHET
 │    └── other CAP feeds
 ├── WeatherProvider
 │    ├── IMD
 │    └── fallback/replay
 ├── FloodProvider
 │    ├── CWC
 │    └── GloFAS
 ├── EOProvider
 │    ├── Sentinel-1/CDSE
 │    └── NASA FIRMS
 ├── GeoProvider
 │    ├── APSDMA ArcGIS
 │    ├── OSM
 │    └── local geodatabase
 └── AirQualityProvider
      └── OpenAQ
```

Every normalized observation should retain:

- source
- provider
- source record ID
- observed_at
- received_at
- valid_until, where available
- geometry
- data version/product
- confidence/quality flags
- provenance URL/reference
- freshness status

## 15. Reliability strategy

### Live
Use official/live provider adapters where access is stable.

### Replay
Every provider should have a recorded-fixture adapter for development and testing.

### Fallback
A provider outage should degrade gracefully rather than cause the whole incident pipeline to fail.

### Freshness
Every operational observation must have an explicit freshness state:

```text
FRESH
STALE
EXPIRED
UNKNOWN
```

### Conflicts
If sources disagree, Sentinel should surface the conflict instead of silently averaging them.

## 16. Cost strategy

The initial Sentinel research/prototype can be built predominantly with open/public data, but "free" does not mean "unlimited" or "operationally guaranteed."

Likely cost pressure points:

- LLM inference
- large EO processing
- managed geospatial databases/compute
- production routing
- commercial weather/geocoding providers if required
- enterprise GIS/services if integration moves beyond public APIs

The architecture should therefore make expensive providers replaceable.

## 17. Recommended v2 data priorities

### P0 — build around these first

1. APSDMA GIS/ArcGIS layers for India/AP infrastructure and operational context.
2. CWC flood monitoring/forecast information for the flood case.
3. SACHET/CAP official warning ingestion after contract validation.
4. OSM-derived road network for routing prototypes.
5. Historical data.gov.in datasets for replay/evaluation.

### P1 — add after the core loop works

6. IMD API adapter once access is available/confirmed.
7. Sentinel-1/CDSE SAR evidence.
8. GloFAS for independent/global flood context.
9. NASA FIRMS for wildfire.
10. INCOIS for coastal/tsunami scenarios.

### P2

11. OpenAQ and other environmental context.
12. Additional commercial or specialist feeds only when a concrete user job requires them.

## 18. Most important product consequence

The strongest new market insight is that **the map/data aggregation layer is not enough**, especially in Andhra Pradesh. APSDMA already has a very broad operational GIS/DSS surface.

Therefore Sentinel's core differentiation should be:

> **Turn heterogeneous authoritative evidence into auditable, constraint-aware response options and decision records.**

This makes the AI genuinely useful while allowing existing government systems to remain the source of authority.

## Sources

- NDMA SACHET: https://sachet.ndma.gov.in/
- IMD API Management: https://api.imd.gov.in/public/index.php
- CWC flood forecast appraisal: https://cwc.gov.in/sites/default/files/ffwnappraisal-report-2023.pdf
- CWC flood forecasting SOP: https://cwc.gov.in/sites/default/files/sopapril2025.pdf
- CWC hydro-meteorological observation: https://cwc.gov.in/hydro-meteorological-observation
- INCOIS ITEWS: https://tsunami.incois.gov.in/TEWS/searlywarnings.jsp
- APSDMA GIS Portal: https://apsdmagis.ap.gov.in/weather-watch/portal-home.html
- APSDMA ArcGIS Feature Services: https://apsdmagis.ap.gov.in/gisserver/rest/services/Hosted/APSDMA_Infra/FeatureServer/14
- NASA FIRMS: https://firms.modaps.eosdis.nasa.gov/active_fire/
- NASA FIRMS API: https://firms.modaps.eosdis.nasa.gov/api/
- Copernicus Sentinel-1: https://dataspace.copernicus.eu/data-collections/copernicus-sentinel-missions/sentinel-1
- Copernicus STAC: https://documentation.dataspace.copernicus.eu/APIs/STAC.html
- Copernicus CDS API: https://cds.climate.copernicus.eu/how-to-api
- GloFAS: https://ewds.climate.copernicus.eu/stac-browser/collections/cems-glofas-forecast
- OpenStreetMap API policy: https://operations.osmfoundation.org/policies/api/
- OpenStreetMap Overpass: https://wiki.openstreetmap.org/wiki/Overpass_API
- OpenAQ: https://docs.openaq.org/about/about
- India OGD rainfall: https://www.data.gov.in/catalog/rainfall-india
