# Architecture Request Flow

```text
User incident brief
  -> Sentinel app validates incident input
  -> Claude receives incident and approved tool definitions
  -> Claude may return tool_use
  -> Sentinel app validates tool name and JSON input
  -> Sentinel app checks identity against read-only policy
  -> Sentinel app enforces time range, result size, max calls, and max duration
  -> Mock tool executes against fictional data
  -> Sentinel app validates result shape
  -> Sentinel app marks result as untrusted evidence
  -> tool_result is returned to Claude
  -> Claude updates analysis
  -> app stops on final answer or deterministic limit
```

Important boundary:

```text
Claude chooses what evidence to request.
Application code decides what is allowed to execute.
```

