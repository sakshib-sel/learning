# Pre-Model Analysis

Complete this before consulting a model.

## 1. Known Facts

From the currently available course brief only:

- The incident is named `INC-104 -- Checkout failures after a deployment`.
- The affected area is checkout.
- A deployment is relevant enough to appear in the title.

The full incident details are not yet available, so no specific root cause,
timeline, affected region, error rate, customer impact, service owner, or
mitigation can be established.

## 2. Possible Causes

Possible causes to investigate, not conclusions:

- A checkout API regression introduced by the deployment.
- A configuration or feature-flag change released with the deployment.
- A dependency problem in payment, inventory, tax, shipping, fraud, or identity.
- A client-side checkout issue caused by asset, JavaScript, or validation
  changes.
- A pre-existing issue that happened to become visible after the deployment.

## 3. Correlation But Not Causation

- The phrase "after a deployment" is temporal correlation only.
- A recent deployment may be a strong lead, but it does not prove the deployment
  caused checkout failures.

## 4. Missing Information

- Exact incident timeline.
- Deployment time, scope, services, and changed components.
- Error messages, logs, traces, and metrics before and after deployment.
- Affected checkout paths, payment methods, regions, devices, and customer
  segments.
- Whether dependencies reported incidents.
- Whether rollback or mitigation was attempted and what changed afterward.
- Runbook instructions and approval boundaries.

## 5. Reversible Next Action

- Gather the incident timeline and compare checkout errors before and after the
  deployment.
- Check whether a staging or canary environment reproduces the failure.
- Review changed checkout paths and feature flags.
- Prepare rollback as a human-approved option, but do not execute or recommend
  it as confirmed without evidence.

## 6. What Would Change This Conclusion

- Direct evidence that failures began immediately after a specific deployed
  change and stop after reverting it.
- Logs or traces linking the failures to a changed component.
- Contradictory evidence showing failures began before the deployment.
- Dependency status or provider logs showing an external outage aligned with the
  failures.

