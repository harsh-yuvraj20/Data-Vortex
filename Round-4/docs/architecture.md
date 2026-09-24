# DATA VORTEX 2026 — ROUND 4: ARCHITECTURE SPECIFICATION

## 1. Architectural Philosophy: Streamlit-First Full-Stack Design

The **Round 4 Social Engine Revival** application is engineered as a clean, modular Python/Streamlit system that adheres to enterprise software engineering standards. While running as a single, zero-dependency Python process (`streamlit run app.py`), it strictly decouples business logic, data access, presentation, and domain validation.

```
                    ┌─────────────────────────┐
                    │      Streamlit UI       │
                    │   (Browser Viewport)    │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │      Controller         │
                    │       (app.py)          │
                    └────────────┬────────────┘
                                 │
           ┌─────────────────────┼─────────────────────┐
           │                     │                     │
┌──────────▼──────────┐ ┌────────▼──────────┐ ┌────────▼──────────┐
│  Presentation Layer │ │   Component Layer │ │  Settings/Config  │
│  (Round-4/pages/)   │ │(Round-4/compone...│ │(Round-4/config/...)│
└──────────┬──────────┘ └────────┬──────────┘ └───────────────────┘
           │                     │
           └──────────┬──────────┘
                      │
           ┌──────────▼──────────┐
           │    Service Layer    │
           │ (Round-4/services/) │
           └──────────┬──────────┘
                      │
           ┌──────────▼──────────┐
           │  Repository Layer   │
           │ (Round-4/reposit...)│
           └──────────┬──────────┘
                      │
   ┌──────────────────┼──────────────────┐
   │                  │                  │
┌──▼──────────────┐ ┌─▼────────────────┐ ┌▼────────────────┐
│ SQLite Database │ │ Canonical CSVs   │ │ Scikit Pipelines│
│ (data_vortex.db)│ │ (Rounds 1, 2, 3) │ │ (Round-2 Models)│
└─────────────────┘ └──────────────────┘ └─────────────────┘
```

---

## 2. Layer Descriptions

### 2.1 Configuration Layer (`config/settings.py` & `src/utils.py`)
- **Dynamic Path Resolution:** Inspects parent hierarchies to determine `REPO_ROOT` dynamically, completely eliminating machine-specific absolute drive letters (`C:\`, `D:\`).
- **Canonical Pointers:** Defines immutable path constants to Round 1, 2, and 3 assets.
- **Visual Design System:** Standardizes Plotly themes, color tokens (Navy `#1E3A8A`, Teal `#0D9488`, Slate `#0F172A`), and typography.

### 2.2 Core Application & Analytics Engine (`src/`)
- **`src/utils.py`:** Machine-independent path resolution, palette tokens, and standard formatting helpers.
- **`src/data_loader.py`:** Utilizes `@st.cache_data` to load tabular records across Rounds 1, 2, and 3, enforcing row count and column presence checks with immutable read-only SQLite connectivity (`?mode=ro`).
- **`src/preprocessing.py`:** Schema and volume validation functions and text sanitizers.
- **`src/model.py`:** Employs `@st.cache_resource` to deserialize trained scikit-learn pipelines in memory. Implements dual-head inference with strict calibration isolation (probabilities for Logistic Regression vs. decision scores for Linear SVM).
- **`src/analysis.py`:** Net Sentiment Index trajectory calculations, target entity gazetteer extraction, candidate shift/spike records, and SQL challenge execution (E2, M1, H2).
- **`src/metrics.py`:** Computes cross-round scale counts, frozen held-out test benchmarks, and narrative synthesis pillars.
- **`src/export_outputs.py`:** Generates verified tabular CSV exports into `outputs/results/`.

### 2.3 Data Access & Repository Layer (`repositories/`)
- **`sqlite_repository.py`:** Manages safe read-only connections (`file:...?mode=ro`) to `Round-1/Phase-2/data/data_vortex.db`. Restricts queries strictly to `SELECT` and `WITH`. Contains canonical implementations of challenges `E2`, `M1`, and `H2`.
- **`dataset_repository.py`:** Cached access to tabular records across Rounds 1, 2, and 3, enforcing schema validation via `utils.validation`.
- **`model_repository.py`:** Cached model pipelines and calibrated scoring.

### 2.4 Domain Service Layer (`services/`)
- **`data_service.py`:** Aggregates cross-round platform scale, handles interactive post filtering, and computes engagement statistics.
- **`round1_service.py`:** Manages forensic data recovery reconciliation, follower vs. engagement analysis, and SQL query execution.
- **`nlp_service.py`:** Presents training class distributions, held-out evaluation benchmarks, and live inference sandbox logic.
- **`round3_service.py`:** Calculates monthly Net Sentiment Index $(Pos - Neg)/Total$, tracks candidate shifts SS1 & SS2, and engagement spikes ES1–ES3.
- **`insight_service.py`:** Synthesizes the 4 cross-round executive narrative pillars and verification evidence matrix.

### 2.5 UI Component Library (`components/`)
- **`findings.py`:** Standardized empirical finding callout cards and mandatory non-causality notices (actively imported by all pages).
- **`header.py`:** Unified page header with breadcrumbs.
- **`sidebar.py`:** Navigation menu & system integrity diagnostics.
- **`metric_cards.py`:** High-contrast KPI cards.
- **`charts.py`:** Standardized Plotly research figures.
- **`tables.py`:** Formatted Streamlit dataframe displays.
- **`filters.py`:** Reusable interactive post filtering widgets.

### 2.6 Page Layer (`app.py` & `pages/`)
Five cohesive, narrative-driven views:
1. `app.py`: Executive Home (Landing summary answering "What did we learn from the Social Engine?", system scale KPIs, funnel chart, 15-year trajectory, roadmap).
2. `pages/01_Overview.py`: Executive Overview & System Recovery (platform distributions, forensic recovery logs, 4 synthesis pillars).
3. `pages/02_Analysis.py`: Relational SQL, NLP & Temporal Evidence (challenges E2/M1/H2, dual-head benchmarks, shifts SS1/SS2, spikes ES1–ES3).
4. `pages/03_Interactive_Explorer.py`: Dynamic Exploration & Live Inference (multi-attribute post filter, dual-head live NLP prediction sandbox with presets).
5. `pages/04_Methodology.py`: Methodology, Architecture, and Provenance (4-phase lifecycle, verification matrix, model cards, calibration standards, non-causal disclosures).

### 2.7 Automated Test Suite (`tests/`)
- `tests/test_data.py`: Dataset schema, row counts, and SQLite database integrity checks.
- `tests/test_analysis.py`: Net sentiment trajectory bounds, candidate shifts SS1/SS2, spikes ES1–ES3, and SQL challenge execution.
- `tests/test_app.py`: Module import verification, page loading smoke tests, and calibrated inference execution.

---

## 3. Data Integrity & Non-Causality Rules

1. **Zero Data Duplication:** Previous-round datasets, databases, and `.pkl` models are referenced in place. No binary copies exist in Round-4.
2. **Strict Calibration Honesty:** Posterior probabilities are reported only when produced by calibrated models (`predict_proba`). SVM hyperplane margins are explicitly labeled as decision scores with separate softmax approximations.
3. **Disclaimed Causality:** Temporal shifts (SS1, SS2) and engagement spikes (ES1–ES3) are framed purely as empirical observations within a bounded historical archive sample, with explicit disclosures that observational signals do not establish algorithmic causation.
