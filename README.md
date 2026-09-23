# DATA VORTEX 2026

## Repository Purpose

This repository houses the complete, validated, and reproducible deliverables for the **DATA VORTEX 2026** analytics and machine learning competition. It organizes the project into three distinct competition rounds, maintaining strict data governance, relational integrity, machine learning reproducibility, and historical audit trails.

---

## Directory Structure Overview

```text
DATA-VORTEX/
│
├── README.md                                 # Root repository documentation (this file)
├── .gitignore                                # Git ignore rules for caches, runtimes, and temp files
│
├── Round-1/
│   ├── Phase-1/                              # Data recovery, forensic analysis, cleaning, and EDA
│   │   ├── data/
│   │   │   ├── raw/                          # Original supplied raw data (read-only provenance)
│   │   │   └── cleaned/                      # Verified cleaned datasets
│   │   ├── src/
│   │   │   └── clean_data.py                 # Deterministic data cleaning pipeline
│   │   ├── notebooks/                        # Inspection, forensic, cleaning, and EDA notebooks
│   │   ├── outputs/
│   │   │   ├── summaries/                    # Inspection and forensic summary CSVs
│   │   │   └── figures/                      # 12 publication-quality EDA figures
│   │   ├── reports/                          # Audit logs, reconciliation, and full EDA report
│   │   └── README.md
│   │
│   └── Phase-2/                              # Authoritative analytical SQL challenges (E2, M1, H2)
│       ├── data/
│       │   └── data_vortex.db                # SQLite 3 production relational database
│       ├── sql/
│       │   ├── 01_schema.sql                 # DDL schema definition with constraints and indexes
│       │   └── 02_load_and_validation.sql    # Relational integrity and assertion suite
│       ├── src/
│       │   ├── load_sqlite.py                # Automated database ingestion from cleaned data
│       │   └── build_phase2_submission.py    # Authoritative submission and report generator
│       ├── submission/                       # Upload-ready submission package
│       │   ├── Data_Vortex_Phase2_SQL_Queries.pdf
│       │   ├── Easy_Output.jpeg
│       │   ├── Medium_Output.jpeg
│       │   ├── Hard_Output.jpeg
│       │   ├── Data_Vortex_Phase2_Logic_Explanation.pdf
│       │   ├── Data_Vortex_Phase2_Insight_Report.pdf
│       │   └── SUBMISSION_MANIFEST.txt
│       └── README.md
│
├── Round-2/                                  # Supervised NLP pipelines (Sentiment & Topic classification)
│   ├── data/
│   │   └── Labeled_Social_NLP_Training_Data.csv
│   ├── src/
│   │   └── round2/                           # Modular preprocessing, training, and evaluation
│   ├── run_round2.py                         # End-to-end pipeline execution and validation script
│   ├── notebooks/
│   │   └── Round2_NLP_Model.ipynb            # Fully executed modeling notebook with outputs
│   ├── models/
│   │   ├── sentiment_label_pipeline.pkl      # Canonical primary sentiment model (TF-IDF + LogReg)
│   │   └── topic_category_pipeline.pkl       # Preserved secondary topic model (TF-IDF + LinearSVC)
│   ├── reports/
│   │   ├── Round2_Evaluation_Metrics.pdf     # Per-class metrics and confusion matrices
│   │   └── Round2_Technical_Report.pdf       # Comprehensive methodology and architecture report
│   ├── README.md
│   └── requirements.txt
│
└── Round-3/                                  # Real-world public discourse analysis (Hacker News)
    ├── data/
    │   ├── raw/
    │   │   ├── collection_metadata.json      # Provenance metadata and query terms
    │   │   └── hn_recommendation_algorithm_reactions_raw.csv
    │   └── processed/
    │       └── round3_recommendation_algorithm_reactions.csv # 204 final retained analytical records
    ├── src/                                  # Ingestion, preprocessing, and analytical modules
    ├── notebooks/
    │   └── Round3_Real_Time_Analysis.ipynb   # Executed analysis notebook with visualizations
    ├── reports/
    │   ├── Round3_Real_Time_Analysis_Notebook.pdf
    │   └── Round3_Analytical_Report.pdf      # Detailed analytical report
    ├── README.md
    └── requirements.txt
```

---

## Round-by-Round Summary

### Round 1: Phase 1 — Data Recovery and Exploratory Data Analysis
- **Scope:** Ingestion of supplied corrupted Social Engine data (`Social_Engine_Users.csv` and `Social_Engine_Posts_Corrupted.csv`), forensic corruption diagnosis, audit logging, deterministic cleaning, and exhaustive exploratory analysis across user demographics, engagement distributions, and temporal trends.
- **Key Artifacts:** Cleaned CSVs in `Round-1/Phase-1/data/cleaned/`, cleaning script `clean_data.py`, 6 inspection/EDA notebooks, 12 EDA figures, and comprehensive forensic audit reports.
- **Strict Governance:** Raw data is strictly read-only; missing values in optional fields are preserved without imputation; negative likes are corrected via confirmed sign inversion; duplicates are removed cleanly.

### Round 1: Phase 2 — Relational Database & Analytical SQL Challenges
- **Authoritative Challenges:**
  - **Easy (E2):** *Most Engaged Posts* — Top 10 posts ranked by total engagement (`likes + shares + comments`), filtering out missing likes.
  - **Medium (M1):** *Which Locations Generate the Most Engagement?* — Aggregated post counts and total engagement per user location across 33 global locations.
  - **Hard (H2):** *Rank Users Within Their Location* — Window-function ranking (`DENSE_RANK()`) isolating the top 3 users per location.
- **Database Engine:** Embedded SQLite 3 (`data/data_vortex.db`) with full foreign key constraints and optimized indexes.
- **Submission Artifacts:** Consolidated SQL query PDF, execution output JPEGs for Easy, Medium, and Hard, Logic Explanation PDF, Insight Report PDF, and submission manifest.

### Round 2: Supervised Natural Language Processing
- **Scope:** Text classification on 9,000 labelled social posts. Primary task: 3-class sentiment prediction (`Positive`, `Neutral`, `Negative`). Secondary task: 5-class topic categorization.
- **Architecture:** Group-aware train/validation/test split preventing duplicate-text leakage, TF-IDF n-gram vectorization, and class-weighted Logistic Regression (primary) and Linear SVM (secondary).
- **Deliverables:** Fully executed `Round2_NLP_Model.ipynb`, serialised pipelines (`sentiment_label_pipeline.pkl`, `topic_category_pipeline.pkl`), evaluation metrics PDF, and technical report PDF.

### Round 3: Real-Time / Historical Public Reaction Analysis
- **Assigned Topic:** *Public Reaction to Changes in the Recommendation Algorithm*.
- **Data Source:** Genuine public Hacker News archive export via the Algolia archive API, filtered using documented recommendation/feed context plus explicit change/reaction signals to yield 204 canonical records.
- **Methodology:** Ingests the single canonical Round 2 sentiment model to evaluate sentiment evolution over time, computes activity and score metrics, analyzes TF-IDF term trajectories and platform entities, and identifies temporal coincidences without causal overreach.

---

## Canonical Model Dependency

A single canonical copy of the trained sentiment pipeline is maintained:
```text
Round-2/models/sentiment_label_pipeline.pkl
```
Round 3 loads this exact model using a repository-relative path (`../Round-2/models/sentiment_label_pipeline.pkl`). To maintain integrity and prevent version drift, no duplicate copy of this model exists in Round 3 or elsewhere in the repository.

---

## Reproduction Instructions

### Prerequisites
- Python 3.10+ (tested on Python 3.14)
- Standard scientific stack (`pandas`, `numpy`, `scikit-learn`, `joblib`, `matplotlib`, `reportlab`, `pillow`)

### Step-by-Step Reproduction

1. **Round 1 Phase 1 (Data Cleaning):**
   ```bash
   cd Round-1/Phase-1
   python src/clean_data.py
   ```

2. **Round 1 Phase 2 (SQLite Setup & SQL Generation):**
   ```bash
   cd ../Phase-2
   python src/load_sqlite.py
   python src/build_phase2_submission.py
   ```

3. **Round 2 (NLP Modeling & Evaluation):**
   ```bash
   cd ../../Round-2
   python -m pip install -r requirements.txt
   python run_round2.py
   ```

4. **Round 3 (Public Discourse Analysis):**
   ```bash
   cd ../Round-3
   python -m pip install -r requirements.txt
   python src/run_round3.py
   ```

---

## Important Assumptions & Limitations

1. **Phase 1 Missing Data:** Missing values in `platform`, `text_content`, and `likes` are preserved as SQL `NULL`s to maintain ground truth without introducing synthetic bias.
2. **Phase 2 Scoring:** Total engagement is defined strictly as `likes + shares + comments`. Posts with missing likes are excluded from engagement calculations in accordance with challenge specifications.
3. **Round 2 Classification:** Models operate on TF-IDF n-gram representations with linear classifiers; results represent held-out test splits with strict group-level isolation.
4. **Round 3 Observations:** Hacker News is a tech-centric public forum and does not constitute a statistically representative sample of general social media users. Detected sentiment and engagement shifts are descriptive temporal coincidences; they do not establish causal relationships.
5. **No Tracked Caches:** All Python compilation caches (`__pycache__`, `*.pyc`), notebook checkpoints (`.ipynb_checkpoints`), IDE configurations, and temporary files are strictly excluded from version control via `.gitignore`.
