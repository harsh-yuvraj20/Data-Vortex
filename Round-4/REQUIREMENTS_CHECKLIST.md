# DATA VORTEX 2026 — ROUND 4: REQUIREMENTS CHECKLIST

**Project:** DATA VORTEX 2026  
**Round:** Round 4 — Social Engine Revival  
**Working Document:** Requirements Mapping & Compliance Checklist  
**Operating Constraint:** Zero Git write operations (`git add`, `git commit`, `git push`, history mutation are strictly forbidden).

---

## 1. Challenge & Objective Mapping

- [x] **Primary Objective:** Deliver an interactive, research-grade synthesis of DATA VORTEX Rounds 1–3 titled **SOCIAL ENGINE REVIVAL**.
- [x] **Core Theme:** "Reconstructing the Social Engine through data, language and social signals."
- [x] **Analytical Progression:**
  - *Stage 1 (Data Recovery):* Forensic deduplication and sign inversion correction (Round 1 Phase 1).
  - *Stage 2 (SQL Intelligence):* Relational core analysis and queries E2, M1, H2 on SQLite (Round 1 Phase 2).
  - *Stage 3 (NLP Classification):* Supervised sentiment and topic modeling (Round 2).
  - *Stage 4 (Social Signals):* Public reaction and descriptive shift detection on algorithm changes (Round 3).
  - *Stage 5 (Synthesis):* Integrated interactive dashboard and technical deliverables (Round 4).

---

## 2. Canonical Data & Model Asset Dependencies

- [x] **Round 1 Posts:** `Round-1/Phase-1/data/cleaned/Social_Engine_Posts_Cleaned.csv` (12,000 rows).
- [x] **Round 1 Users:** `Round-1/Phase-1/data/cleaned/Social_Engine_Users_Cleaned.csv` (1,500 rows).
- [x] **Round 1 Database:** `Round-1/Phase-2/data/data_vortex.db` (opened strictly in read-only mode `?mode=ro`).
- [x] **Round 2 Labeled Data:** `Round-2/data/Labeled_Social_NLP_Training_Data.csv` (9,000 rows).
- [x] **Round 2 Sentiment Model:** `Round-2/models/sentiment_label_pipeline.pkl` (TF-IDF + Logistic Regression).
- [x] **Round 2 Topic Model:** `Round-2/models/topic_category_pipeline.pkl` (TF-IDF + Linear SVM).
- [x] **Round 3 Processed Dataset:** `Round-3/data/processed/round3_recommendation_algorithm_reactions.csv` (204 rows).
- [x] **Round 3 Metadata:** `Round-3/data/raw/collection_metadata.json`.
- [x] **Zero Duplication Policy:** No copies of previous-round CSVs, SQLite databases, or pickled models inside Round-4.
- [x] **Zero Machine-Specific Paths:** All paths resolve dynamically relative to the repository root.

---

## 3. Dashboard Information Architecture (4 Core Sections)

### Section 1: OVERVIEW
- [x] Title: `SOCIAL ENGINE REVIVAL`.
- [x] Subtitle: `"Reconstructing the Social Engine through data, language and social signals."`
- [x] Visual pipeline: `DATA RECOVERY` → `SQL INTELLIGENCE` → `NLP CLASSIFICATION` → `SOCIAL SIGNALS` → `ROUND 4 SYNTHESIS`.
- [x] Verified high-value KPI cards:
  - Round 1 Cleaned Posts: 12,000
  - Round 1 Users: 1,500
  - Round 2 Training Records: 9,000
  - Round 3 Retained Records: 204
- [x] Compact cross-round data volume visualization (Funnel / Stage Volume).
- [x] Concise inventory table: `Round | Source | Records | Purpose`.

### Section 2: SOCIAL INTELLIGENCE
- [x] Filters: Sentiment (`All`, `Positive`, `Negative`, `Neutral`), Platform Entity (`All`, `YouTube`, `Twitter`, etc.), Keyword search, Date range slider.
- [x] Tab 1 (Temporal Trends): Monthly Sentiment Index $(Positive - Negative) / Total$ line chart and stacked sentiment distribution bar chart.
- [x] Tab 2 (Entity & Term Frequency): Entity frequency horizontal bar chart with documented gazetteer methodology and top domain terms via Round 3 TF-IDF.
- [x] Tab 3 (Detected Shifts): Candidate shifts SS1 and SS2 review cards with period before/after, index change, sample size, magnitude, and contextual notes (explicitly labeled descriptive, not causal).
- [x] Tab 4 (Engagement / Signals): Engagement spike candidates ES1, ES2, ES3 with time period, observed engagement, baseline, calculable ratio, observations count, and source context.
- [x] Compact SQL Relational Core: Interactive execution of authoritative queries E2, M1, and H2 against `data_vortex.db` in SQLite read-only mode.

### Section 3: NLP INTELLIGENCE
- [x] Model 1: Sentiment classification (TF-IDF + Logistic Regression).
- [x] Model 2: Topic classification (TF-IDF + Linear SVM).
- [x] Verified evaluation metrics from Round 2 held-out benchmarks.
- [x] Live Post Analysis:
  - Text area for arbitrary text input.
  - 4 domain preset example buttons.
  - Non-empty validation.
  - Live prediction execution using canonical models.
  - Predicted sentiment with probability distribution.
  - Predicted topic with decision score margins and explicitly labeled softmax approximation.
  - Graceful error handling.

### Section 4: INSIGHTS & SYNTHESIS
- [x] 4 Synthesis Cards:
  1. Data Integrity (Round 1 deduplication, sign inversion correction, SQLite relational integrity).
  2. Semantic Understanding (Round 2 GroupShuffleSplit, performance boundaries).
  3. Social Signals (Round 3 negative sentiment skew, descriptive shifts, Twitter source spike).
  4. Engine Synthesis (Round 4 unified architecture, zero duplication, auditable provenance).
- [x] Prominent "METHODOLOGY & LIMITATIONS" callout:
  - Hacker News technical community demographic bias.
  - Historical archive sample (Feb 2011 to Sep 2026), not a continuous live stream.
  - Sample size constraints on monthly cohorts.
  - Missing comment scores handled without distortion.
  - Empirical temporal association vs. causality strictly preserved.

---

## 4. Engineering & Code Structure

- [x] `Round-4/src/utils.py`: Dynamic repository root resolver, canonical path constants, Plotly research theme.
- [x] `Round-4/src/data_loader.py`: Cached loading functions for previous-round assets.
- [x] `Round-4/src/analysis.py`: Canonical SQL queries (E2, M1, H2), temporal signal shifts, and post filtering.
- [x] `Round-4/src/model.py`: Dynamic model loading and live dual-head inference engine.
- [x] `Round-4/src/metrics.py`: Cross-round scale metrics, model benchmarks, and synthesis evidence matrix.
- [x] `Round-4/app.py`: Clean Streamlit dashboard.
- [x] `Round-4/requirements.txt`: Minimal pinned dependencies.

---

## 5. Deliverables & Submission Package

- [x] **Notebook:** `Round-4/notebooks/Round4_Social_Engine_Revival.ipynb` demonstrating the complete pipeline top-to-bottom.
- [x] **PDF Reports:**
  - `Round-4/reports/Round4_Technical_Report.pdf` (Methodology, architecture, and pipeline validation).
  - `Round-4/reports/Round4_Analytical_Report.pdf` (Empirical findings across all 4 stages).
  - `Round-4/reports/Round4_Dashboard_Documentation.pdf` (Interactive UI user guide and architecture).
- [x] **Submission Package:** `Round-4/submission/` containing final submission artifacts and `SUBMISSION_MANIFEST.txt`.
- [x] **Final Audit Report:** `Round-4/FINAL_AUDIT.md`.
