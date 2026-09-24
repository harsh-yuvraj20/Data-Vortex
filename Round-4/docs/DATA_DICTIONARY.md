# DATA VORTEX 2026 — ROUND 4: DATA DICTIONARY

**Document:** `docs/DATA_DICTIONARY.md`  
**Purpose:** Comprehensive field-level documentation for all canonical datasets integrated in Round 4.  
**Provenance:** Directly traces source milestones, data types, business definitions, transformations, and missing-value treatments.

---

## 1. Round 1 Cleaned Posts Dataset

**Source Milestone:** Round 1 — Phase 1  
**Canonical File Path:** `Round-1/Phase-1/data/cleaned/Social_Engine_Posts_Cleaned.csv`  
**Record Count:** 12,000 rows × 8 columns  
**Relational Role:** Fact table in production SQLite core (`posts`)

| Column Name | Data Type | Meaning / Business Description | Transformation / Provenance | Missing-Value Handling |
| :--- | :--- | :--- | :--- | :--- |
| `post_id` | String (`VARCHAR`) | Unique identifier for each social post item. | Preserved from raw source; exact duplicates removed. | None (0 missing; primary key). |
| `user_id` | String (`VARCHAR`) | Creator identifier linking post to creator profile. | Foreign key referencing `users.user_id`. | None (0 missing; 100% referential integrity). |
| `timestamp` | Datetime (`TIMESTAMP`) | Publication timestamp of the social post. | Normalized to standard ISO-8601 UTC representation. | None (0 missing). |
| `platform` | String (`VARCHAR`) | Hosting social media platform (`Twitter`, `Instagram`, `Facebook`, etc.). | Standardized casing and whitespace stripped. | None (0 missing). |
| `post_type` | String (`VARCHAR`) | Content modality (`text`, `image`, `video`). | Standardized lowercase string categorical. | None (0 missing). |
| `likes` | Float / Int (`INTEGER`) | Total public like count for the post. | Confirmed negative values corrected via sign restoration. | **Preserved genuine missing** (excluded in complete engagement queries). |
| `shares` | Integer (`INTEGER`) | Total share / repost interaction count. | Validated non-negative integer count. | None (0 missing). |
| `comments` | Integer (`INTEGER`) | Total comment interaction count. | Validated non-negative integer count. | None (0 missing). |

---

## 2. Round 1 Cleaned Users Dataset

**Source Milestone:** Round 1 — Phase 1  
**Canonical File Path:** `Round-1/Phase-1/data/cleaned/Social_Engine_Users_Cleaned.csv`  
**Record Count:** 1,500 rows × 5 columns  
**Relational Role:** Dimension table in production SQLite core (`users`)

| Column Name | Data Type | Meaning / Business Description | Transformation / Provenance | Missing-Value Handling |
| :--- | :--- | :--- | :--- | :--- |
| `user_id` | String (`VARCHAR`) | Unique identifier for each creator account. | Primary key; deduplicated creator registry. | None (0 missing; primary key). |
| `username` | String (`VARCHAR`) | Creator display handle. | Standardized clean alphanumeric handle. | None (0 missing). |
| `location` | String (`VARCHAR`) | Geographical home location of creator. | Stripped trailing spaces and normalized city/region tokens. | None (0 missing; used for M1/H2 SQL grouping). |
| `follower_count` | Integer (`INTEGER`) | Number of accounts following this creator. | Non-negative integer count. | None (0 missing). |
| `following_count` | Integer (`INTEGER`) | Number of accounts followed by this creator. | Non-negative integer count. | None (0 missing). |

---

## 3. Round 1 SQLite Relational Schema (`data_vortex.db`)

**Source Milestone:** Round 1 — Phase 2  
**Canonical File Path:** `Round-1/Phase-2/data/data_vortex.db`  
**Integrity Status:** PRAGMA integrity_check = `ok` | PRAGMA foreign_key_check = `0 violations`  
**Access Semantic:** Opened strictly in read-only mode (`?mode=ro`).

- **Table `users`:** 1,500 rows. Primary Key: `user_id`.
- **Table `posts`:** 12,000 rows. Primary Key: `post_id`. Foreign Key: `user_id REFERENCES users(user_id)`.
- **Calculated Metric (Total Engagement):** `likes + shares + comments` (calculated where `likes IS NOT NULL`).

---

## 4. Round 2 Labeled NLP Training Dataset

**Source Milestone:** Round 2  
**Canonical File Path:** `Round-2/data/Labeled_Social_NLP_Training_Data.csv`  
**Record Count:** 9,000 rows × 4 columns  
**Supervised Targets:** `sentiment_label` (primary) and `topic_category` (secondary)

| Column Name | Data Type | Meaning / Business Description | Transformation / Provenance | Missing-Value Handling |
| :--- | :--- | :--- | :--- | :--- |
| `text_id` | String (`str`) | Unique identifier for labeled training text item. | Preserved from official Round 2 supplied CSV. | None (0 missing). |
| `post_text` | String (`str`) | Raw post text with user mentions, URLs, hashtags. | Unicode NFKC normalization used for duplicate grouping. | None (0 missing; empty strings verified absent). |
| `sentiment_label` | Categorical (`str`) | 3-class ground truth sentiment (`Negative`, `Neutral`, `Positive`). | Perfectly balanced: exactly 3,000 records per class. | None (0 missing). |
| `topic_category` | Categorical (`str`) | 4-class thematic category (`Community_Discussion`, `Technical_Issues`, `Feature_Feedback`, `Account_Security`). | Skewed distribution: 7,752 Community, 815 Technical, 297 Feedback, 136 Security. | None (0 missing). |

---

## 5. Round 3 Processed Public Reactions Dataset

**Source Milestone:** Round 3  
**Canonical File Path:** `Round-3/data/processed/round3_recommendation_algorithm_reactions.csv`  
**Record Count:** 204 rows × 24 columns  
**Observation Window:** 2011-02-02 06:34:14 UTC to 2026-09-21 18:49:57 UTC (15-year public archive)

| Column Name | Data Type | Meaning / Business Description | Transformation / Provenance | Missing-Value Handling |
| :--- | :--- | :--- | :--- | :--- |
| `id` | String (`str`) | Unique Hacker News item identifier. | Preserved from Algolia search API item record. | None (0 missing). |
| `source` | String (`str`) | Upstream public data source name. | Constant string (`Hacker News`). | None (0 missing). |
| `source_type` | String (`str`) | Item type (`public_story` or `public_comment`). | Screened from raw archive records. | None (0 missing). |
| `timestamp` | Datetime (`UTC`) | Public record creation timestamp. | Parsed to ISO-8601 UTC datetime. | None (0 missing). |
| `date` | Date (`date`) | Truncated calendar date (`YYYY-MM-DD`). | Extracted from timestamp for date range filtering. | None (0 missing). |
| `text` | String (`str`) | Raw text of comment or story text snippet. | Preserved raw text from API export. | None (0 missing). |
| `title` | String (`str`) | Story title (empty for standalone comments). | Preserved raw title string where applicable. | Retained empty where item is comment. |
| `url` | String (`str`) | Web URL of story link or HN discussion thread. | Validated web URL for provenance reference. | Retained empty where no link present. |
| `engagement_score`| Float / Numeric | Public Hacker News story score (upvotes). | Converted to numeric score where available. | **Missing for comments** (excluded from score sums). |
| `comment_count` | Integer | Total comments posted on the parent story. | Integer count where available. | Missing for individual comments. |
| `query_term` | String (`str`) | Algolia API search term that retrieved record. | Logged collection query parameter. | None (0 missing). |
| `cleaned_text` | String (`str`) | Cleaned text for NLP inference and entity extraction. | Lowercased, stripped HTML entities, normalized whitespace. | None (0 missing). |
| `predicted_sentiment`| Categorical (`str`)| Predicted sentiment (`Negative`, `Neutral`, `Positive`). | Generated by canonical Round 2 TF-IDF + LogReg pipeline. | None (0 missing; 132 Neg, 38 Neu, 34 Pos). |
| `negative_probability`| Float (`float`) | Calibrated model probability for Negative class. | Direct output from `predict_proba`. | None (0 missing; bounded [0, 1]). |
| `neutral_probability` | Float (`float`) | Calibrated model probability for Neutral class. | Direct output from `predict_proba`. | None (0 missing; bounded [0, 1]). |
| `positive_probability`| Float (`float`) | Calibrated model probability for Positive class. | Direct output from `predict_proba`. | None (0 missing; bounded [0, 1]). |
