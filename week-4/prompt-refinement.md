# Prompt Refinement

Review checklist:

- Keep durable system instructions in the system prompt.
- Put incident-specific facts in user content.
- Delimit tool outputs as untrusted evidence.
- Use examples that include contradictions and absent evidence.
- Keep output constraints explicit.
- Validate inputs before the model sees them.
- Use failures to refine prompts, but do not use prompts as security controls.
- Treat confident output as unsafe until evidence supports it.

Prompting can influence model behavior, but it is not authorization and not a
security boundary.

