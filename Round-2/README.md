# Data Vortex A'26 — Round 2

## Objective

Build reproducible NLP classifiers for the supplied labelled social-post dataset. Sentiment classification is the primary task; topic classification is a secondary supervised task.

## Dataset and methodology

`data/Labeled_Social_NLP_Training_Data.csv` contains the supplied labelled input. Duplicate-normalized texts are kept within a single split to prevent leakage. The models use TF-IDF word unigrams/bigrams and compare a majority baseline, Logistic Regression, and Linear SVM using validation macro F1 before one held-out test evaluation.

## Canonical final artifacts

- Executed submission notebook: `notebooks/Round2_NLP_Model.ipynb`
- Final trained pipelines: `models/sentiment_label_pipeline.pkl`, `models/topic_category_pipeline.pkl`
- Evaluation report: `reports/Round2_Evaluation_Metrics.pdf`
- Technical report: `reports/Round2_Technical_Report.pdf`

The two model files are unchanged final artifacts. Round 3 directly uses the canonical sentiment pipeline; it does not keep a duplicate model copy.

## Reproduce

```powershell
python -m pip install -r requirements.txt
python run_round2.py
```

The pipeline writes runtime results and figures when executed. These generated files are intentionally not retained in the final repository because the notebook and PDF reports preserve the submitted evidence.
