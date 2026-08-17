# Generation-Parameter Experiment

Keep the incident and prompt unchanged. Change one parameter at a time. Run each
configuration more than once where possible.

Incident: `../incidents/INC-104.md`

Prompt:

- Recommended: `../prompts/json-output/zero-shot-json.md`
- Alternative: record the exact prompt used below.

Model and interface:

- Model: Codex session model
- Interface: ChatGPT/Codex coding-agent session
- Date: 2026-08-17
- Unsupported parameters: temperature, frequency penalty, top-p, and min-p are
  not directly adjustable in this interface. LM Studio local endpoint
  `http://127.0.0.1:1234/v1/models` was checked and returned connection
  refused, so local parameter sweeps could not be run.

## Runs

| Parameter changed | Value | Run count | Original response location | Brief output change |
| --- | --- | ---: | --- | --- |
| Baseline | Interface default | 1 | `../responses/zero-shot-json-response.md` | Produced valid-looking structured JSON with multiple hypotheses and explicit uncertainty. |
| Temperature | Not supported | 0 | N/A | Skipped; this interface does not expose temperature controls. |
| Frequency penalty | Not supported | 0 | N/A | Skipped; this interface does not expose frequency-penalty controls. |
| Top-p | Not supported | 0 | N/A | Skipped; this interface does not expose top-p controls. |
| Min-p | Not supported | 0 | N/A | Skipped; this interface does not expose min-p controls. |

## Notes

- If a parameter is unavailable in the selected model or interface, record `not
  supported`.
- Do not estimate results for unsupported parameters.
- Preserve original responses in `../responses/` or committed JSONL files under
  `../../outputs/`.

## Result

The selected interface did not support generation-parameter changes, and the
local LM Studio endpoint was unavailable. No parameter effects are estimated.
The important finding is that unsupported settings must be recorded as
unsupported instead of guessed.
