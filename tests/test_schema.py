from __future__ import annotations

import json
import unittest
from pathlib import Path

from sentinel_claude.schema import validate_analysis


ROOT = Path(__file__).resolve().parents[1]


class SchemaTests(unittest.TestCase):
    def test_valid_analysis(self) -> None:
        data = json.loads((ROOT / "week-2/examples/valid-analysis.json").read_text())
        self.assertEqual(validate_analysis(data), [])

    def test_invalid_analysis(self) -> None:
        data = json.loads((ROOT / "week-2/examples/invalid-analysis.json").read_text())
        errors = validate_analysis(data)
        self.assertTrue(errors)
        self.assertIn("facts must be a list of strings", errors)


if __name__ == "__main__":
    unittest.main()

