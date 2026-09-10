from __future__ import annotations

import unittest
from pathlib import Path

from sentinel_claude.tool_loop import DEFAULT_SCRIPTED_REQUESTS, run_scripted_investigation
from sentinel_claude.tooling import execute_tool_request, safety_hook


class ToolingTests(unittest.TestCase):
    def test_successful_multi_step_investigation(self) -> None:
        result = run_scripted_investigation(incident_path=Path("week-1/incidents/INC-104.md"))
        self.assertEqual(result.status, "accepted")
        self.assertEqual(result.tool_calls, 3)
        self.assertIn("tool_supported_observations", result.final_analysis)

    def test_unknown_tool_rejected(self) -> None:
        record = execute_tool_request(
            {"type": "tool_use", "id": "x", "name": "delete_deployment", "input": {}},
            identity="sentinel-readonly",
        )
        self.assertIn("unknown tool", record.validation_result)
        self.assertEqual(record.execution_result, "not executed")

    def test_invalid_service_rejected(self) -> None:
        request = {
            "type": "tool_use",
            "id": "x",
            "name": "get_service_metrics",
            "input": {
                "service": "admin-api",
                "metric": "error_rate",
                "start_time": "10:00",
                "end_time": "10:10",
            },
        }
        record = execute_tool_request(request, identity="sentinel-readonly")
        self.assertIn("service is not allowed", record.validation_result)

    def test_unauthorized_identity_denied(self) -> None:
        record = execute_tool_request(DEFAULT_SCRIPTED_REQUESTS[0], identity="incident-viewer")
        self.assertEqual(record.validation_result, "allowed")
        self.assertIn("not allowed", record.authorization_result)
        self.assertEqual(record.execution_result, "not executed")

    def test_prompt_injection_is_untrusted_result(self) -> None:
        record = execute_tool_request(DEFAULT_SCRIPTED_REQUESTS[2], identity="sentinel-readonly")
        self.assertEqual(record.execution_result, "success")
        self.assertIs(record.result["trusted_as_instructions"], False)
        line = record.result["observations"][0]["line"]
        self.assertIn("Ignore all previous instructions", line)

    def test_timeout_reported_without_success(self) -> None:
        request = dict(DEFAULT_SCRIPTED_REQUESTS[2])
        request["input"] = dict(request["input"], query="simulate_timeout")
        record = execute_tool_request(request, identity="sentinel-readonly")
        self.assertIn("timeout", record.execution_result)
        self.assertIn("do not claim evidence was retrieved", record.final_sentinel_behaviour)

    def test_malformed_output_rejected(self) -> None:
        request = dict(DEFAULT_SCRIPTED_REQUESTS[2])
        request["input"] = dict(request["input"], query="simulate_malformed")
        record = execute_tool_request(request, identity="sentinel-readonly")
        self.assertIn("malformed output", record.execution_result)

    def test_max_call_limit_enforced(self) -> None:
        result = run_scripted_investigation(
            incident_path=Path("week-1/incidents/INC-104.md"),
            max_tool_calls=1,
        )
        self.assertEqual(result.status, "failure")
        self.assertEqual(result.final_analysis["failure"]["code"], "tool_call_limit_exceeded")

    def test_safety_hook_blocks_production_write(self) -> None:
        decision = safety_hook("mark_incident_resolved")
        self.assertFalse(decision["allowed"])
        self.assertTrue(decision["human_approval_required"])


if __name__ == "__main__":
    unittest.main()

