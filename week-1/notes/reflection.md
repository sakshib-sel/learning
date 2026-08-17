# Reflection

## What Increased Consistency Failed To Solve

More structured prompts can make responses easier to compare, but structure does
not make unsupported claims true. A model may consistently produce the same
plausible root cause because the title strongly suggests a deployment-related
failure. That consistency is still not evidence.

Lower temperature can reduce variation, but it cannot create missing facts. It
may even make a single unsupported interpretation appear more stable and
therefore more convincing.

## Safe Boundary

Sentinel can organize evidence, generate hypotheses, identify missing
information, and suggest reversible investigation steps. It cannot confirm the
root cause from incomplete evidence and must not independently approve or
execute production actions.

## What Changed Across Prompt Approaches

The zero-shot response was useful but broad. The one-shot response followed the
example and separated facts, assumptions, hypotheses, and evidence more
consistently. The few-shot response handled competing signals better because the
examples showed that deployment timing, contradictory evidence, and missing
timeline details must be treated carefully.

## What Changed When Generation Parameters Were Adjusted

The selected Codex interface did not expose temperature, frequency penalty,
top-p, or min-p controls. The local LM Studio endpoint was unavailable, so these
experiments were recorded as unsupported rather than estimated.

## Did Greater Consistency Make The Response More Correct?

No. A consistent response can still be wrong if it repeats an unsupported
causal story. In INC-104, the model could consistently prefer `dep-1842` because
the deployment happened three minutes before the alert. That consistency does
not resolve the database-latency signal, the payment-provider errors, or the
credential-history clue.

## Claim Classification

Facts:

- Checkout failures increased from 0.4% to 9%.
- The alert fired at 10:04 UTC.
- `dep-1842` completed at 10:01 UTC.
- Database latency increased at approximately the same time.
- The external payment provider reported intermittent errors.
- A prior similar incident involved an expired service credential.

Hypotheses:

- `dep-1842` introduced a checkout regression.
- Database latency caused or amplified failures.
- Payment-provider degradation caused failed checkouts.
- A credential expired or was misconfigured.

Assumptions:

- The database and payment provider are dependencies in the checkout path.
- Rollback is available and reversible.
- Similar prior symptoms are relevant enough to investigate.

Unsupported claims:

- The deployment definitely caused the incident.
- Rollback will definitely fix the incident.
- The payment provider is definitely responsible.
- The service credential is currently expired.

## Most Important Learning

The most important learning is that a plausible answer is not the same as an
evidence-backed answer. Sentinel is most useful when it slows the team down just
enough to separate facts from hypotheses and asks for the observations that
would actually reduce uncertainty.
