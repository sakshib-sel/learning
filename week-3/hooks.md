# Deterministic Safety Hook

Hook implementation: `safety_hook` in `src/sentinel_claude/tooling.py`.

Blocked actions:

- `delete_deployment`
- `restart_production_service`
- `rotate_production_credentials`
- `mark_incident_resolved`

Recorded fields:

- requested action
- reason for rejection
- applicable policy
- whether human approval would be required

Policy:

```text
read_only_incident_investigation
```

A prompt can request safe behavior, but the hook enforces it deterministically.

