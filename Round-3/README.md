# Data Vortex A'26 — Round 3

## Objective

Analyze public reaction to changes in recommendation algorithms using genuine public Hacker News archive records. The assigned topic is **Public Reaction to Changes in the Recommendation Algorithm**.

## Data and methodology

`data/raw/` preserves the collection export and its metadata. `data/processed/round3_recommendation_algorithm_reactions.csv` is the final 204-record structured dataset used for the corrected analysis. The source modules document collection, preprocessing, sentiment analysis, activity analysis, topic/entity analysis, and descriptive shift detection.

## Round 2 model dependency

Round 3 loads the canonical, unchanged sentiment pipeline at `../Round-2/models/sentiment_label_pipeline.pkl`. This is the same TF-IDF plus Logistic Regression model submitted for Round 2; Round 3 does not contain a duplicate model copy.

## Final deliverables

- Final dataset: `data/processed/round3_recommendation_algorithm_reactions.csv`
- Provenance archive: `data/raw/`
- Collection and analysis source: `src/`
- Executed analysis notebook: `notebooks/Round3_Real_Time_Analysis.ipynb`
- Required notebook PDF: `reports/Round3_Real_Time_Analysis_Notebook.pdf`
- Analytical report: `reports/Round3_Analytical_Report.pdf`

## Reproduce

```powershell
python -m pip install -r requirements.txt
python src/run_round3.py
```

The stored archive is reused; this repository does not recollect data during reproduction.

## Limitations

Hacker News is a technical-community source and is not population-representative. The archive sample is historical rather than a continuous live stream. Missing comment scores remain missing, and detected shifts or triggers are descriptive temporal coincidences rather than causal claims.
