"""
Unit tests for analytical computations and SQL challenges.
"""

import unittest
from pathlib import Path
import sys

# Ensure Round-4 root is in sys.path
ROUND4_DIR = Path(__file__).resolve().parent.parent
if str(ROUND4_DIR) not in sys.path:
    sys.path.insert(0, str(ROUND4_DIR))

from src.analysis import (
    get_monthly_trajectory,
    get_entity_frequencies,
    execute_sql_challenge,
    filter_posts,
    CANDIDATE_SHIFTS,
    ENGAGEMENT_SPIKES,
)

class TestAnalysis(unittest.TestCase):
    """Test suite verifying analytical algorithms, shifts, and SQL challenges."""

    def test_monthly_trajectory_and_index_bounds(self):
        """Verifies that Net Sentiment Index is bounded strictly within [-1.0, 1.0]."""
        df = get_monthly_trajectory()
        self.assertGreater(len(df), 0)
        self.assertIn("year_month", df.columns)
        self.assertIn("net_sentiment_index", df.columns)
        self.assertTrue((df["net_sentiment_index"] >= -1.0).all())
        self.assertTrue((df["net_sentiment_index"] <= 1.0).all())

    def test_candidate_shifts_integrity(self):
        """Verifies candidate shifts SS1 and SS2."""
        self.assertEqual(len(CANDIDATE_SHIFTS), 2)
        ss1 = CANDIDATE_SHIFTS[0]
        self.assertEqual(ss1["id"], "SS1")
        self.assertEqual(ss1["delta"], -0.8000)
        ss2 = CANDIDATE_SHIFTS[1]
        self.assertEqual(ss2["id"], "SS2")
        self.assertEqual(ss2["delta"], 0.8000)

    def test_engagement_spikes_integrity(self):
        """Verifies engagement spikes ES1, ES2, and ES3."""
        self.assertEqual(len(ENGAGEMENT_SPIKES), 3)
        es1 = ENGAGEMENT_SPIKES[0]
        self.assertEqual(es1["id"], "ES1")
        self.assertEqual(es1["observed_score"], 1704.0)
        self.assertEqual(es1["ratio"], 284.0)

    def test_canonical_sql_challenges(self):
        """Verifies execution of canonical SQL challenges E2, M1, and H2."""
        # E2
        res_e2 = execute_sql_challenge("E2")
        self.assertEqual(res_e2["id"], "E2")
        self.assertEqual(len(res_e2["results"]), 10)
        self.assertIn("total_engagement", res_e2["results"].columns)

        # M1
        res_m1 = execute_sql_challenge("M1")
        self.assertEqual(res_m1["id"], "M1")
        self.assertGreater(len(res_m1["results"]), 0)
        self.assertIn("location", res_m1["results"].columns)

        # H2
        res_h2 = execute_sql_challenge("H2")
        self.assertEqual(res_h2["id"], "H2")
        self.assertGreater(len(res_h2["results"]), 0)
        self.assertIn("engagement_rank", res_h2["results"].columns)
        # Ranks must be between 1 and 3
        self.assertTrue((res_h2["results"]["engagement_rank"] <= 3).all())

    def test_filter_posts_function(self):
        """Verifies interactive post filtering logic."""
        filtered = filter_posts(platforms=["Twitter"], min_likes=100, limit=20)
        self.assertLessEqual(len(filtered), 20)
        if not filtered.empty:
            self.assertTrue((filtered["platform"] == "Twitter").all())
            self.assertTrue((filtered["likes"] >= 100).all())

if __name__ == "__main__":
    unittest.main()
