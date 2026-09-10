# Week 3 -- Bounded Tool Use

Week 3 gives Sentinel controlled access to mocked operational evidence.

Sentinel can request:

- `get_service_metrics`
- `get_dependency_health`
- `search_logs`

All tools use fictional data only. The application validates requests,
authorizes identity, enforces limits, executes mocked tools, validates output,
and treats results as untrusted evidence.

## Run

```bash
python3 -m pip install -e .
sentinel-tool-loop \
  --incident week-1/incidents/INC-104.md \
  --output outputs/week-3/tool-loop.json
```

## Test

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s tests
```

## Optional Agent SDK Demo

```bash
python3 -m pip install -e ".[agent]"
sentinel-agent-sdk-demo --incident week-1/incidents/INC-104.md
```

The custom loop remains the main Week 3 proof because it makes validation,
authorization, hooks, and termination limits explicit.

## Request Flow

```text
Incident
  -> Claude may request a tool
  -> application checks tool allow-list
  -> application validates JSON input
  -> application checks identity and permissions
  -> application enforces time and result-size limits
  -> mocked tool returns fictional evidence
  -> application validates and marks output as untrusted
  -> Claude updates analysis
  -> loop stops on final response or fixed limits
```

## Safety Boundary

Claude can request tools, but it cannot grant itself permissions. Production
write actions such as `delete_deployment`, `restart_production_service`,
`rotate_production_credentials`, and `mark_incident_resolved` are blocked by a
deterministic safety hook.
