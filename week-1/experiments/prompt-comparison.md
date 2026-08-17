# Prompt Comparison

Keep the incident, model, and generation settings unchanged while comparing
zero-shot, one-shot, and few-shot prompts. Do not select a preferred prompt from
a single response.

## Evaluation Table

| Prompt | Runs | Preservation of supplied facts | Unsupported claims | Missing information recognized | Hypothesis quality and diversity | Uncertainty expression | Response consistency | Token usage / latency |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Zero-shot | 1 | Preserved all supplied INC-104 facts | Avoided direct unsupported root-cause claim; still framed deployment as a strong candidate | Identified timeline, traces, credential status, and rollback evidence as missing | Covered deployment, database, payment provider, credential, and multi-factor hypotheses | Clear statement that root cause cannot be confirmed | N/A; one preserved response in this interface | Not available in Codex interface |
| One-shot | 1 | Preserved all supplied INC-104 facts in tighter bullet form | Avoided saying rollback would definitely help | More explicit about first-failure time, error types, affected population, and rollback safety | Similar hypotheses, with clearer evidence needed for each | Strong uncertainty wording; deployment plausible but not confirmed | N/A; one preserved response in this interface | Not available in Codex interface |
| Few-shot | 1 | Preserved all supplied INC-104 facts and emphasized initial-report limitation | Avoided causal certainty and avoided rollback certainty | Most complete list of timeline, trace, credential, deployment, and unaffected-path gaps | Best hypothesis separation; included multiple contributing factors | Strongest safety boundary around rollback and incident-command decision | N/A; one preserved response in this interface | Not available in Codex interface |

## Concise Comparison

- Zero-shot: produced a reasonable structure and did not claim a confirmed root
  cause, but its guidance was broader.
- One-shot: better separated facts, assumptions, evidence, and actions because
  the example demonstrated the expected style.
- Few-shot: handled competing signals best. It was least likely to over-weight
  the deployment because the examples included contradictory evidence and cases
  without deployment causes.

## Preferred Prompt, If Any

Preferred prompt:

Few-shot JSON prompt.

Reason:

It preserved the facts, produced machine-checkable structure, represented
competing hypotheses, and explicitly listed unsupported claims to avoid.

Residual risks:

JSON structure controls the shape of the answer, not factual correctness. The
model can still overstate likelihood, omit evidence, or produce valid JSON that
contains weak reasoning.
