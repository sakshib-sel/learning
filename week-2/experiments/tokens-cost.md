# Tokens, Latency, Stop Reason, And Cost

Record at least one request:

| Field | Value |
| --- | --- |
| Model |  |
| Input tokens |  |
| Output tokens |  |
| Thinking tokens |  |
| Maximum output tokens |  |
| Latency |  |
| Estimated cost |  |
| Stop reason |  |

The app records token and stop metadata when returned by the SDK. Estimated cost
is calculated from the local pricing table for supported model IDs.

## Notes

- The same prompt may tokenize differently across models because tokenizers can
  differ by model family.
- Context length affects request size because all included instructions,
  incidents, images, and conversation history consume context.
- Repeated system instructions consume tokens unless prompt caching applies.
- `max_tokens` is an upper bound, not a promise that the model will generate
  exactly that many tokens.

