# DATA VORTEX 2026 — ROUND 4: OFFICIAL REQUIREMENTS SPECIFICATION

**Document:** `docs/ROUND4_REQUIREMENTS.md`  
**Milestone:** Round 4 — Social Engine Revival  
**Author:** Lead Engineering Agent  
**Build Scope:** Comprehensive Multi-Round Synthesis & Interactive System  
**Git Rule:** Zero Git write operations permitted.

---

## 1. Challenge Definition & Objective

- **Official Challenge Objective:** Deliver a unified, interactive analytical synthesis titled **SOCIAL ENGINE REVIVAL**, integrating all completed milestones of DATA VORTEX 2026.
- **Assigned Problem Topic:** Reconstruct the Social Engine by integrating:
  1. *Data Recovery & Forensics:* Cleaning, deduplicating, and restructuring corrupt social engagement records (Round 1 Phase 1).
  2. *Relational SQL Core:* Authoritative queries answering post engagement, location aggregation, and creator ranking challenges (Round 1 Phase 2).
  3. *Semantic NLP Understanding:* Supervised classification models for post sentiment and topic categorization (Round 2).
  4. *Social Reaction Signals:* Public reaction, temporal sentiment shifts, and engagement spikes regarding recommendation algorithm changes (Round 3).
  5. *Interactive Analytical Revival:* Production-ready interactive dashboard, reproducible execution notebook, and formal technical reports (Round 4).
- **Primary Source / Reference:** DATA VORTEX 2026 Official Competition Instructions & Round 1–3 Deliverables.

---

## 2. Canonical Dataset Requirements

| Dataset Identifier | Canonical File Path | Records | Source Milestone | Usage in Round 4 |
| :--- | :--- | :--- | :--- | :--- |
| **Cleaned Posts** | `Round-1/Phase-1/data/cleaned/Social_Engine_Posts_Cleaned.csv` | 12,000 | Round 1 Phase 1 | Platform activity, engagement distributions, and SQL source |
| **Cleaned Users** | `Round-1/Phase-1/data/cleaned/Social_Engine_Users_Cleaned.csv` | 1,500 | Round 1 Phase 1 | Relational creator attributes and location metadata |
| **Relational Database** | `Round-1/Phase-2/data/data_vortex.db` | 13,500 | Round 1 Phase 2 | SQLite read-only query execution (E2, M1, H2) |
| **NLP Labeled Posts** | `Round-2/data/Labeled_Social_NLP_Training_Data.csv` | 9,000 | Round 2 | Training class distributions (balanced sentiment & topic) |
| **Public HN Reactions** | `Round-3/data/processed/round3_recommendation_algorithm_reactions.csv` | 204 | Round 3 | Historical public reaction signals, sentiment index, and shift analysis |
| **Collection Metadata** | `Round-3/data/raw/collection_metadata.json` | — | Round 3 | Algolia API export parameters & query documentation |

*Rule:* Zero duplicate copies of raw or processed datasets within Round-4.

---

## 3. Mandatory Analysis & Methodology Requirements

1. **Cross-Round Volume & Provenance Tracking:**
   - Programmatically compute verified record counts across all stages (12,000 posts, 1,500 users, 9,000 training rows, 204 archive records).
   - Trace and verify data lineage from raw corruption to final structured synthesis.
2. **Relational Core Validation:**
   - Open `data_vortex.db` strictly with `?mode=ro`.
   - Validate SQLite database integrity (`PRAGMA integrity_check`) and foreign-key constraints (`PRAGMA foreign_key_check`).
   - Execute and render the three authoritative queries:
     - `E2 (Easy)`: Top 10 engaged posts (`likes + shares + comments`).
     - `M1 (Medium)`: Location engagement aggregation.
     - `H2 (Hard)`: Window function user ranking within location (`DENSE_RANK() <= 3`).
3. **Machine Learning Model Ingestion & Inference:**
   - Dynamically load canonical pipelines from `Round-2/models/`:
     - Sentiment: `sentiment_label_pipeline.pkl` (TF-IDF + Logistic Regression).
     - Topic: `topic_category_pipeline.pkl` (TF-IDF + Linear SVM).
   - Display frozen held-out test benchmarks:
     - Sentiment: 0.5795 Macro F1, 0.5786 Accuracy.
     - Topic: 0.5805 Macro F1, 0.9264 Accuracy.
   - Live Inference Engine:
     - Support arbitrary text input or one-click domain presets.
     - Validate non-empty input.
     - Return predicted sentiment with true calibrated probabilities (`predict_proba`).
     - Return predicted topic with raw decision scores and explicitly labeled softmax approximation (never fabricate confidence).
4. **Social Signal & Shift Analysis:**
   - Compute monthly sentiment index: $(Positive - Negative) / (Positive + Negative + Neutral)$.
   - Extract platform/product entity frequencies using documented gazetteer (YouTube, Twitter, Facebook, TikTok, etc.) with strict context regex for 'X'.
   - Review algorithmically detected candidate shifts (SS1, SS2) and engagement spikes (ES1, ES2, ES3).
   - Explicitly label all detections as descriptive temporal associations; causality is strictly disclaimed.

---

## 4. Dashboard Requirements

- **Technology:** Streamlit + Plotly.
- **Design Principles:** Minimalist research/analytics aesthetic, dark slate/navy typography, restrained indigo accent (`#1E3A8A`), white cards (`#FFFFFF`, 10px radius), subtle borders (`#E2E8F0`), zero neon/cyberpunk clutter.
- **Information Architecture (4 Primary Sections):**
  1. `OVERVIEW`: Title, subtitle, 5-stage pipeline breadcrumb, 4 verified KPI cards, data volume funnel chart, concise inventory table.
  2. `SOCIAL INTELLIGENCE`: Reactive filter panel (sentiment, entity, keyword, date range) with empty-state safety; 4 distinct tabs (Temporal Trends, Entity & Term Frequency, Detected Shifts, Engagement / Signals with expandable SQLite query execution).
  3. `NLP INTELLIGENCE`: Model benchmark cards, training distribution charts, live post analysis engine with preset buttons and calibration honesty.
  4. `INSIGHTS`: 4 synthesis cards (Data Integrity, Semantic Understanding, Social Signals, Engine Synthesis) and a prominent Methodology & Limitations callout.

---

## 5. Required Reports & Submission Artifacts

- **Reports (`Round-4/reports/`):**
  1. `Round4_Technical_Report.pdf`: System architecture, pipeline verification, zero-duplication data flow, and model loading.
  2. `Round4_Analytical_Report.pdf`: Empirical cross-round findings, SQL outputs, NLP benchmarks, social signals, and limitations.
  3. `Round4_Dashboard_Documentation.pdf`: Interactive UI documentation, information architecture, filter parameters, and execution manual.
- **Submission Package (`Round-4/submission/`):**
  1. `Round4_Technical_Report.pdf`
  2. `Round4_Analytical_Report.pdf`
  3. `Round4_Dashboard_Documentation.pdf`
  4. `Round4_Social_Engine_Revival.ipynb`
  5. `SUBMISSION_MANIFEST.txt`
- **Format Requirements:** All PDFs valid `%PDF`, < 10 MB. Notebook executed top-to-bottom with 0 errors.

---

## 6. Prohibited Approaches & Constraints

- [x] **No Git Operations:** Do NOT commit, push, stage, rebase, or mutate Git history.
- [x] **No Hardcoded Machine Paths:** Zero occurrences of `C:\Users\`, `D:\`, `/home/`, etc.
- [x] **No Data Duplication:** Do not copy raw datasets or model pickle files into Round-4.
- [x] **No Unverified / Fabricated Metrics:** Every metric must directly reconcile to canonical source files.
- [x] **No Causal Claims:** Strictly distinguish empirical temporal coincidence from causation.
