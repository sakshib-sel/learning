# Multimodal Input

Fictional dashboard image:

```bash
sentinel-claude make-dashboard --output week-2/assets/fictional-dashboard.png
```

Request:

```bash
sentinel-claude analyze \
  --incident week-1/incidents/INC-104.md \
  --image week-2/assets/fictional-dashboard.png \
  --model claude-sonnet-5
```

## Observation Tracking

| Observation | Source | Classification |
| --- | --- | --- |
| Checkout failures increased from 0.4% to 9% | Text | Fact |
| Alert fired at 10:04 UTC | Text | Fact |
| Dashboard appears to show an elevated red metric card | Image | Model observation, must be checked |
| Deployment caused the incident | Neither | Unsupported conclusion |

Image interpretation is model-generated output and must be evaluated.

