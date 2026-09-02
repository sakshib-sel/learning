# Structured Output

The Week 2 application contract is stored in:

```text
schemas/sentinel-analysis.schema.json
```

The validator accepts:

```bash
sentinel-claude validate-json week-2/examples/valid-analysis.json
```

The validator rejects:

```bash
sentinel-claude validate-json week-2/examples/invalid-analysis.json
```

## Difference Between Output Controls

- Asking for JSON through a prompt influences model behavior but does not
  guarantee valid JSON.
- JSON Schema defines the required application contract.
- API-supported structured output can constrain the response shape when the
  model and account support it.
- Parsing JSON only proves syntax.
- Schema validation proves structure.
- Content validation still requires evidence review; valid JSON can still make
  an unsupported causal claim.

