# Data References & Zero-Duplication Architecture

This directory is reserved for lightweight reference schemas and configuration pointers.

## Canonical Data Source Mapping

In strict compliance with competition constraints against unnecessary large file duplication, all tabular datasets are consumed directly from their canonical previous-round locations via deterministic, repository-relative paths:

1. **Round 1 Phase 1 Cleaned Posts (12,000 rows):**
   `Round-1/Phase-1/data/cleaned/Social_Engine_Posts_Cleaned.csv`
2. **Round 1 Phase 1 Cleaned Users (1,500 rows):**
   `Round-1/Phase-1/data/cleaned/Social_Engine_Users_Cleaned.csv`
3. **Round 1 Phase 1 Raw Corrupted Posts (12,000 rows):**
   `Round-1/Phase-1/data/raw/Social_Engine_Posts_Corrupted.csv`
4. **Round 1 Phase 2 SQLite Database (13,500 records):**
   `Round-1/Phase-2/data/data_vortex.db` (accessed strictly via `?mode=ro`)
5. **Round 2 Labeled NLP Training Data (9,000 rows):**
   `Round-2/data/Labeled_Social_NLP_Training_Data.csv`
6. **Round 3 Algorithm Reaction Archive (204 rows):**
   `Round-3/data/processed/round3_recommendation_algorithm_reactions.csv`

All data loaders implement Streamlit `@st.cache_data` and strict schema validation through `Round-4/repositories/dataset_repository.py`.
