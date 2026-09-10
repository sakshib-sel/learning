# Week 4 Knowledge Check

1. Model choice depends on workload requirements, not model novelty.
2. Fast mode favors latency.
3. Extended thinking may improve hard reasoning but adds cost.
4. Adaptive thinking lets the model decide when more reasoning is useful.
5. Effort controls tune reasoning depth where supported.
6. `max_tokens` is a limit, not a guaranteed output length.
7. Normal cost uses measured average tokens.
8. Worst-case cost uses max context, max tools, and max output.
9. Prompt caching reuses stable prompt prefixes.
10. Prompt caching is not KV cache.
11. Prompt caching is not long-term memory.
12. Cache invalidation can happen when content before the checkpoint changes.
13. Batches are suitable for non-urgent offline processing.
14. Real-time requests are better for active incidents.
15. Context growth increases cost and drift risk.
16. Compaction must preserve evidence IDs and contradictions.
17. Negative findings are critical evidence.
18. Evaluations must use fixed cases across configurations.
19. A model migration is a behavioral change.
20. Failures should identify whether the first divergence came from model
    output, prompt/context, tool execution, parser, or integration.

