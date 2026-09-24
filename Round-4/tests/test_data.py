"""
Unit tests for data loading and schema integrity.
"""

import unittest
from pathlib import Path
import sys

# Ensure Round-4 root is in sys.path
ROUND4_DIR = Path(__file__).resolve().parent.parent
if str(ROUND4_DIR) not in sys.path:
    sys.path.insert(0, str(ROUND4_DIR))

from src.data_loader import (
    load_round1_posts,
    load_round1_users,
    load_round1_corrupted,
    load_round2_training,
    load_round3_reactions,
    get_sqlite_info,
)

class TestData(unittest.TestCase):
    """Test suite verifying data accessibility, schema, and volume constraints."""

    def test_round1_posts_schema_and_volume(self):
        """Verifies Round 1 cleaned posts dataset (12,000 rows)."""
        df = load_round1_posts()
        self.assertEqual(len(df), 12000)
        expected_cols = ["post_id", "user_id", "platform", "text_content", "timestamp", "likes", "shares", "comments"]
        for c in expected_cols:
            self.assertIn(c, df.columns)
        self.assertEqual(df["post_id"].isna().sum(), 0)

    def test_round1_users_schema_and_volume(self):
        """Verifies Round 1 cleaned users dataset (1,500 rows)."""
        df = load_round1_users()
        self.assertEqual(len(df), 1500)
        expected_cols = ["user_id", "location", "language", "account_created", "follower_count"]
        for c in expected_cols:
            self.assertIn(c, df.columns)
        self.assertEqual(df["user_id"].isna().sum(), 0)

    def test_round2_training_balance(self):
        """Verifies Round 2 NLP training data balance (9,000 rows, 3k each)."""
        df = load_round2_training()
        self.assertEqual(len(df), 9000)
        counts = df["sentiment_label"].value_counts().to_dict()
        self.assertEqual(counts["Negative"], 3000)
        self.assertEqual(counts["Neutral"], 3000)
        self.assertEqual(counts["Positive"], 3000)

    def test_round3_reaction_archive(self):
        """Verifies Round 3 reaction archive (204 rows)."""
        df = load_round3_reactions()
        self.assertEqual(len(df), 204)
        self.assertIn("predicted_sentiment", df.columns)
        self.assertIn("date", df.columns)

    def test_sqlite_core_integrity(self):
        """Verifies read-only SQLite database integrity and zero foreign-key violations."""
        info = get_sqlite_info()
        self.assertEqual(info["integrity"], "ok")
        self.assertEqual(info["foreign_key_violations"], 0)
        self.assertEqual(info["row_counts"]["posts"], 12000)
        self.assertEqual(info["row_counts"]["users"], 1500)

if __name__ == "__main__":
    unittest.main()
