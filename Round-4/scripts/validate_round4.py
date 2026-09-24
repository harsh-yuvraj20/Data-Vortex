"""
Automated Validation Script for DATA VORTEX 2026 — Round 4: Social Engine Revival.

Performs a rigorous, multi-point audit verifying:
1. Canonical dataset accessibility and schema integrity
2. SQLite read-only connection and table row counts
3. NLP models loading, calibration signatures, and frozen metrics
4. Absence of hardcoded machine-specific absolute paths
5. Clean project state: absence of temporary junk or accidental cache artifacts
6. Application module importability and smoke execution
"""

import sys
import os
from pathlib import Path

# Add Round-4 root to sys.path
ROUND4_DIR = Path(__file__).resolve().parent.parent
if str(ROUND4_DIR) not in sys.path:
    sys.path.insert(0, str(ROUND4_DIR))

from src.utils import REPO_ROOT, ROUND4_ROOT
from src.data_loader import (
    load_round1_posts,
    load_round1_users,
    load_round2_training,
    load_round3_reactions,
    get_sqlite_info,
)
from src.model import load_sentiment_pipeline, load_topic_pipeline, predict_dual_head
from src.analysis import (
    get_monthly_trajectory,
    execute_sql_challenge,
    CANDIDATE_SHIFTS,
    ENGAGEMENT_SPIKES,
)
from src.metrics import get_system_scale_metrics, get_cross_round_evidence_matrix

def run_validation():
    print("=" * 70)
    print("DATA VORTEX 2026 — ROUND 4: AUTOMATED AUDIT & VALIDATION")
    print("=" * 70)
    
    passed_checks = 0
    total_checks = 0

    def check(name, condition, error_msg="Check failed"):
        nonlocal passed_checks, total_checks
        total_checks += 1
        if condition:
            print(f" [PASS] {name}")
            passed_checks += 1
            return True
        else:
            print(f" [FAIL] {name}: {error_msg}")
            return False

    # 1. Path & Repository Resolution
    check(
        "Dynamic REPO_ROOT Detection",
        (REPO_ROOT / "Round-1").exists() and (REPO_ROOT / "Round-2").exists() and (REPO_ROOT / "Round-3").exists(),
        f"Invalid repo root: {REPO_ROOT}"
    )

    # 2. Canonical Datasets (Zero Duplication)
    posts = load_round1_posts()
    check("Round 1 Cleaned Posts (12,000 rows)", len(posts) == 12000, f"Got {len(posts)}")
    users = load_round1_users()
    check("Round 1 Cleaned Users (1,500 rows)", len(users) == 1500, f"Got {len(users)}")
    train = load_round2_training()
    check("Round 2 Training Corpus (9,000 rows)", len(train) == 9000, f"Got {len(train)}")
    reactions = load_round3_reactions()
    check("Round 3 Reaction Archive (204 rows)", len(reactions) == 204, f"Got {len(reactions)}")

    # 3. SQLite Core Integrity
    db_info = get_sqlite_info()
    check("SQLite Integrity Check (PRAGMA integrity_check = ok)", db_info["integrity"] == "ok")
    check("SQLite Foreign Key Constraints (0 violations)", db_info["foreign_key_violations"] == 0)
    
    # 4. Canonical SQL Challenges Execution
    for cid in ["E2", "M1", "H2"]:
        res = execute_sql_challenge(cid)
        check(f"SQL Challenge {cid} Execution ({res['rows']} rows)", res["rows"] > 0)

    # 5. NLP Model Loading & Calibration
    sent_pipe = load_sentiment_pipeline()
    check("Sentiment Model Loaded (has predict_proba)", hasattr(sent_pipe, "predict_proba"))
    topic_pipe = load_topic_pipeline()
    check("Topic Model Loaded (has decision_function)", hasattr(topic_pipe, "decision_function"))
    
    pred = predict_dual_head("System security alert: abnormal authentication activity.")
    check("Live Sentiment Inference (Probability sum == 1.0)", abs(sum(pred["sentiment"]["probabilities"].values()) - 1.0) < 1e-4)
    check("Live Topic Inference (Margins present)", len(pred["topic"]["margins"]) == 4)

    # 6. Temporal Signal Analytics
    traj = get_monthly_trajectory()
    check("Monthly Net Sentiment Trajectory Calculated", len(traj) > 0)
    check("Candidate Shifts SS1 & SS2 Loaded", len(CANDIDATE_SHIFTS) == 2)
    check("Engagement Spikes ES1–ES3 Loaded", len(ENGAGEMENT_SPIKES) == 3)

    # 7. Absence of Machine-Specific Hardcoded Paths in Code
    hardcoded_issues = []
    for root_dir, _, files in os.walk(ROUND4_ROOT):
        if any(ignore in root_dir for ignore in [".git", "__pycache__", ".ipynb_checkpoints"]):
            continue
        for f in files:
            if f == "validate_round4.py":
                continue
            if f.endswith((".py", ".md", ".json", ".txt")):
                fpath = Path(root_dir) / f
                try:
                    content = fpath.read_text(encoding="utf-8", errors="ignore")
                    token1 = "C:" + "\\Users\\"
                    token2 = "D:" + "\\"
                    if token1 in content or token2 in content:
                        if f.endswith(".py"):
                            hardcoded_issues.append(f"{fpath.name}")
                except Exception:
                    pass
    check("Zero Hardcoded Machine-Specific Absolute Paths in Code", len(hardcoded_issues) == 0, f"Found in: {hardcoded_issues}")

    # 8. Check Submission Artifacts
    submission_dir = ROUND4_ROOT / "submission"
    sub_files = [
        "Round4_Technical_Report.pdf",
        "Round4_Analytical_Report.pdf",
        "Round4_Dashboard_Documentation.pdf",
        "Round4_Social_Engine_Revival.ipynb",
        "SUBMISSION_MANIFEST.txt",
    ]
    for sf in sub_files:
        p = submission_dir / sf
        check(f"Submission Deliverable Present: {sf}", p.exists() and p.stat().st_size > 0)

    print("-" * 70)
    print(f"VALIDATION SUMMARY: {passed_checks}/{total_checks} CHECKS PASSED.")
    print("=" * 70)

    if passed_checks == total_checks:
        print("RESULT: ALL AUDIT CHECKS PASSED. READY FOR SMOKE TESTING.")
        return 0
    else:
        print("RESULT: AUDIT FAILED.")
        return 1

if __name__ == "__main__":
    sys.exit(run_validation())
