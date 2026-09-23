"""Training helpers for the Round 2 pipeline."""
from time import perf_counter
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC


def make_candidates():
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_df=0.98,
                                 sublinear_tf=True, strip_accents="unicode")
    return {
        "Majority baseline": Pipeline([("tfidf", vectorizer), ("classifier", DummyClassifier(strategy="most_frequent"))]),
        "TF-IDF + Logistic Regression": Pipeline([("tfidf", vectorizer), ("classifier", LogisticRegression(C=2.0, max_iter=2000, class_weight="balanced", random_state=42))]),
        "TF-IDF + Linear SVM": Pipeline([("tfidf", vectorizer), ("classifier", LinearSVC(C=1.0, class_weight="balanced", random_state=42))]),
    }


def fit_timed(pipeline, x_train, y_train):
    start = perf_counter()
    pipeline.fit(x_train, y_train)
    return pipeline, perf_counter() - start
