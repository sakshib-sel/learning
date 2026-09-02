# Week 2 Knowledge Check

- Claude Messages API requests include a model, system instructions, messages,
  and limits such as `max_tokens`.
- Streaming returns partial events; Sentinel accepts only a complete final
  message.
- JSON parsing is not enough. The parsed object must match the Sentinel schema.
- Schema-valid content can still contain unsupported conclusions.
- Input, configuration, integration, runtime, and model-output failures should
  be classified separately.
- Tokens, latency, stop reason, and cache usage are observability data, not
  proof of correctness.
- Prompt caching reuses stable prompt prefixes; it is not the same as memory.
- Claude may request tools, but application code validates and executes them.
- `CLAUDE.md` guides Claude Code behavior but is not a security boundary.

