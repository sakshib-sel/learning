# Prompt Caching Experiment

Simulation commands:

```bash
sentinel-cache-sim --output outputs/week-4/cache-hit.json
sentinel-cache-sim --change system_prompt --output outputs/week-4/cache-invalidation.json
```

Stable prefix:

- Sentinel system contract
- tool definitions
- runbook context

Changing incident inputs should produce a cache hit. Changing the system prompt,
tool definition, thinking configuration, effort level, or content before the
checkpoint should bypass or invalidate the cache.

Prompt caching reuses a stable prompt prefix. It is not KV cache, conversation
history, application memory, or long-term storage.

