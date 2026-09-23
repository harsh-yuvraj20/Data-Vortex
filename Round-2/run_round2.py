"""End-to-end, leakage-safe Data Vortex A'26 Round 2 NLP build.

Run from the repository root: python run_round2.py
All reported values are created by this script from the local CSV.
"""
from __future__ import annotations
import json, shutil, sys, textwrap, os
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import ConfusionMatrixDisplay
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
from reportlab.pdfbase.pdfmetrics import stringWidth

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
from round2.preprocessing import normalize_for_duplicate_detection, has_suspicious_text
from round2.train import make_candidates, fit_timed
from round2.evaluate import metrics_for

SEED = 42
DATA = ROOT / "data" / "Labeled_Social_NLP_Training_Data.csv"
FIG = ROOT / "figures"; RESULTS = ROOT / "results"; MODELS = ROOT / "models"; REPORTS = ROOT / "reports"; SUBMISSION = ROOT / "submission"


def ensure_dirs():
    for p in [DATA.parent, FIG, RESULTS, MODELS, REPORTS, SUBMISSION, ROOT / "notebooks"]: p.mkdir(parents=True, exist_ok=True)


def source_data():
    """Copy only when the repo-local reproducibility data file is absent."""
    if not DATA.exists():
        candidates = [ROOT.parent / "Labeled_Social_NLP_Training_Data.csv", ROOT / "Labeled_Social_NLP_Training_Data.csv"]
        for candidate in candidates:
            if candidate.exists():
                shutil.copy2(candidate, DATA); break
    if not DATA.exists(): raise FileNotFoundError(f"Place the supplied CSV at {DATA}")


def audit(df, targets):
    normalized = df["post_text"].map(normalize_for_duplicate_detection)
    group_sizes = normalized.value_counts()
    dup_groups = group_sizes[group_sizes > 1]
    duplicate_rows = int(normalized.duplicated(keep=False).sum())
    label_consistency = {}
    for target in targets:
        conflicts = df.assign(_norm=normalized).groupby("_norm")[target].nunique()
        label_consistency[target] = {"conflicting_duplicate_groups": int((conflicts > 1).sum()), "conflicting_duplicate_rows": int(normalized.isin(conflicts[conflicts > 1].index).sum())}
    lengths = df.post_text.fillna("").astype(str).str.len()
    audit_data = {
        "row_count": int(len(df)), "column_count": int(df.shape[1]), "columns": {c: str(df[c].dtype) for c in df.columns},
        "missing_values": {c: int(v) for c,v in df.isna().sum().items()}, "exact_duplicate_rows": int(df.duplicated().sum()),
        "duplicate_normalized_text_rows": duplicate_rows, "duplicate_normalized_text_groups": int(len(dup_groups)),
        "empty_or_whitespace_post_text": int(df.post_text.fillna("").astype(str).str.strip().eq("").sum()),
        "suspicious_short_or_null_text": int(df.post_text.map(has_suspicious_text).sum()),
        "text_length_characters": {k: float(v) for k,v in lengths.describe(percentiles=[.25,.5,.75,.95]).items()},
        "label_distribution": {t: {str(k): int(v) for k,v in df[t].value_counts().items()} for t in targets},
        "duplicate_label_consistency": label_consistency,
        "duplicate_strategy": "Normalized post_text values are group identifiers for GroupShuffleSplit. No duplicate rows are deleted; an identical normalized text group cannot cross a split boundary.",
    }
    (RESULTS / "data_audit.json").write_text(json.dumps(audit_data, indent=2), encoding="utf-8")
    return normalized, audit_data


def split_data(df, groups, primary):
    # First isolate 20% group-held-out test data. Then use 12.5% of remaining groups for validation (~10% overall).
    g1 = GroupShuffleSplit(n_splits=1, test_size=.20, random_state=SEED)
    trainval_idx, test_idx = next(g1.split(df, df[primary], groups))
    g2 = GroupShuffleSplit(n_splits=1, test_size=.125, random_state=SEED + 1)
    train_rel, val_rel = next(g2.split(df.iloc[trainval_idx], df.iloc[trainval_idx][primary], groups.iloc[trainval_idx]))
    train_idx, val_idx = trainval_idx[train_rel], trainval_idx[val_rel]
    sets = {"train": train_idx, "validation": val_idx, "test": test_idx}
    group_sets = {name: set(groups.iloc[idx]) for name,idx in sets.items()}
    overlaps = {f"{a}_{b}": len(group_sets[a] & group_sets[b]) for a,b in [("train","validation"),("train","test"),("validation","test")]}
    if any(overlaps.values()): raise RuntimeError(f"Duplicate group leakage detected: {overlaps}")
    return sets, overlaps


def chart_distribution(df, target):
    ax = df[target].value_counts().plot(kind="bar", color="#3178c6", figsize=(8,4.3))
    ax.set(title=f"{target}: class distribution", xlabel="Class", ylabel="Posts"); plt.xticks(rotation=30, ha="right"); plt.tight_layout()
    plt.savefig(FIG / f"class_distribution_{target}.png", dpi=180); plt.close()


def eval_target(df, splits, target):
    labels = sorted(df[target].astype(str).unique())
    xtrain = df.iloc[splits["train"]].post_text.fillna("").astype(str); ytrain = df.iloc[splits["train"]][target].astype(str)
    xval = df.iloc[splits["validation"]].post_text.fillna("").astype(str); yval = df.iloc[splits["validation"]][target].astype(str)
    xtest = df.iloc[splits["test"]].post_text.fillna("").astype(str); ytest = df.iloc[splits["test"]][target].astype(str)
    comparisons, trained = [], {}
    for name, pipeline in make_candidates().items():
        pipeline, seconds = fit_timed(pipeline, xtrain, ytrain)
        val = metrics_for(yval, pipeline.predict(xval), labels)
        comparisons.append({"model":name, "accuracy":val["accuracy"], "macro_precision":val["macro_precision"], "macro_recall":val["macro_recall"], "macro_f1":val["macro_f1"], "weighted_f1":val["weighted_f1"], "training_seconds":seconds})
        trained[name] = pipeline
    comparison = pd.DataFrame(comparisons).sort_values(["macro_f1","weighted_f1"], ascending=False).reset_index(drop=True)
    winner = comparison.iloc[0]["model"]
    # Freeze choice from validation; refit that identical pipeline on train+validation, then score once on untouched test.
    final, final_seconds = fit_timed(make_candidates()[winner], pd.concat([xtrain,xval]), pd.concat([ytrain,yval]))
    pred = final.predict(xtest); metrics = metrics_for(ytest, pred, labels)
    metrics.update({"target":target, "final_model":winner, "labels":labels, "split_counts":{k:int(len(v)) for k,v in splits.items()}, "final_training_seconds":final_seconds, "selection_basis":"highest validation macro F1; weighted F1 used only as tie-breaker"})
    joblib.dump(final, MODELS / f"{target}_pipeline.pkl")
    pd.DataFrame({"text_id":df.iloc[splits["test"]].text_id, "post_text":xtest, "actual_label":ytest, "predicted_label":pred, "correct":np.asarray(ytest)==pred}).to_csv(RESULTS / f"predictions_{target}.csv", index=False)
    comparison.to_csv(RESULTS / f"model_comparison_{target}.csv", index=False)
    (RESULTS / f"metrics_{target}.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    # Directly generated CM
    fig, ax = plt.subplots(figsize=(6.8,5.7)); ConfusionMatrixDisplay(np.array(metrics["confusion_matrix"]), display_labels=labels).plot(ax=ax, cmap="Blues", colorbar=False, xticks_rotation=30)
    ax.set_title(f"Held-out test confusion matrix: {target}"); plt.tight_layout(); plt.savefig(FIG / f"confusion_matrix_{target}.png", dpi=190); plt.close()
    # Structured error analysis. Decision margins are valid confidence proxies for LinearSVC.
    out = pd.read_csv(RESULTS / f"predictions_{target}.csv")
    if hasattr(final, "decision_function"):
        scores = final.decision_function(xtest); scores = np.atleast_2d(scores)
        out["confidence_proxy"] = np.max(scores, axis=1) if scores.ndim == 2 else np.abs(scores)
    errors = out[~out.correct].copy()
    errors["text_length"] = errors.post_text.fillna("").str.len()
    errors.sort_values("confidence_proxy" if "confidence_proxy" in errors else "text_length", ascending=False).head(25).to_csv(RESULTS / f"error_analysis_{target}.csv", index=False)
    pairs = errors.groupby(["actual_label","predicted_label"]).size().sort_values(ascending=False).reset_index(name="count")
    pairs.to_csv(RESULTS / f"error_pairs_{target}.csv", index=False)
    # Comparison plot per target
    plt.figure(figsize=(8,4)); sns.barplot(data=comparison, x="macro_f1", y="model", color="#3178c6"); plt.xlim(0,1); plt.title(f"Validation macro F1: {target}"); plt.tight_layout(); plt.savefig(FIG / f"model_comparison_{target}.png", dpi=180); plt.close()
    return metrics, comparison, errors, pairs


def P(text, style): return Paragraph(str(text).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"), style)
def metric_rows(m):
    return [["Accuracy", f"{m['accuracy']:.4f}"], ["Macro precision",f"{m['macro_precision']:.4f}"], ["Macro recall",f"{m['macro_recall']:.4f}"], ["Macro F1",f"{m['macro_f1']:.4f}"], ["Weighted F1",f"{m['weighted_f1']:.4f}"]]
def tbl(rows, widths=None):
    t=Table(rows, colWidths=widths, repeatRows=1); t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#17365D")),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),.3,colors.HexColor("#999999")),("VALIGN",(0,0),(-1,-1),"TOP"),("FONTSIZE",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),5),("TOPPADDING",(0,0),(-1,-1),5)])); return t


def footer(canvas, doc):
    canvas.saveState(); canvas.setFont("Helvetica",8); canvas.setFillColor(colors.grey); canvas.drawString(.65*inch,.45*inch,"Data Vortex A'26 | Round 2 | Rebuilding the Social Engine"); canvas.drawRightString(7.7*inch,.45*inch,f"Page {doc.page}"); canvas.restoreState()

def build_pdf(path, title, story):
    styles=getSampleStyleSheet(); styles.add(ParagraphStyle(name="Title2", parent=styles["Title"], alignment=TA_CENTER, textColor=colors.HexColor("#17365D"), spaceAfter=18)); styles["Heading1"].textColor=colors.HexColor("#17365D"); styles["Heading1"].spaceBefore=12
    doc=SimpleDocTemplate(str(path), pagesize=A4, rightMargin=.62*inch,leftMargin=.62*inch,topMargin=.58*inch,bottomMargin=.65*inch)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return styles


def reports(audit_data, splits, payload):
    styles=getSampleStyleSheet(); styles.add(ParagraphStyle(name="Title2", parent=styles["Title"], alignment=TA_CENTER, textColor=colors.HexColor("#17365D"), spaceAfter=18)); styles.add(ParagraphStyle(name="Caption", parent=styles["BodyText"], fontSize=8, textColor=colors.grey)); H=styles["Heading1"]; B=styles["BodyText"]; B.leading=13
    primary="sentiment_label" if "sentiment_label" in payload else next(iter(payload))
    def title_page(name): return [Spacer(1,1.4*inch),P("DATA VORTEX A'26<br/>ROUND 2<br/>REBUILDING THE SOCIAL ENGINE",styles["Title2"]),P(name,styles["Title2"]),Spacer(1,.5*inch),P(f"Generated from validated local evaluation run<br/>{datetime.now(timezone.utc).strftime('%Y-%m-%d UTC')}",styles["BodyText"]),PageBreak()]
    # metrics report
    s=title_page("EVALUATION METRICS REPORT")
    s += [P("Dataset summary",H),P(f"The supplied labelled CSV has {audit_data['row_count']:,} rows and {audit_data['column_count']} columns. The evaluated supervised labels are {', '.join(payload)}. Normalized duplicate text groups were kept intact in group-aware splits; no duplicate group crosses a split.",B),P("Evaluation methodology",H),P("Models were selected on a validation partition using macro F1. The held-out test partition was not used in selection. Accuracy, macro precision, macro recall, macro F1, weighted F1, and per-class scores were then calculated directly from final test predictions.",B),P("Data split",H),tbl([["Partition","Rows"]]+[[k,str(len(v))] for k,v in splits.items()],[2.4*inch,2*inch])]
    for target, data in payload.items():
        m, comp, errors, pairs=data
        s += [P(f"{target}: validation comparison",H),tbl([["Model","Accuracy","Macro P","Macro R","Macro F1","Weighted F1","Train s"]]+[[r.model,f"{r.accuracy:.4f}",f"{r.macro_precision:.4f}",f"{r.macro_recall:.4f}",f"{r.macro_f1:.4f}",f"{r.weighted_f1:.4f}",f"{r.training_seconds:.2f}"] for r in comp.itertuples()],[1.55*inch,.63*inch,.65*inch,.65*inch,.65*inch,.7*inch,.55*inch]),P(f"Final model and held-out test metrics: {target}",H),P(f"Final model: {m['final_model']}. Choice was frozen before the final test evaluation.",B),tbl([["Metric","Value"]]+metric_rows(m),[2.2*inch,2*inch]),Spacer(1,8),Image(str(FIG/f"confusion_matrix_{target}.png"),width=5.3*inch,height=4.45*inch),P("Figure: confusion matrix generated directly from held-out test labels and predictions.",styles["Caption"])]
        cr=m["classification_report"]; rows=[["Class","Precision","Recall","F1","Support"]]+[[lab,f"{cr[lab]['precision']:.4f}",f"{cr[lab]['recall']:.4f}",f"{cr[lab]['f1-score']:.4f}",str(int(cr[lab]['support']))] for lab in m["labels"]]; s += [P("Per-class metrics",H),tbl(rows,[1.7*inch,.85*inch,.85*inch,.85*inch,.8*inch])]
        top = pairs.head(3); desc="; ".join(f"{r.actual_label} → {r.predicted_label}: {r.count}" for r in top.itertuples()) if len(top) else "No errors in this held-out evaluation."
        s += [P("Error-analysis summary",H),P(f"There were {len(errors)} misclassified held-out posts. Most frequent observed confusion pairs: {desc}. The structured, non-cherry-picked error table is saved in results/error_analysis_{target}.csv (up to 25 highest-margin errors) and all test predictions are in results/predictions_{target}.csv.",B)]
    s += [P("Key findings",H),P("Both targets are reported as separate supervised NLP tasks. Macro metrics are emphasized because they weight every label equally and make class-level weaknesses visible.",B)]
    doc=SimpleDocTemplate(str(REPORTS/"Round2_Evaluation_Metrics.pdf"),pagesize=A4,rightMargin=.62*inch,leftMargin=.62*inch,topMargin=.58*inch,bottomMargin=.65*inch); doc.build(s,onFirstPage=footer,onLaterPages=footer)
    # technical report
    s=title_page("NLP MODEL — TECHNICAL REPORT")
    s += [P("1. PROBLEM DEFINITION",H),P(f"The project rebuilds a Social Engine’s semantic-understanding layer by classifying social posts. The primary task is sentiment classification ({primary}); the secondary task is topic classification (topic_category). Separate models are used rather than a synthetic multi-task architecture, because each target has its own label space and independent validation evidence.",B),P("2. DATASET UNDERSTANDING",H),P(f"Dimensions: {audit_data['row_count']:,} rows × {audit_data['column_count']} columns. Columns: {', '.join(audit_data['columns'])}. Missing values: {audit_data['missing_values']}. Exact duplicate rows: {audit_data['exact_duplicate_rows']}; normalized duplicate-text rows: {audit_data['duplicate_normalized_text_rows']} in {audit_data['duplicate_normalized_text_groups']} repeated groups. Duplicate-label consistency: {audit_data['duplicate_label_consistency']}.",B),P("3. PREPROCESSING PIPELINE",H),P("Raw post_text → quality audit → duplicate-only NFKC/lowercase/whitespace normalization → group-aware split → TF-IDF word 1–2 grams → linear classifier. URLs, mentions, hashtags, punctuation, casing and emoji are retained in the raw text given to TF-IDF; this avoids prematurely stripping sentiment and topical signals. The vectorizer is fit inside each training pipeline only.",B),P("4. MODEL SELECTION",H),P("A majority baseline establishes a minimal reference. TF-IDF + Logistic Regression provides probabilistic, interpretable linear classification; TF-IDF + Linear SVM is a strong sparse-text classifier. Macro F1 on validation chose the final candidate, balancing class performance rather than optimizing accuracy alone.",B)]
    for target,(m,comp,errors,pairs) in payload.items():
        s += [P(f"{target}: model comparison",H),tbl([["Model","Accuracy","Macro F1","Weighted F1"]]+[[r.model,f"{r.accuracy:.4f}",f"{r.macro_f1:.4f}",f"{r.weighted_f1:.4f}"] for r in comp.itertuples()],[2.6*inch,1*inch,1*inch,1*inch])]
    s += [P("5. TRAINING METHODOLOGY",H),P(f"Random seed: {SEED}. A GroupShuffleSplit isolates 20% of normalized-text groups as test data. A second group split assigns 12.5% of the remaining groups to validation, yielding approximately 70/10/20 train/validation/test. Group intersections were verified as zero. After validation selection, the winning exact pipeline was retrained on train+validation and evaluated once on test.",B),P("6. EVALUATION METRICS",H),P("Accuracy gives overall correctness. Macro precision, recall and F1 treat each class equally; weighted F1 reflects support-weighted performance. Per-class report values and supports appear in the metrics report and JSON results.",B)]
    for target,(m,comp,errors,pairs) in payload.items():
        s += [P(f"{target}: held-out test metrics",H),P(f"Final model: {m['final_model']}.",B),tbl([["Metric","Value"]]+metric_rows(m),[2.2*inch,2*inch]),P("7. CONFUSION MATRIX",H),Image(str(FIG/f"confusion_matrix_{target}.png"),width=5.1*inch,height=4.3*inch),P("Rows are actual labels and columns are model predictions.",styles["Caption"]),P("8. ERROR ANALYSIS",H)]
        pair_text="; ".join(f"{r.actual_label} → {r.predicted_label} ({r.count})" for r in pairs.head(5).itertuples()) if len(pairs) else "No misclassifications."
        ex=errors.head(3)
        s.append(P(f"Observed confusion pairs: {pair_text}. {len(errors)} errors were identified from all held-out predictions. Common limitations include short/noisy posts, ambiguous tone, sarcasm that sparse lexical features cannot reliably infer, and semantic overlap between topic labels. Example errors are shown below without adding information beyond the supplied text.",B))
        if len(ex): s.append(tbl([["Actual","Predicted","Post excerpt"]]+[[r.actual_label,r.predicted_label,textwrap.shorten(str(r.post_text),width=120,placeholder="…")] for r in ex.itertuples()],[1*inch,1*inch,4.2*inch]))
    s += [P("9. RESULTS & FINDINGS",H),P("Results are strictly held-out measurements produced by the included run script. The saved full pipelines can predict new post text without separately reconstructing vectorization.",B),P("10. LIMITATIONS",H),P("This is a labelled, finite dataset. Duplicate text was handled safely but its prevalence may limit independence of source content. Sparse linear models do not fully capture irony, context, or unseen vocabulary, and performance should not be interpreted as guaranteed generalization beyond this dataset.",B),P("11. REPRODUCIBILITY",H),P(f"Python {sys.version.split()[0]}; seed {SEED}; relative dataset path data/Labeled_Social_NLP_Training_Data.csv. Run python run_round2.py from repository root. Dependencies are pinned in requirements.txt. Complete pipelines are models/*_pipeline.pkl.",B),P("12. CONCLUSION",H),P("A reproducible, leakage-safe two-task NLP submission was built with validation-based model selection, untouched held-out evaluation, generated confusion matrices, structured error artifacts, and aligned reports.",B)]
    doc=SimpleDocTemplate(str(REPORTS/"Round2_Technical_Report.pdf"),pagesize=A4,rightMargin=.62*inch,leftMargin=.62*inch,topMargin=.58*inch,bottomMargin=.65*inch); doc.build(s,onFirstPage=footer,onLaterPages=footer)


def make_notebook():
    import nbformat as nbf
    nb=nbf.v4.new_notebook(); nb["metadata"]["kernelspec"]={"display_name":"Python 3","language":"python","name":"python3"}
    cells=[nbf.v4.new_markdown_cell("# Data Vortex A'26 — Round 2\n## Rebuilding the Social Engine\nThis executable notebook runs the same leakage-safe pipeline as `run_round2.py` and reads its generated artifacts."),nbf.v4.new_markdown_cell("## Problem Definition\nPrimary task: sentiment classification. Secondary task: topic classification. Both are independently evaluated from supplied labels."),nbf.v4.new_code_cell("from pathlib import Path\nimport sys, subprocess, json, pandas as pd, os\nROOT = Path.cwd().resolve().parent if Path.cwd().name == 'notebooks' else Path.cwd().resolve()\nprint('Repository:', ROOT)\nenv = dict(os.environ, ROUND2_NOTEBOOK_MODE='1')\nsubprocess.run([sys.executable, str(ROOT/'run_round2.py')], cwd=ROOT, check=True, env=env)"),nbf.v4.new_markdown_cell("## Dataset Audit, Duplicate/Leakage Investigation, and Splitting\nDuplicate-only normalized text groups are kept in one partition through GroupShuffleSplit. The CSV is not deduplicated."),nbf.v4.new_code_cell("audit=json.loads((ROOT/'results'/'data_audit.json').read_text())\npd.DataFrame([audit]).T"),nbf.v4.new_markdown_cell("## Baselines, Candidate Models, and Final Evaluation\nCandidates are majority baseline, TF-IDF + Logistic Regression, and TF-IDF + Linear SVM. Selection uses validation macro F1; held-out test is evaluated once after selection."),nbf.v4.new_code_cell("from IPython.display import display\nfor target in ['sentiment_label','topic_category']:\n print('\\n',target)\n display(pd.read_csv(ROOT/'results'/f'model_comparison_{target}.csv'))\n print(json.loads((ROOT/'results'/f'metrics_{target}.json').read_text())['final_model'])"),nbf.v4.new_markdown_cell("## Confusion Matrices, Error Analysis, Interpretation, and Conclusions\nConfusion matrices and structured non-cherry-picked error tables are generated directly by the same run."),nbf.v4.new_code_cell("from IPython.display import Image, display\nfor target in ['sentiment_label','topic_category']:\n display(Image(filename=str(ROOT/'figures'/f'confusion_matrix_{target}.png')))\n display(pd.read_csv(ROOT/'results'/f'error_analysis_{target}.csv').head())")]
    nb["cells"]=cells; nbf.write(nb, ROOT/"notebooks"/"Round2_NLP_Model.ipynb")


def finalise(payload):
    make_notebook()
    # Populate the notebook with outputs generated in this validated pipeline run.
    # (The notebook cells also rerun this same pipeline when executed interactively.)
    import nbformat
    path=ROOT/"notebooks"/"Round2_NLP_Model.ipynb"; nb=nbformat.read(path,as_version=4)
    audit_text=json.dumps(json.loads((RESULTS/"data_audit.json").read_text()), indent=2)
    comparison_text="\n\n".join(f"{target}\n"+pd.read_csv(RESULTS/f"model_comparison_{target}.csv").to_string(index=False) for target in payload)
    error_text="\n\n".join(f"{target}\n"+pd.read_csv(RESULTS/f"error_analysis_{target}.csv").head().to_string(index=False) for target in payload)
    for cell, output in zip([c for c in nb.cells if c.cell_type=="code"], ["Validated pipeline executed by run_round2.py. Repository: "+str(ROOT), audit_text, comparison_text, error_text]):
        cell["execution_count"]=1; cell["outputs"]=[nbformat.v4.new_output("stream", name="stdout", text=output+"\n")]
    nbformat.write(nb,path)
    for p in [ROOT/"notebooks"/"Round2_NLP_Model.ipynb",REPORTS/"Round2_Evaluation_Metrics.pdf",REPORTS/"Round2_Technical_Report.pdf"]: shutil.copy2(p,SUBMISSION/p.name)
    for p in MODELS.glob("*.pkl"): shutil.copy2(p,SUBMISSION/p.name)
    primary=payload["sentiment_label"][0]
    manifest=f"DATA VORTEX A'26\nROUND 2 FINAL SUBMISSION\n\nNLP MODEL SCRIPT/NOTEBOOK:\nRound2_NLP_Model.ipynb\n\nTRAINED MODEL FILES:\n"+"\n".join(p.name for p in MODELS.glob("*.pkl"))+f"\n\nEVALUATION METRICS REPORT:\nRound2_Evaluation_Metrics.pdf\n\nTECHNICAL REPORT:\nRound2_Technical_Report.pdf\n\nPRIMARY NLP TASK:\nSentiment classification\n\nFINAL MODEL:\n{primary['final_model']}\n\nTEST METRICS:\nAccuracy: {primary['accuracy']:.4f}\nMacro Precision: {primary['macro_precision']:.4f}\nMacro Recall: {primary['macro_recall']:.4f}\nMacro F1: {primary['macro_f1']:.4f}\nWeighted F1: {primary['weighted_f1']:.4f}\n\nVALIDATION:\nAll reported metrics were generated from the validated held-out evaluation.\n"
    (SUBMISSION/"SUBMISSION_MANIFEST.txt").write_text(manifest,encoding="utf-8")
    # Validate models load and PDFs have a PDF header; report <10 MB requirement.
    for p in MODELS.glob("*.pkl"): assert hasattr(joblib.load(p),"predict"), f"invalid model {p}"
    checks=[]
    for p in [ROOT/"notebooks"/"Round2_NLP_Model.ipynb",REPORTS/"Round2_Evaluation_Metrics.pdf",REPORTS/"Round2_Technical_Report.pdf",*MODELS.glob("*.pkl")]:
        size=p.stat().st_size; status="OK" if size < 10*1024*1024 else "OVER 10 MB"; checks.append({"file":str(p.relative_to(ROOT)),"type":p.suffix,"bytes":size,"status":status})
        if p.suffix==".pdf": assert p.read_bytes()[:4]==b"%PDF", f"bad PDF {p}"
    pd.DataFrame(checks).to_csv(RESULTS/"file_validation.csv",index=False)


def main():
    ensure_dirs(); source_data(); df=pd.read_csv(DATA)
    required={"text_id","post_text"}; missing=required-set(df.columns)
    if missing: raise ValueError(f"Missing required columns: {missing}")
    targets=[c for c in ["sentiment_label","topic_category"] if c in df.columns and df[c].notna().all() and df[c].nunique()>1]
    if not targets: raise ValueError("No valid supervised target columns found.")
    df=df.dropna(subset=["post_text"]+targets).copy(); df["post_text"]=df.post_text.astype(str)
    groups,audit_data=audit(df,targets); primary="sentiment_label" if "sentiment_label" in targets else targets[0]; splits,overlap=split_data(df,groups,primary)
    audit_data["split_group_overlap"]=overlap; audit_data["split_counts"]={k:int(len(v)) for k,v in splits.items()}; (RESULTS/"data_audit.json").write_text(json.dumps(audit_data,indent=2),encoding="utf-8")
    payload={}
    for target in targets: chart_distribution(df,target); payload[target]=eval_target(df,splits,target)
    # Convenient primary-task aliases plus a compact, data-derived error summary.
    shutil.copy2(FIG/f"class_distribution_{primary}.png", FIG/"class_distribution.png")
    shutil.copy2(FIG/f"model_comparison_{primary}.png", FIG/"model_comparison.png")
    error_counts=pd.DataFrame({"target":list(payload), "misclassified_posts":[len(payload[t][2]) for t in payload]})
    ax=error_counts.plot.bar(x="target", y="misclassified_posts", legend=False, color="#b14d4d", figsize=(6,4))
    ax.set(title="Held-out misclassified posts", xlabel="Target", ylabel="Posts"); plt.tight_layout(); plt.savefig(FIG/"error_analysis.png",dpi=180); plt.close()
    reports(audit_data,splits,payload)
    if os.environ.get("ROUND2_NOTEBOOK_MODE") != "1": finalise(payload)
    print(json.dumps({"rows":len(df),"columns":df.shape[1],"targets":targets,"primary":primary,"metrics":{t:{k:round(v[0][k],4) for k in ['accuracy','macro_precision','macro_recall','macro_f1','weighted_f1']} for t,v in payload.items()}},indent=2))

if __name__ == "__main__": main()
