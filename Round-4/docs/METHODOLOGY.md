# DATA VORTEX 2026 — ROUND 4: METHODOLOGY SPECIFICATION

**Document:** `docs/METHODOLOGY.md`  
**Milestone:** Round 4 — Social Engine Revival  
**Author:** Lead Engineering Agent  
**Methodological Standard:** End-to-End Scientific Rigor, Leakage Prevention, and Non-Causal Interpretation

---

## 1. Overview & System Synthesis Architecture

The objective of Round 4 is the holistic reconstruction of the Social Engine across five interconnected phases:

```
[Phase 1: Forensic Recovery] ──> [Phase 2: Relational SQL Core] ──> [Phase 3: Supervised NLP Modeling]
                                                                              │
                                                                              ▼
[Round 4: Synthesis & UI] <───────────────────────────────────── [Phase 4: Social Signal Dynamics]
```

Every stage establishes an immutable foundation for subsequent analytical layers.

---

## 2. Stage 1: Data Recovery & Forensic Cleaning (Round 1 Phase 1)

1. **Exact Deduplication:**
   - Forensic analysis identified exactly 1,000 exact duplicate post rows.
   - Exact duplicates were safely pruned, reducing 13,000 raw rows to exactly 12,000 unique records without altering analytical distributions.
2. **Sign Inversion Correction:**
   - Upstream corruption inverted numerical engagement metrics for a subset of records into negative integers.
   - Forensic confirmation verified that these values represented authentic positive engagement with corrupted sign bits; absolute values were restored rather than discarding valid rows.
3. **Missing Value Integrity:**
   - Missing likes reflect creator platform privacy settings rather than zero likes.
   - Rather than introducing synthetic imputation bias (mean/median/zero filling), missing likes are explicitly preserved as `NULL` and filtered appropriately in complete-engagement analyses.

---

## 3. Stage 2: Relational Database Architecture (Round 1 Phase 2)

1. **Schema Design & Integrity:**
   - The production SQLite database (`data_vortex.db`) models a normalized 1-to-many relationship: dimension table `users` (1,500 rows) and fact table `posts` (12,000 rows).
   - Foreign-key constraints enforce that every post references an authentic creator. PRAGMA integrity checks confirm 0 violations.
2. **Authoritative Analytical Challenges:**
   - **E2 (Most Engaged Posts):** Identifies top 10 posts based on complete engagement (`likes + shares + comments`) where `likes IS NOT NULL`.
   - **M1 (Location Engagement Aggregation):** Relational join aggregating post counts and total interaction volume by creator location, sorted descending.
   - **H2 (Rank Users Within Location):** Relational join and aggregation using `DENSE_RANK() OVER (PARTITION BY location ORDER BY total_engagement DESC)` to isolate the top 3 creators per location while preserving genuine ties.
3. **Read-Only Guarantee:**
   - All connections to the production database utilize SQLite URI syntax with `?mode=ro`. No write or mutating operations are executed.

---

## 4. Stage 3: Supervised Semantic Classification (Round 2)

1. **Leakage-Safe Partitioning:**
   - Exact and near-duplicate normalized text groups (987 groups totaling 2,087 rows) posed severe cross-partition leakage risks.
   - `GroupShuffleSplit` was utilized to isolate normalized text groups entirely within a single split (approximately 70% train, 10% validation, 20% held-out test). Group intersection between partitions was verified as exactly zero.
2. **Feature Representation:**
   - Text vectorization uses TF-IDF with word unigrams and bigrams (`ngram_range=(1, 2)`).
   - Raw casing, punctuation, and platform tokens (mentions, hashtags, URLs) were preserved to maintain subtle topical and emotional cues.
3. **Model Selection & Frozen Benchmarks:**
   - Evaluated candidate models (Majority Baseline, TF-IDF + Logistic Regression, TF-IDF + Linear SVM) using validation Macro F1.
   - **Sentiment Model (Primary Task):** TF-IDF + Logistic Regression won validation selection. Frozen held-out test metrics:
     - Accuracy: **0.5786**
     - Macro F1: **0.5795**
     - Weighted F1: **0.5800**
     - Probability Output: True calibrated probabilities via `predict_proba`.
   - **Topic Model (Secondary Task):** TF-IDF + Linear SVM won validation selection across 4 imbalanced categories. Frozen held-out test metrics:
     - Accuracy: **0.9264**
     - Macro F1: **0.5805**
     - Weighted F1: **0.9110**
     - Confidence Output: Raw decision function margins with an explicitly labeled softmax approximation (calibration honesty enforced).

---

## 5. Stage 4: Social Reaction Signal Analysis (Round 3)

1. **Historical Archive Ingestion:**
   - Reused the genuine public Hacker News archive export collected via Algolia API across an extensive 15-year observation window (February 2011 to September 2026).
   - Screened 389 raw records using recommendation/feed contextual criteria, yielding exactly 204 retained high-quality records.
2. **Monthly Sentiment Index:**
   - Defined mathematically as:
     $$\text{Sentiment Index} = \frac{\text{Positive} - \text{Negative}}{\text{Positive} + \text{Negative} + \text{Neutral}}$$
   - Bounded strictly within $[-1.0, +1.0]$.
3. **Documented Platform Entity Extraction:**
   - Case-insensitive gazetteer extraction across cleaned text for major platforms (YouTube, Twitter, Facebook, TikTok, Google, Instagram, Reddit, Netflix, Spotify, Meta, GitHub).
   - Strict context-aware regex matching for single-letter entity **X** (e.g., `twitter / x`, `on x`, `x's recommendation`) to prevent false-positive inflation.
4. **Candidate Shifts & Engagement Spikes:**
   - **SS1 (Candidate Shift 1):** 2025-09 to 2025-10 ($\Delta -0.80$, index $-0.20 \to -1.00$).
   - **SS2 (Candidate Shift 2):** 2024-10 to 2024-11 ($\Delta +0.80$, index $-1.00 \to -0.20$).
   - **ES1 (Engagement Spike 1):** March 2023 (1,704 points, 284.0x baseline) coinciding with Twitter recommendation code open-sourcing.
   - **Non-Causal Interpretation:** All detected events represent empirical temporal coincidence in public discussion; causal platform policy impacts are strictly disclaimed.

---

## 6. Stage 5: Interactive System & Dashboard Architecture (Round 4)

1. **Framework & Layout:**
   - Implemented in Python using Streamlit and Plotly.
   - Organized into 4 dedicated sections (`OVERVIEW`, `SOCIAL INTELLIGENCE`, `NLP INTELLIGENCE`, `INSIGHTS`).
2. **Dynamic Path Resolution:**
   - Dynamic `REPO_ROOT` detection resolves all paths relative to the workspace root. Zero machine-specific drive letters or user directories are permitted.
3. **Automated Verification:**
   - End-to-end unit, cross-file consistency, and visual QA automation verify that all displayed values reconcile identically across database tables, serialized models, reports, and notebooks.
