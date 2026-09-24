# Model Registry & Calibration Specifications

This directory documents the model loading strategy and calibration protocols for Round 4.

## Canonical Model Pointers

Trained machine learning models from Round 2 are referenced dynamically via `Round-4/repositories/model_repository.py` without duplicating multi-megabyte binary artifacts:

1. **Sentiment Classification Pipeline:**
   - Canonical Path: `Round-2/models/sentiment_label_pipeline.pkl`
   - Architecture: Word Unigram/Bigram TF-IDF + Logistic Regression (`C=1.0`)
   - Held-Out Test Accuracy: `0.5786` | Macro F1: `0.5795` | Weighted F1: `0.5800`
   - Calibration Protocol: Calibrated posterior probabilities via `predict_proba`. Sums strictly to 1.0 across classes `['Negative', 'Neutral', 'Positive']`.

2. **Topic Category Classification Pipeline:**
   - Canonical Path: `Round-2/models/topic_category_pipeline.pkl`
   - Architecture: Word N-gram TF-IDF + Linear Support Vector Machine (`LinearSVC`)
   - Held-Out Test Accuracy: `0.9264` | Macro F1: `0.5805` | Weighted F1: `0.9110`
   - Calibration Protocol: Signed margin hyperplane distances via `decision_function`. Explicitly labeled softmax approximation displayed in the UI for relative comparisons without claiming true calibrated probability.

Models are cached in memory using Streamlit `@st.cache_resource` for low-latency interactive inference.
