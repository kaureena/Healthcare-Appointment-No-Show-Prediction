# RULE_17: Label quality

## Why this rule exists
No-show label must be 0/1 and distribution must be plausible.

## What it protects
- Dashboard correctness (no blank visuals due to missing fields)
- Model training stability (no schema drift between runs)
- Monitoring accuracy (drift/latency alerts depend on consistent keys)

## Related expectations (examples)
This rule is enforced using multiple expectation checks in:
- `dq_data_quality/expectations/`

Typical checks used:
- `expect_required_columns`
- `expect_unique`
- `expect_between`
- `expect_in_set`
- `expect_non_negative`

## Failure handling
If this rule fails:
1. Inspect `reports/dq_report.html` for failing expectations and details
2. Check whether the issue is:
   - upstream data defect (fix generator / ingestion)
   - transformation bug (fix ETL)
   - incorrect assumption (update expectation with justification)
3. Record decision in the logbook and update the issue register.
