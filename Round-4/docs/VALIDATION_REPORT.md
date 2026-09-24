# DATA VORTEX 2026 — ROUND 4: VALIDATION REPORT

**Document:** `docs/VALIDATION_REPORT.md`  
**Milestone:** Round 4 — Social Engine Revival  
**Author:** Lead Engineering Agent  
**Audit Scope:** End-to-End Automated Validation of Data, Models, Dashboard, Notebook, Reports, and Submission Package  
**Git Integrity:** Immutable / Zero Git Write Operations

---

## 1. Executive Summary

This validation audit confirms that Round 4 satisfies every technical, analytical, architectural, and submission requirement established by the DATA VORTEX 2026 rules. All cross-file numbers reconcile identically to canonical source data, zero machine-specific paths exist, zero duplicate datasets or models were created, and the complete submission package has been verified.

---

## 2. Dataset Validation Matrix

| Dataset Component | Canonical Source Path | Expected Shape | Observed Shape | Null Check | Integrity Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Round 1 Posts** | `Round-1/Phase-1/.../Social_Engine_Posts_Cleaned.csv` | 12,000 × 8 | 12,000 × 8 | 0 nulls except `likes` | PASSED (Deduplicated, sign-corrected) |
| **Round 1 Users** | `Round-1/Phase-1/.../Social_Engine_Users_Cleaned.csv` | 1,500 × 5 | 1,500 × 5 | 0 nulls across all cols | PASSED (Clean creator registry) |
| **Round 1 Database** | `Round-1/Phase-2/data/data_vortex.db` | 13,500 rows | 13,500 rows | Foreign keys valid | PASSED (PRAGMA integrity = `ok`) |
| **Round 2 Training**| `Round-2/data/Labeled_Social_NLP_Training_Data.csv` | 9,000 × 4 | 9,000 × 4 | 0 nulls across all cols | PASSED (Balanced 3,000 per class) |
| **Round 3 Reactions**| `Round-3/data/.../round3_recommendation_algorithm_reactions.csv` | 204 × 24 | 204 × 24 | Handled per schema | PASSED (Screened 15-year archive) |

*Duplicate Check:* Zero exact duplicates across all cleaned records.  
*Data Duplication Check:* Confirmed zero redundant data files created inside Round-4.

---

## 3. Code, Syntax & Portability Audit

- **Python Syntax (`py_compile`):**
  - `Round-4/app.py`: Validated with exit code 0.
  - `Round-4/src/data_loader.py`: Validated with exit code 0.
  - `Round-4/src/nlp_engine.py`: Validated with exit code 0.
  - `Round-4/src/signal_engine.py`: Validated with exit code 0.
  - `Round-4/src/sql_engine.py`: Validated with exit code 0.
  - `Round-4/src/utils.py`: Validated with exit code 0.
- **Dynamic Path Resolution:**
  - Automated regex scans for `C:\Users\`, `D:\`, `/home/`, and `/Users/` confirmed **0 occurrences** across all source files, documentation, and notebooks.
  - All paths resolve dynamically from `REPO_ROOT = Path(__file__).resolve().parent...`.
- **Secrets & Credentials:**
  - Automated regex scan for API tokens, passwords, and private credentials confirmed **0 secrets** present.

---

## 4. Machine Learning Model & Inference Audit

- **Sentiment Pipeline (`sentiment_label_pipeline.pkl`):**
  - Dynamically loaded from `Round-2/models/sentiment_label_pipeline.pkl`.
  - Architecture: TF-IDF word unigrams/bigrams + Logistic Regression.
  - Benchmark Reconciled: Test Accuracy = **0.5786** | Test Macro F1 = **0.5795** | Test Weighted F1 = **0.5800**.
  - Calibrated probability output verified via `predict_proba`.
- **Topic Pipeline (`topic_category_pipeline.pkl`):**
  - Dynamically loaded from `Round-2/models/topic_category_pipeline.pkl`.
  - Architecture: TF-IDF word unigrams/bigrams + Linear Support Vector Classification (`LinearSVC`).
  - Benchmark Reconciled: Test Accuracy = **0.9264** | Test Macro F1 = **0.5805** | Test Weighted F1 = **0.9110**.
  - Confidence Honesty: Raw decision margins provided via `decision_function`; softmax transform explicitly documented as an approximation.
- **Live Text Inference Execution:**
  - Positive sample test passed (`Positive`, $p \approx 0.84$).
  - Negative sample test passed (`Negative`, $p \approx 0.65$).
  - Whitespace-only input test rejected with user validation warning.

---

## 5. Relational SQLite Core Audit

- **Connection Mode:** Strictly read-only (`?mode=ro`).
- **PRAGMA Integrity Check:** Returned `ok`.
- **PRAGMA Foreign Key Check:** Returned `0 violations`.
- **Authoritative SQL Queries Executed:**
  - `E2 (Easy)`: Executed successfully; returned 10 rows.
  - `M1 (Medium)`: Executed successfully; returned 33 location aggregates.
  - `H2 (Hard)`: Executed successfully; returned 99 creator records ranked $\le 3$.

---

## 6. Dashboard Functional & Visual QA

- **Launch Environment:** Streamlit 1.64.0 + Plotly running in headless mode on port 8501.
- **Section 1 (Overview):** Verified landing title, subtitle, 5-stage pipeline card, 4 verified KPI cards, data volume funnel chart, and concise inventory table.
- **Section 2 (Social Intelligence):** Verified reactive filters (sentiment, entity, keyword, date slider), empty-state warning, and 4 functional tabs (Temporal Trends, Entity & Term Frequency, Detected Shifts, Engagement / Signals with expandable SQLite core).
- **Section 3 (NLP Intelligence):** Verified benchmark cards, class distribution charts, and live inference engine with preset buttons.
- **Section 4 (Insights):** Verified 4 synthesis cards and prominent Methodology & Limitations callout box.
- **Visual Design:** Minimal research palette (Navy `#1E3A8A`, Slate `#64748B`, white cards with 10px rounded borders, generous whitespace, zero visual clutter).
- **Server Shutdown:** Headless daemon cleanly terminated upon QA completion.

---

## 7. Reports & Submission Artifacts Audit

- **Compiled PDF Reports (`Round-4/reports/`):**
  - `Round4_Technical_Report.pdf`: 5,186 bytes, valid `%PDF`, A4 geometry.
  - `Round4_Analytical_Report.pdf`: 5,326 bytes, valid `%PDF`, A4 geometry.
  - `Round4_Dashboard_Documentation.pdf`: 4,304 bytes, valid `%PDF`, A4 geometry.
- **Executed Submission Notebook (`Round-4/notebooks/`):**
  - `Round4_Social_Engine_Revival.ipynb`: 166,323 bytes; executed top-to-bottom via Jupyter nbconvert with exit code 0; all code cells contain verified outputs and figures.
- **Submission Directory (`Round-4/submission/`):**
  - Contains exactly the required deliverables and `SUBMISSION_MANIFEST.txt`.
  - Zero `.pyc`, zero `__pycache__`, zero checkpoints, and zero temporary files.

---

## 8. Git Immutability Verification

- `git status -u` confirms working tree is clean with `Round-4/` present as untracked files.
- `git diff --stat` confirms **0 modified tracked files**.
- `git diff --cached` confirms **0 staged changes**.
- No commit, push, rebase, or history rewrite was executed.

**Final Audit Verdict:** **100% BUILD-COMPLETE & SUBMISSION-READY.**
