# Workflow Versus Agent Decision

## Workflow

Use a workflow when:

- the sequence is known
- actions are predictable
- deterministic control is important
- branching is limited

## Agent

Use an agent when:

- the next step depends on discovered evidence
- multiple valid tool paths may be needed
- the model must choose between investigation paths
- the workflow cannot be fully known in advance

## Multi-Agent

Use multiple agents only when separate roles, contexts, or permissions provide
measurable value.

## Sentinel Decision

Sentinel is currently a bounded agent inside a workflow shell.

The application controls identity, tools, limits, hooks, and final acceptance.
Within those boundaries, the model may decide which approved evidence would
reduce uncertainty.

Sentinel does not need multiple agents yet. A manager/subagent design would add
complexity without measurable value for the current two-tool investigation.

## Paper Architecture For Later

```text
Incident Manager
  -> Metrics Investigator subagent: read-only metrics
  -> Dependency Investigator subagent: read-only dependency status
  -> Log Reviewer subagent: read-only bounded logs
  -> Safety Reviewer: checks unsupported claims and authority boundaries
```

This should not be implemented until separate permissions or measurable quality
improvements justify it.

