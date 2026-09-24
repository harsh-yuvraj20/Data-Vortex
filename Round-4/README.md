# DATA VORTEX 2026 — ROUND 4: SOCIAL ENGINE REVIVAL
## Streamlit-First Integrated Social Intelligence Application

---

## 1. Project Overview

**Round 4: Social Engine Revival** unites the three preceding analytical rounds into a single, cohesive, production-grade interactive dashboard application. The system provides an executive lens into social media platform behavior, tracking the analytical lifecycle from forensic data restoration through dual-head NLP semantic comprehension to longitudinal anomaly mining.

```
                    SOCIAL ENGINE
                         │
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
       RECOVERY       SEMANTICS       SIGNALS
       Round 1         Round 2        Round 3
          │              │              │
          └──────────────┼──────────────┘
                         ↓
                  UNIFIED INSIGHTS
                      (Round 4)
```

---

## 2. Architecture & Layer Design

The application is structured into decoupled layers, separating business logic, data access, and presentation:

```
Round-4/
├── README.md                           # Project documentation & run guide
├── requirements.txt                    # Minimal pinned dependencies
├── .gitignore                          # Local Git ignore definitions
├── app.py                              # Top-level Streamlit controller & router
│
├── src/                                # Core application & analytical engine
│   ├── __init__.py
│   ├── utils.py                        # Path resolution, styling tokens, formatters
│   ├── data_loader.py                  # Cached multi-round data loading & read-only SQLite
│   ├── preprocessing.py                # Schema validation & text cleaning
│   ├── model.py                        # Deserialization & dual-head calibrated inference
│   ├── analysis.py                     # Trajectory, shifts (SS1/2), spikes (ES1-3), SQL challenges
│   ├── metrics.py                      # Scale KPIs, frozen benchmarks & evidence matrix
│   └── export_outputs.py               # Tabular results exporter
│
├── pages/                              # Streamlit multi-page application views
│   ├── 01_Overview.py                  # Page 1: Executive Overview & Recovery
│   ├── 02_Analysis.py                  # Page 2: Relational SQL, NLP & Temporal Evidence
│   ├── 03_Interactive_Explorer.py      # Page 3: Dynamic Exploration & Live Inference
│   └── 04_Methodology.py               # Page 4: Provenance, Models & Limitations
│
├── components/                         # UI component library
│   ├── __init__.py
│   ├── findings.py                     # Empirical takeaway cards & non-causality notices
│   ├── header.py                       # Unified page header with breadcrumbs
│   ├── sidebar.py                      # Navigation menu & system integrity diagnostics
│   ├── metric_cards.py                 # High-contrast KPI cards
│   ├── charts.py                       # Standardized Plotly research figures
│   ├── tables.py                       # Formatted Streamlit dataframe displays
│   └── filters.py                      # Reusable post filtering widgets
│
├── config/                             # Application configuration
│   ├── __init__.py
│   └── settings.py                     # Dynamic path resolution & UI style tokens
│
├── repositories/                       # Data access abstraction layer
│   ├── __init__.py
│   ├── sqlite_repository.py            # Safe read-only SQLite access (?mode=ro)
│   ├── dataset_repository.py           # Cached dataset loading & schema validation
│   └── model_repository.py             # Cached model pipelines & calibration inference
│
├── services/                           # Domain service abstraction layer
│   ├── __init__.py
│   ├── data_service.py                 # Multi-round scale metrics & post filtering
│   ├── round1_service.py               # Forensic recovery & canonical SQL queries (E2, M1, H2)
│   ├── nlp_service.py                  # Training distributions, benchmarks, live prediction
│   ├── round3_service.py               # Net sentiment trajectory, shifts (SS1/2), spikes (ES1-3)
│   └── insight_service.py              # Cross-round synthesis pillars & evidence matrix
│
├── utils/                              # Utility helpers
│   ├── __init__.py
│   ├── formatting.py                   # Number, date, and percent formatters
│   ├── logging_config.py               # Structured console logger
│   └── validation.py                   # Dataframe and model schema validators
│
├── data/
│   ├── README.md                       # Canonical data provenance guide
│   └── references/
│       └── README.md                   # Reference schema notes
│
├── models/
│   └── README.md                       # Model loading & calibration guide
│
├── outputs/
│   └── results/                        # Generated analytical CSV results (8 files)
│
├── tests/
│   ├── test_data.py                    # Dataset schema & row count tests
│   ├── test_analysis.py                # Analytical algorithms, shifts & SQL tests
│   └── test_app.py                     # Application module import & smoke tests
│
├── scripts/
│   └── validate_round4.py              # Automated 23-point audit script
│
├── reports/
│   ├── Round4_Technical_Report.pdf     # Validated PDF report
│   ├── Round4_Analytical_Report.pdf    # Validated PDF report
│   └── Round4_Dashboard_Documentation.pdf # Validated PDF report
│
├── notebooks/
│   └── Round4_Social_Engine_Revival.ipynb # Executed notebook
│
├── submission/
│   ├── Round4_Technical_Report.pdf
│   ├── Round4_Analytical_Report.pdf
│   ├── Round4_Dashboard_Documentation.pdf
│   ├── Round4_Social_Engine_Revival.ipynb
│   └── SUBMISSION_MANIFEST.txt
│
└── docs/
    ├── architecture.md                 # Detailed architecture specification
    ├── ROUND4_REQUIREMENTS.md          # Requirements mapping checklist
    ├── DATA_DICTIONARY.md              # Multi-round field dictionary
    ├── METHODOLOGY.md                  # Comprehensive technical methodology
    └── VALIDATION_REPORT.md            # Verification audit report
```

---

## 3. How Rounds 1–3 Feed Round 4

The application references existing canonical artifacts in-place without duplicating large files:

| Round | Canonical Artifact | Role in Round 4 |
| :--- | :--- | :--- |
| **Round 1 Phase 1** | `Social_Engine_Posts_Cleaned.csv` (12,000 rows)<br>`Social_Engine_Users_Cleaned.csv` (1,500 rows) | Provides base platform scale, user distributions, and cleaned engagement metrics. |
| **Round 1 Phase 2** | `data_vortex.db` (SQLite relational core) | Executed read-only via `sqlite_repository.py` for challenges E2, M1, and H2. |
| **Round 2** | `sentiment_label_pipeline.pkl`<br>`topic_category_pipeline.pkl` | Powers real-time semantic inference sandbox with frozen held-out benchmarks. |
| **Round 3** | `round3_recommendation_algorithm_reactions.csv` (204 rows) | Drives longitudinal sentiment trajectory, candidate shifts (SS1, SS2), and spikes (ES1–ES3). |

---

## 4. Local Installation & Setup

The application operates completely offline without external API keys, cloud databases, or remote endpoints.

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run Automated Validation Audit
```bash
python scripts/validate_round4.py
```

### Step 3: Launch Streamlit Dashboard
```bash
streamlit run app.py
```

---

## 5. Dashboard Navigation

The application provides 5 integrated navigation views via the Streamlit multi-page interface:

1. **Executive Home (`app.py`):** Executive landing page answering "What did we learn from the Social Engine?", displaying system-wide scale, cross-round data flow funnel, 15-year sentiment trajectory, and application roadmap.
2. **Overview (`pages/01_Overview.py`):** Audits Round 1 forensic reconstruction (100% recovery of 12,000 corrupted posts), platform volume distributions, forensic recovery logs, and four core synthesis pillars.
3. **Analysis (`pages/02_Analysis.py`):** Multi-round analytics covering canonical SQLite competition challenges (E2, M1, H2), Round 2 NLP held-out benchmarks, candidate shifts (SS1, SS2), and extreme engagement spikes (ES1–ES3).
4. **Interactive Explorer (`pages/03_Interactive_Explorer.py`):** Dynamic multi-attribute post filter and dual-head live NLP prediction sandbox with calibrated posterior probabilities, signed margin scores, and preset domain examples.
5. **Methodology (`pages/04_Methodology.py`):** Complete 4-phase technical documentation, data provenance inventory, model cards, calibration protocols, reproducibility guides, and non-causal disclosures.

---

## 6. Automated Testing

Run the full unit test suite covering data loaders, analytical calculations, and smoke imports:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

All 14 unit tests pass with zero errors across `test_data.py`, `test_analysis.py`, and `test_app.py` (accompanied by 23 passing audit checks in `scripts/validate_round4.py`).

---

## 7. Known Methodological Limitations

1. **Hacker News Demographic Bias:** Round 3 reaction records originate from public Hacker News submissions and reflect technical discussion norms rather than general population behavior.
2. **Historical Bounded Sample:** The Round 3 dataset is a historical archival sample (2011–2026), not a continuous live streaming feed.
3. **Non-Causality Principle:** Detected shifts (SS1, SS2) and engagement spikes (ES1, ES2, ES3) are empirical temporal correlations; algorithmic causality is strictly disclaimed.
4. **Missing Comment Scores:** Comment-level scores are absent by API design and excluded from aggregate engagement calculations rather than zero-imputed.
