# Facts, Assumptions, Hypotheses, and Missing Evidence

## Facts

- At 10:04 UTC, the checkout error-rate alert fired.
- Checkout failures increased from 0.4% to 9%.
- Deployment `dep-1842` for `checkout-api` completed at 10:01 UTC.
- Database latency increased at approximately the same time.
- The external payment provider reported intermittent errors.
- A previous incident with similar symptoms involved an expired service
  credential.
- The incident brief is an initial report, not a confirmed timeline or root
  cause.

## Assumptions To Avoid

- Do not assume the deployment caused the incident.
- Do not assume rollback is safe or sufficient.
- Do not assume the affected component is the checkout API without evidence.
- Do not assume all users, regions, payment methods, or devices are affected.

## Candidate Hypotheses

| Hypothesis | Supporting evidence | Contradicting evidence | Evidence needed |
| --- | --- | --- | --- |
| Deployment regression | Checkout failures rose after `checkout-api` deployment completed | Database latency and payment-provider errors happened at approximately the same time | Changed files, logs, traces, canary/staging reproduction, rollback outcome if approved |
| External payment dependency | Payment provider reported intermittent errors | Brief does not prove provider errors match failed checkouts | Provider status details, payment-method breakdown, dependency traces |
| Database latency | Database latency increased at approximately the same time | Brief does not prove latency preceded checkout failures | DB metrics, slow queries, saturation signals, request traces |
| Credential issue | Similar previous incident involved an expired service credential | Previous similarity is not current evidence | Credential expiry status, auth failure logs, recent rotation history |
| Configuration or feature-flag issue | Deployment-adjacent config changes can affect checkout | No config or flag evidence supplied | Config diff, flag audit, segment impact |

## Unsupported Claim To Watch For

"The deployment caused the checkout failures and rollback will fix the incident."

Why unsupported: the available evidence establishes only a title-level temporal
relationship plus several competing signals. It does not establish causation or
rollback safety.
