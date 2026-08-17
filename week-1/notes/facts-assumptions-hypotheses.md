# Facts, Assumptions, Hypotheses, and Missing Evidence

## Facts

- `INC-104` is titled `Checkout failures after a deployment`.

## Assumptions To Avoid

- Do not assume the deployment caused the incident.
- Do not assume rollback is safe or sufficient.
- Do not assume the affected component is the checkout API without evidence.
- Do not assume all users, regions, payment methods, or devices are affected.

## Candidate Hypotheses

| Hypothesis | Supporting evidence | Contradicting evidence | Evidence needed |
| --- | --- | --- | --- |
| Deployment regression | Title mentions failures after deployment | No incident details yet | Timeline, changed files, logs, rollback/canary outcome |
| External payment dependency | Checkout failures often depend on payment providers | No provider evidence yet | Provider status, payment-method breakdown, dependency traces |
| Configuration or feature-flag issue | Deployment-adjacent config changes can affect checkout | No config evidence yet | Config diff, flag audit, segment impact |
| Client-side checkout issue | Checkout can fail due to frontend assets or validation | No device/browser evidence yet | Browser logs, synthetic tests, client error rates |

## Unsupported Claim To Watch For

"The deployment caused the checkout failures and rollback will fix the incident."

Why unsupported: the available evidence establishes only a title-level temporal
relationship, not causation or rollback safety.

