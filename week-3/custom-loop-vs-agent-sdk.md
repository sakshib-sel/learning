# Custom Loop Versus Agent SDK

| Area | Custom loop | Agent SDK |
| --- | --- | --- |
| Control | Maximum control over validation, authorization, loop limits, and output handling. | Higher-level loop management with hooks and built-in agent primitives. |
| Code required | More code because the app owns every step. | Less orchestration code for common agent patterns. |
| Tool handling | Explicit allow-list, validation, execution, and tool_result construction. | SDK can manage parts of the loop, but app still owns tool safety. |
| Safety enforcement | Clear deterministic policy layer in application code. | Hooks can enforce policy, but configuration must be audited carefully. |
| Traceability | Straightforward records for each requested action and result. | Depends on SDK tracing and how callbacks/hooks are configured. |
| Failure handling | Fully explicit typed failures. | May be easier to start but requires careful mapping to Sentinel failure categories. |
| Latency and cost | Predictable because max calls and scripted flow are obvious. | May vary more if the agent explores multiple paths. |
| Deployment complexity | Simple Python package and CLI. | More moving parts and SDK-specific hosting/runtime choices. |

## Decision

Sentinel should use the custom bounded loop at this stage.

Reason: Week 3 is about learning the trust boundary. The custom loop makes every
permission check, validator, result limiter, and termination condition visible.
An Agent SDK may become useful later, but only after the same safety policies
are proven in the smaller workflow.

## Agent SDK Implementation

`src/sentinel_claude/agent_sdk_sim.py` contains a bounded Agent SDK demo path.
It uses the documented Agent SDK shape:

- `query()`
- `ClaudeAgentOptions`
- `ResultMessage`
- `allowed_tools=[]`
- explicit `disallowed_tools`
- `permission_mode="dontAsk"`
- `max_turns=2`
- `max_budget_usd=0.05`
- project settings only

The optional SDK is not a replacement for application policy. The same
production-write actions remain denied, and the custom loop remains the source
of mocked operational evidence for this week.
