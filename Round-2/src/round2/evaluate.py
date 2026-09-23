"""Evaluation helpers, kept separate to make results easy to reproduce."""
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report, confusion_matrix


def metrics_for(y_true, y_pred, labels):
    p, r, f, _ = precision_recall_fscore_support(y_true, y_pred, average="macro", zero_division=0)
    _, _, wf, _ = precision_recall_fscore_support(y_true, y_pred, average="weighted", zero_division=0)
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)), "macro_precision": float(p),
        "macro_recall": float(r), "macro_f1": float(f), "weighted_f1": float(wf),
        "classification_report": classification_report(y_true, y_pred, labels=labels, output_dict=True, zero_division=0),
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=labels).tolist(),
    }
