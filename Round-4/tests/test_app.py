"""
Smoke tests for Streamlit application modules, page imports, and model inference.
"""

import unittest
import importlib
from pathlib import Path
import sys

# Ensure Round-4 root is in sys.path
ROUND4_DIR = Path(__file__).resolve().parent.parent
if str(ROUND4_DIR) not in sys.path:
    sys.path.insert(0, str(ROUND4_DIR))

from src.model import load_sentiment_pipeline, load_topic_pipeline, predict_dual_head, PRESET_EXAMPLES
from src.metrics import FROZEN_SENTIMENT_BENCHMARKS, FROZEN_TOPIC_BENCHMARKS

class TestApp(unittest.TestCase):
    """Test suite ensuring all pages and inference components operate without side effects."""

    def test_import_src_modules(self):
        """Verifies that all core src modules import cleanly."""
        importlib.import_module("src.utils")
        importlib.import_module("src.data_loader")
        importlib.import_module("src.preprocessing")
        importlib.import_module("src.analysis")
        importlib.import_module("src.model")
        importlib.import_module("src.metrics")

    def test_import_components_and_services(self):
        """Verifies that all component, repository, and service modules import cleanly."""
        for mod in [
            "components.header",
            "components.sidebar",
            "components.findings",
            "components.charts",
            "components.metric_cards",
            "components.tables",
            "components.filters",
            "repositories.dataset_repository",
            "repositories.model_repository",
            "repositories.sqlite_repository",
            "services.data_service",
            "services.nlp_service",
            "services.round1_service",
            "services.round3_service",
            "services.insight_service",
        ]:
            importlib.import_module(mod)

    def test_import_page_modules(self):
        """Verifies that all 4 Streamlit page scripts import without syntax or runtime errors."""
        importlib.import_module("pages.01_Overview")
        importlib.import_module("pages.02_Analysis")
        importlib.import_module("pages.03_Interactive_Explorer")
        importlib.import_module("pages.04_Methodology")

    def test_model_loading_and_calibrated_inference(self):
        """Verifies live inference returns calibrated posterior probabilities summing to 1.0."""
        res = predict_dual_head("Critical security incident: unauthorized login detected.")
        self.assertIn(res["sentiment"]["label"], ["Positive", "Neutral", "Negative"])
        self.assertIn(res["topic"]["label"], ["Account_Security", "Community_Discussion", "Feature_Feedback", "Technical_Issues"])
        
        # Verify probability sum is 1.0
        prob_sum = sum(res["sentiment"]["probabilities"].values())
        self.assertAlmostEqual(prob_sum, 1.0, places=4)

        # Verify margin scores are present for all 4 topic classes
        self.assertEqual(len(res["topic"]["margins"]), 4)

    def test_preset_domain_examples(self):
        """Verifies all preset examples execute inference without crashing."""
        for p in PRESET_EXAMPLES:
            res = predict_dual_head(p["text"])
            self.assertIsNotNone(res["sentiment"]["label"])
            self.assertIsNotNone(res["topic"]["label"])

if __name__ == "__main__":
    unittest.main()
