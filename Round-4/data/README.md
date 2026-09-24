# Round 4 Data Architecture & Canonical Dependencies

## Zero-Duplication Architecture

To maintain rigorous scientific provenance, prevent file bloat, and comply with DATA VORTEX rules, Round 4 does **not** duplicate previous-round datasets. All analytical modules, the interactive dashboard, and the submission notebook resolve canonical datasets using repository-relative paths.

---

## Canonical Data Sources Referenced

| Source Milestone | Canonical File Path | Records | Description | Access Mode |
| :--- | :--- | :--- | :--- | :--- |
| **Round 1 — Phase 1** | `Round-1/Phase-1/data/cleaned/Social_Engine_Posts_Cleaned.csv` | 12,000 | Cleaned social posts (deduplicated, sign inversions corrected) | Read-only Pandas |
| **Round 1 — Phase 1** | `Round-1/Phase-1/data/cleaned/Social_Engine_Users_Cleaned.csv` | 1,500 | Cleaned user creator records | Read-only Pandas |
| **Round 1 — Phase 2** | `Round-1/Phase-2/data/data_vortex.db` | 13,500 | Relational SQLite production database (users & posts) | SQLite URI (`?mode=ro`) |
| **Round 2** | `Round-2/data/Labeled_Social_NLP_Training_Data.csv` | 9,000 | Ground-truth labeled NLP dataset (3,000 Neg / 3,000 Neu / 3,000 Pos) | Read-only Pandas |
| **Round 3** | `Round-3/data/processed/round3_recommendation_algorithm_reactions.csv` | 204 | Retained public Hacker News reactions dataset | Read-only Pandas |
| **Round 3** | `Round-3/data/raw/collection_metadata.json` | — | Collection parameters and query metadata from Algolia API | JSON loader |

---

## Data Pipeline Guarantee

1. **Immutability:** Source datasets are never modified, overwritten, or mutated.
2. **Read-Only SQLite:** The production database is opened exclusively with `file:{path}?mode=ro` URI semantics.
3. **No Imputation Bias:** Missing likes and comments are excluded rather than zero-imputed to prevent artificial distortion.
