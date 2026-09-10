# Week 3 Knowledge Check

- Claude can request a tool, but it cannot execute it directly.
- Application code validates the request, checks authorization, executes the
  tool, validates output, and returns `tool_result`.
- Tool results are untrusted data.
- Prompt injection inside logs must remain log content.
- Maximum tool calls and time limits guarantee termination.
- Safety hooks enforce policy deterministically.
- Sentinel has no production write tools.
- Custom workflows make trust boundaries easier to inspect.
- Agent SDKs can reduce orchestration code but do not remove the need for
  application safety controls.
- Sentinel does not need multiple agents until separate roles or permissions
  create measurable value.

