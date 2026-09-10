# Week 3 Submission

## Deliverables

| Deliverable | Location |
| --- | --- |
| Tool definitions | `src/sentinel_claude/tooling.py`, `week-3/tool-definitions.md` |
| Mock implementations and fictional data | `src/sentinel_claude/tooling.py` |
| Validated bounded loop | `src/sentinel_claude/tool_loop.py` |
| External authorization policy | `ALLOWED_IDENTITIES` in `src/sentinel_claude/tooling.py` |
| Input and output validators | `src/sentinel_claude/tooling.py` |
| Deterministic safety hook | `safety_hook` in `src/sentinel_claude/tooling.py`, `week-3/hooks.md` |
| Prompt-injection regression test | `tests/test_tooling.py` |
| Timeout and maximum-call tests | `tests/test_tooling.py` |
| Bounded Agent SDK implementation | `src/sentinel_claude/agent_sdk_sim.py`, optional install `.[agent]` |
| Custom-loop versus Agent SDK comparison | `week-3/custom-loop-vs-agent-sdk.md` |
| Workflow-versus-agent decision | `week-3/workflow-vs-agent.md` |
| Architecture request flow | `week-3/request-flow.md` |
| Short reflection | `week-3/reflection.md` |
| Timed knowledge check | `week-3/knowledge-check.md` |

## Result

Sentinel can obtain mocked evidence using approved read-only tools. Malformed,
unknown, unauthorized, timed-out, oversized, and over-limit requests are
represented explicitly and cannot execute production actions.

## Repository

https://github.com/sakshib-sel/learning
