# Few-Shot Prompt and Original Response

## Prompt Used

See `../prompts/few-shot.md`.

## Original Model Response

Known facts

- Checkout failures rose from 0.4% to 9%.
- The alert fired at 10:04 UTC.
- `checkout-api` deployment `dep-1842` completed at 10:01 UTC.
- Database latency rose around the same time.
- The external payment provider reported intermittent errors.
- A previous incident with similar symptoms involved an expired service
  credential.
- The incident brief contains initial reports only.

Assumptions

- Checkout requests depend on the database and external payment provider.
- Similar symptoms may indicate a useful investigation path, but not the same
  root cause.
- Rollback is technically possible, but the brief does not prove it is safe or
  sufficient.

Missing information

- Confirmed timeline with first bad request, deployment completion, database
  latency onset, and payment-provider error onset.
- Dominant checkout error codes.
- Failed request traces.
- Credential expiry and authentication status.
- Deployment contents.
- Whether any unaffected checkout paths exist.

Candidate hypotheses

1. Deployment regression in `checkout-api`.
2. Database latency caused checkout failures.
3. External payment-provider intermittent errors caused checkout failures.
4. Credential expiration or credential misconfiguration.
5. Multiple contributing factors.

Supporting evidence for each hypothesis

- Deployment regression: deployment completed shortly before the alert.
- Database latency: latency increased in the same time window.
- Payment provider: provider reported intermittent errors.
- Credential issue: similar prior incident involved expired credentials.
- Multiple factors: the brief contains several simultaneous signals.

Contradicting evidence for each hypothesis

- Deployment regression: no change diff, stack trace, or rollback outcome is
  supplied.
- Database latency: no evidence shows latency is the first failure in traces.
- Payment provider: no evidence ties provider errors to the affected checkout
  attempts.
- Credential issue: previous incidents can mislead if treated as proof.
- Multiple factors: simultaneity does not establish interaction.

Evidence needed to distinguish between hypotheses

- Trace sample from failed checkouts showing the failing span.
- Error-code counts grouped by internal error, database timeout, provider error,
  and auth/credential error.
- Credential health and expiry check.
- Payment-provider error timestamps and affected methods/regions.
- Deployment diff for `dep-1842`.
- Safe rollback/canary evidence, if approved by incident command.

Reversible next actions

- Triage failed checkout traces for the dominant error class.
- Check credential validity and recent rotations.
- Compare provider errors with checkout failures by timestamp and payment
  method.
- Prepare rollback instructions and risk notes, but do not claim rollback is the
  correct action yet.

Uncertainty statement

The most likely initial investigation path is `dep-1842` because the deployment
preceded the alert by three minutes. However, the safest conclusion is that the
root cause is unconfirmed. Rollback should be readied, not automatically
recommended as the answer, until evidence shows the deployment is causal or the
incident commander chooses rollback as a time-sensitive mitigation.
