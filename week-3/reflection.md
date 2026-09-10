# Week 3 Reflection

## Which decisions belong to Claude?

Claude may decide which approved evidence would reduce uncertainty and how to
update the incident analysis after receiving tool results.

## Which decisions belong to application code?

Application code controls tool allow-lists, input validation, identity and
authorization, result limits, time limits, maximum tool calls, deterministic
hooks, and final acceptance or failure classification.

## Why does tool access increase both capability and risk?

Tools let Sentinel use evidence that was not in the original prompt. That makes
the analysis more useful, but it also creates risk: bad inputs, unauthorized
requests, prompt-injection content, oversized results, timeouts, and accidental
production actions.

## How were untrusted tool results handled?

Tool results are marked as untrusted evidence. The mocked log injection remains
log text and is never treated as an instruction.

## What guarantees termination?

The loop has a maximum number of tool calls and a maximum execution duration.
The model cannot change those limits.

## Custom loop or Agent SDK?

I would choose the custom loop for Sentinel right now because the safety boundary
is more visible and easier to test. The Agent SDK can be reconsidered later if
Sentinel needs more flexible investigation paths.

## Does Sentinel need multiple agents?

No. The current task does not require separate roles or permissions. A
multi-agent design would add complexity before it adds value.

