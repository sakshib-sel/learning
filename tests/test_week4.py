from __future__ import annotations

import unittest
from pathlib import Path

from sentinel_claude.batch_sim import simulate_batch
from sentinel_claude.cache_sim import simulate_cache
from sentinel_claude.context_engineering import compact_context, prune_tool_results
from sentinel_claude.evaluation import QUALITY_THRESHOLD, evaluate_cases, load_cases


class Week4Tests(unittest.TestCase):
    def test_optimized_evaluation_passes_threshold(self) -> None:
        cases = load_cases(Path("week-4/evaluation/cases.json"))
        results = evaluate_cases(cases, "optimized")
        self.assertTrue(all(result.quality_score >= QUALITY_THRESHOLD for result in results))
        self.assertTrue(all(result.passed for result in results))

    def test_baseline_catches_timestamp_failure(self) -> None:
        cases = load_cases(Path("week-4/evaluation/cases.json"))
        results = evaluate_cases(cases, "baseline")
        failed = [result for result in results if result.case_id == "INC-109"][0]
        self.assertFalse(failed.passed)
        self.assertEqual(failed.first_divergence, "model_output")

    def test_cache_hit_and_invalidation(self) -> None:
        self.assertTrue(simulate_cache()["cache_hit"])
        self.assertFalse(simulate_cache("system_prompt")["cache_hit"])

    def test_batch_cost_is_lower_than_realtime(self) -> None:
        result = simulate_batch()
        self.assertLess(result["batch_cost_usd"], result["realtime_cost_usd"])

    def test_context_compaction_preserves_critical_fields(self) -> None:
        context = [
            {
                "evidence_id": "ev-1",
                "source": "logs",
                "negative_finding": "no credential error",
                "contradiction": "timestamps disagree",
                "uncertainty": "timezone unresolved",
                "decision": "do not build causal timeline",
                "observations": [1, 2, 3, 4],
            }
        ]
        pruned = prune_tool_results(context, max_observations=2)
        self.assertEqual(len(pruned[0]["observations"]), 2)
        compacted = compact_context(context)
        self.assertEqual(compacted["evidence_ids"], ["ev-1"])
        self.assertEqual(compacted["contradictions"], ["timestamps disagree"])


if __name__ == "__main__":
    unittest.main()

