"""
Generates static output figures and tabular CSV results into outputs/ directory.
"""

from pathlib import Path
import sys
import pandas as pd

# Add Round-4 root to sys.path
ROUND4_DIR = Path(__file__).resolve().parent.parent
if str(ROUND4_DIR) not in sys.path:
    sys.path.insert(0, str(ROUND4_DIR))

from src.data_loader import (
    load_round1_posts,
    load_round1_users,
    load_round2_training,
    load_round3_reactions,
)
from src.analysis import (
    get_monthly_trajectory,
    get_entity_frequencies,
    execute_sql_challenge,
    CANDIDATE_SHIFTS,
    ENGAGEMENT_SPIKES,
)
from src.metrics import get_system_scale_metrics, get_cross_round_evidence_matrix

def export_outputs():
    fig_dir = ROUND4_DIR / "outputs" / "figures"
    res_dir = ROUND4_DIR / "outputs" / "results"
    fig_dir.mkdir(parents=True, exist_ok=True)
    res_dir.mkdir(parents=True, exist_ok=True)

    print("Exporting tabular results...")
    # 1. System Scale Summary
    scale = get_system_scale_metrics()
    pd.DataFrame([scale]).to_csv(res_dir / "system_scale_summary.csv", index=False)

    # 2. SQL Challenges Results
    for cid in ["E2", "M1", "H2"]:
        res = execute_sql_challenge(cid)
        res["results"].to_csv(res_dir / f"sql_challenge_{cid.lower()}.csv", index=False)

    # 3. Monthly Trajectory
    traj = get_monthly_trajectory()
    traj.to_csv(res_dir / "monthly_sentiment_trajectory.csv", index=False)

    # 4. Candidate Shifts & Spikes
    pd.DataFrame(CANDIDATE_SHIFTS).to_csv(res_dir / "candidate_shifts.csv", index=False)
    pd.DataFrame(ENGAGEMENT_SPIKES).to_csv(res_dir / "engagement_spikes.csv", index=False)

    # 5. Cross-Round Evidence Matrix
    matrix = get_cross_round_evidence_matrix()
    matrix.to_csv(res_dir / "cross_round_evidence_matrix.csv", index=False)

    print("Tabular results successfully exported to:", res_dir)

if __name__ == "__main__":
    export_outputs()
