# Week 1 Submission

## Prompt Comparison

- Zero-shot prompt: `prompts/zero-shot.md`
- Zero-shot response: `responses/zero-shot-response.md`
- One-shot prompt: `prompts/one-shot.md`
- One-shot response: `responses/one-shot-response.md`
- Few-shot prompt: `prompts/few-shot.md`
- Few-shot response: `responses/few-shot-response.md`

JSON-output prompts:

- Zero-shot JSON prompt: `prompts/json-output/zero-shot-json.md`
- Zero-shot JSON response: `responses/zero-shot-json-response.md`
- One-shot JSON prompt: `prompts/json-output/one-shot-json.md`
- One-shot JSON response: `responses/one-shot-json-response.md`
- Few-shot JSON prompt: `prompts/json-output/few-shot-json.md`
- Few-shot JSON response: `responses/few-shot-json-response.md`

Comparison findings:

- Few-shot JSON was the strongest prompt because it preserved facts, represented
  competing hypotheses, and explicitly listed unsupported claims to avoid.
- Zero-shot was acceptable but broader.
- One-shot improved separation of facts, assumptions, hypotheses, missing
  evidence, and next actions.

## Generation-Parameter Experiment

See `experiments/generation-parameters.md`.

Required:

- Keep incident and prompt unchanged.
- Change one parameter at a time.
- Record temperature, frequency penalty, top-p, and min-p results where
  supported.
- Record unsupported options as `not supported`.

Result: the selected Codex interface does not expose temperature, frequency
penalty, top-p, or min-p controls. The local LM Studio endpoint was unavailable,
so no parameter effects were estimated.

## Short Reflection

See `notes/reflection.md`.

Answer:

- What changed across the prompt approaches? Structure and uncertainty handling
  improved from zero-shot to one-shot to few-shot.
- What changed when generation parameters were adjusted? No parameter changes
  were possible in the selected interface; unsupported settings were recorded.
- Did greater consistency make the response more correct? No. Consistency can
  repeat an unsupported causal claim.
- Which claims were facts, hypotheses, assumptions, or unsupported? See
  `notes/reflection.md` and `notes/facts-assumptions-hypotheses.md`.
- What was the most important learning? Evidence and boundaries matter more
  than confidence or polish.

## Repository Link

Add GitHub repository link here after publishing:

https://github.com/sakshib-sel/learning
