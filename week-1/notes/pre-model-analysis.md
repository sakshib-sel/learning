# Pre-Model Analysis

Complete this before consulting a model.

## 1. Known Facts

- At 10:04 UTC, the checkout error-rate alert fired.
- Checkout failures increased from 0.4% to 9%.
- Deployment `dep-1842` for `checkout-api` completed at 10:01 UTC.
- Database latency increased at approximately the same time.
- The external payment provider reported intermittent errors.
- A previous incident with similar symptoms involved an expired service
  credential.
- The incident director asked what the likely cause is and whether to roll back.
- The brief contains initial reports, not a confirmed timeline or root cause.

## 2. Possible Causes

Possible causes to investigate, not conclusions:

- A checkout API regression introduced by the deployment.
- A configuration, feature-flag, or credential issue released with or exposed by
  the deployment.
- A dependency problem in payment, inventory, tax, shipping, fraud, or identity.
- A client-side checkout issue caused by asset, JavaScript, or validation
  changes.
- Database latency causing checkout failures.
- External payment provider intermittent errors causing or amplifying failures.
- An expired service credential, because a previous similar incident had that
  cause.
- A pre-existing issue that happened to become visible after the deployment.

## 3. Correlation But Not Causation

- The alert fired three minutes after deployment `dep-1842` completed, but
  timing alone does not prove the deployment caused checkout failures.
- Database latency increased at approximately the same time, but the brief does
  not prove whether it is cause, consequence, or unrelated.
- The payment provider reported intermittent errors, but the brief does not
  prove whether those errors match the checkout failures.
- The previous credential incident is relevant pattern-matching evidence, not
  proof that credentials are failing now.

## 4. Missing Information

- Confirmed minute-by-minute incident timeline.
- Deployment scope and changed components for `dep-1842`.
- Checkout error messages, logs, traces, and metrics before and after deployment.
- Affected checkout paths, payment methods, regions, devices, and customer
  segments.
- Whether database latency preceded checkout failures or followed increased load.
- Whether payment-provider errors line up with failed checkout attempts.
- Current credential status and recent credential rotation history.
- Whether rollback or mitigation was attempted and what changed afterward.
- Runbook instructions and approval boundaries.

## 5. Reversible Next Action

- Gather a short timeline joining deployment completion, checkout errors,
  database latency, and payment-provider errors.
- Check logs/traces for failing checkout requests and classify failures by
  internal errors, database calls, payment-provider calls, and credential errors.
- Check credential health and recent rotations.
- Review changed checkout paths, configuration, and feature flags in `dep-1842`.
- Prepare rollback as a human-approved option, but do not execute or recommend
  it as confirmed without evidence.

## 6. What Would Change This Conclusion

- Direct evidence that failures began immediately after a specific deployed
  change and stop after reverting it.
- Logs or traces linking failures to a changed component in `checkout-api`.
- Evidence that checkout failures began before deployment `dep-1842`.
- Evidence that payment-provider errors align with failed checkout attempts and
  successful internal processing.
- Evidence that database latency is the leading cause rather than a downstream
  symptom.
- Evidence that a credential is expired or that credential checks are healthy.
