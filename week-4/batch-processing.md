# Batch Processing

Simulation:

```bash
sentinel-batch-sim --output outputs/week-4/batch-sim.json
```

Batching is appropriate for the fictional overnight collection because:

- urgency is low
- volume is higher than interactive triage
- completion can be delayed
- retries can be handled per failed item
- cost is lower than real-time processing

Real-time Messages API requests are better for active incidents where latency
and immediate human coordination matter.

