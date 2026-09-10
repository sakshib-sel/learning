# Tool Definitions

Definitions are implemented in `src/sentinel_claude/tooling.py`.

## get_service_metrics

Purpose: retrieve approved fictional metrics for `checkout-api`.

Allowed metrics:

- `error_rate`
- `database_latency_ms`

Limits:

- service must be `checkout-api`
- time range must be HH:MM
- end time must be after start time
- maximum time range is 30 minutes
- maximum result size is 5 points

## get_dependency_health

Purpose: retrieve fictional health for approved dependencies.

Allowed dependencies:

- `payments-provider`
- `orders-db`

Limits:

- service must be `checkout-api`
- requested time must be HH:MM

## search_logs

Purpose: search bounded fictional checkout logs for safe diagnostic terms.

Limits:

- service must be `checkout-api`
- query length is limited to 80 characters
- shell-like characters are rejected
- maximum result size is 5 lines

## Error Results

Tool requests may be rejected for:

- unknown tool
- invalid input
- unauthorized identity
- timeout
- malformed output
- oversized output
- maximum-call limit

