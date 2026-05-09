# Foundation 2 — Define: Problem + Architecture
**Course:** CIDM 6330  
**Student:** Oluwakemi Innocent  
**Foundation:** 2 — Architecture Styles & Fit  
**Dataset:** BTS Airline On-Time Performance + BTS Carrier Lookup (optional airport reference)

---

## 1. Problem Definition

### Problem statement (committed)
I am building a system that **predicts the likelihood that a scheduled U.S. domestic flight will be delayed** based on known pre-departure factors such as **route (origin–destination), carrier, date/seasonality, and time-of-day**. The primary users are **operations analysts and planners** who need early signals of delay risk to improve planning (e.g., staffing, scheduling buffers, and contingency planning). This matters because delays create operational disruption and can cascade across routes and aircraft rotations.

### Why this problem (why I selected it)
During discovery, I observed that delay values are **unevenly distributed** and certain airports/carriers appear repeatedly in delay-heavy records. This suggests that delay risk is influenced by repeatable patterns (route, carrier, seasonality). I also noticed delay-cause fields can be sparse/inconsistent across records, which reinforced that the system should focus on **predictive features available consistently** rather than relying on complete cause attribution.

### Scope boundaries
**In scope**
- Monthly batch ingestion of BTS on-time performance CSVs
- Data cleaning, feature derivation (date features, route keys, time buckets)
- A prediction-oriented output: delay probability / risk score per flight record (or per route+time bucket)
- Evaluation metrics at a reporting level (basic accuracy/precision/recall or calibration indicators)

**Out of scope (for Foundation 2)**
- Real-time streaming ingestion and live operational alerts
- Advanced ML governance, model registry, distributed coordination
- Complex online feature stores or “always-on” inference serving
- Guaranteeing SLA-level latency (not yet established)

### Success criteria
The system is successful if:
- It produces a delay risk score (or probability) for flights using features known before departure
- Results are reproducible across runs and time windows
- Model performance meets a baseline threshold (e.g., improves over a naive baseline such as “always on-time” or “airport average”)
- Stakeholders can see simple explanations at an aggregate level (top drivers like route, carrier, seasonality), even if the model itself is not fully explainable yet
- The monthly pipeline completes within an acceptable batch window for the dataset size (e.g., within a few hours)

---

## 2. Data Pipeline Definition

### Data sources
- **BTS Airline On-Time Performance** monthly CSVs  
  Example fields: `FlightDate`, `Carrier` (or reporting airline), `Origin`, `Dest`, delay fields (`DepDelay`, `ArrDelay`), cancellation/diversion flags
- **BTS Carrier Lookup Table** to map carrier codes to carrier names
- Optional: airport reference dataset to enrich `Origin`/`Dest` codes with city/state/region

### Data relationships
- Join flight records to carrier lookup on the carrier code field (`Carrier` or equivalent)
- Route key: `(Origin, Dest)`; optionally also track direction separately
- Time keys: derive `month`, `day_of_week`, `season` from `FlightDate`
- If scheduled time fields exist, derive time-of-day bucket (morning/afternoon/evening/night)

### Transformation requirements
- Clean types and missing values (dates, carrier codes, airport codes)
- Create the target label:
  - `Delayed = 1` if departure delay > 15 minutes (common operational threshold), else `0`
- Feature engineering (pre-departure only):
  - route features: origin, destination, route pair
  - carrier features
  - time features: month, day of week, holiday/peak season proxy (optional)
  - historical aggregates (derived from prior periods): e.g., average delay rate for the route/carrier/month
- Split data into training vs evaluation by time (e.g., train on earlier months, evaluate on later months) to reflect real-world usage

### Output shape
- A curated dataset such as:
  - `clean_flight_events` (validated and enriched flight records)
  - `flight_delay_features` (model-ready features + label)
  - `delay_risk_scores` (prediction outputs)
- Delivered as CSV/parquet extracts for downstream consumers, and/or a simple API/report dataset for dashboarding

---

## 3. Architecture Characteristics — Driving and Implicit

### Driving characteristics (top 3)
1. **Evolvability**
   - Why critical: features and problem framing will change as we learn what signals are predictive and which fields are stable across time.
   - Measure: ability to add/modify features without rewriting the whole system; versioned feature pipeline; minimal breakage when schema changes.
   - If failed: system becomes brittle; each change becomes expensive and slows iteration.

2. **Data Consistency / Data Quality**
   - Why critical: incorrect joins (carrier/airport), inconsistent codes, or unvalidated target labels will produce misleading models.
   - Measure: validation checks (null rates, join coverage, schema checks), label correctness checks, anomaly detection on distributions.
   - If failed: predictions lose trust; “good-looking” model performance may be an artifact of bad data.

3. **Scalability**
   - Why critical: dataset is large, grows monthly, and includes long history; feature engineering and training datasets can become expensive.
   - Measure: pipeline runtime and resource usage remain acceptable as data grows; ability to process month partitions and rollups.
   - If failed: training/refresh cycles become too slow, reducing usefulness.

### Implicit characteristics (assumed, not differentiating)
- Basic reliability (reruns, idempotent outputs)
- Basic security (access control if needed)
- Basic maintainability (readable code, documented steps)

### Characteristic trade-offs
- **Evolvability vs Consistency**: allowing flexible features can weaken strict schema enforcement; I will keep strong validation for core fields while allowing feature extension in dedicated modules.
- **Scalability vs Data consistency checks**: heavy validation can slow processing; I will prioritize correctness checks on critical fields and sample-based profiling for non-critical checks.

What I am willing to sacrifice:
- I will sacrifice some ingestion speed (batch window) to maintain strong data validation and trustworthy labels/features.

---

## 4. Architecture Style Selection

### Selected style
**Pipeline architecture (batch ETL/feature pipeline)** implemented as a **modular monolith** with explicit pipeline stages.

### Why this style fits
- The work naturally flows through stages: ingest → validate → transform/features → train/evaluate → score → publish.
- Supports evolvability by allowing feature modules to be added without changing ingestion and validation logic.
- Supports data quality by making validation a first-class stage rather than an afterthought.
- Supports scalability by enabling partition-by-month processing and repeatable batch runs.

### Alternatives considered (and rejected)
- **Layered architecture only**: helps organize code, but does not explicitly model the end-to-end flow needed for feature creation and scoring.
- **Service-based/microservices**: premature; adds deployment complexity and coordination overhead without proven need in F2.
- **Event-driven streaming**: rejected because real-time requirements are not established and BTS data is naturally batch/monthly.

### Style-specific trade-offs
- Batch pipeline means predictions are refreshed on a schedule, not real-time.
- A modular monolith is simpler to deploy but may require refactoring later if the system grows into separate deployables.

### Quantum analysis
**Architecture quanta: 1**
- One deployable pipeline system with tightly coupled stages and shared data outputs. Multiple quanta would only be justified if online inference/service boundaries were required (not established here).

---

## 5. Component Identification

### Component inventory
1. **Ingestion component**
   - Responsibility: load monthly BTS CSVs into raw storage
   - Data: raw flight records (landing zone)

2. **Validation & Profiling component**
   - Responsibility: schema checks, missing values, join coverage checks, anomaly checks
   - Data: validation reports + run metadata

3. **Feature Engineering component**
   - Responsibility: derive labels and pre-departure features; build training tables
   - Data: `flight_delay_features`

4. **Training & Evaluation component**
   - Responsibility: train model on historical data; basic evaluation against baseline; store model artifact (local file)
   - Data: model artifact + evaluation metrics

5. **Scoring component**
   - Responsibility: apply model to produce risk scores for target period
   - Data: `delay_risk_scores`

6. **Publishing component**
   - Responsibility: export outputs for dashboarding/reporting/API consumption
   - Data: curated outputs

7. **Observability component**
   - Responsibility: logs, run status, validation outcomes, failure signals
   - Data: pipeline run logs/metadata

### Partitioning approach
**Domain partitioning by capability (pipeline stage)** because each stage has a single primary responsibility and the boundaries map directly to the data flow.

### Boundaries and cohesion
- Ingestion: functional cohesion
- Validation: functional cohesion
- Features: functional + sequential cohesion
- Train/Evaluate: functional cohesion
- Scoring: functional cohesion
- Publish: functional cohesion

---

## 6. AI Collaboration Log (Foundation 2)
(Also recorded in AI_LOG.md)

- Style selection dialogue: I used AI to compare pipeline vs layered vs service-based approaches and to pressure-test trade-offs. I rejected suggestions implying real-time streaming because that requirement is not established.
- Problem refinement: AI helped narrow from multiple candidate problems to one committed problem by forcing clarity on users, success criteria, and scope boundaries.
- Where AI was wrong/unhelpful: Generic “microservices” recommendations and assumptions about low-latency inference; I chose a batch pipeline modular monolith because it matches BTS monthly data and F2 scope.

---

## Submission Confirmation
I have reviewed this submission for clarity, completeness, and alignment with Foundation 2 requirements.
