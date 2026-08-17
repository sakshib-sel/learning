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
  not directly adjustable in this interface.

Alternative routes checked:

- LM Studio local endpoint `http://127.0.0.1:1234/v1/models`: connection
  refused.
- Ollama CLI: not installed.
- LM Studio CLI: not installed.
- `llm` CLI: not installed.
- Common local model ports including `11434`, `1234`, `8000`, `8080`, `5000`,
  `7860`, and `3000`: no model service listening.
- Common hosted-model API-key environment variables: none available.

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
available local/hosted alternatives did not expose a runnable model from this
environment. No parameter effects are estimated. The important finding is that
unsupported settings must be recorded as unsupported instead of guessed.

The runner now supports a hosted OpenAI-compatible API through `--base-url` and
`--api-key-env`, so this table can be updated later if a real model endpoint is
provided.
