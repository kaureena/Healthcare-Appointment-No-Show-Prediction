# V1 Decision log (ADR-style)

This file captures key decisions made during V1 delivery.

## ADR-001 — Use synthetic dataset for portfolio safety
**Decision:** Use a synthetic dataset with realistic patterns (lead time, reminders, patient history).  
**Reason:** Avoid any privacy risk while keeping outputs believable and reviewer-friendly.

## ADR-002 — Start with interpretable baseline model
**Decision:** Logistic Regression as the baseline.  
**Reason:** Enables clear explanation of drivers to stakeholders and supports governance.

## ADR-003 — Add a non-linear challenger baseline
**Decision:** Add Gradient Boosting as a V1 challenger model.  
**Reason:** Demonstrates versatility and checks whether non-linear effects materially improve performance.

## ADR-004 — Provide threshold policy table
**Decision:** Publish multiple thresholds (0.50/0.35/0.25).  
**Reason:** Outreach capacity varies; precision/recall trade-offs must be transparent.

## ADR-005 — Minimal fairness checks in V1
**Decision:** Slice metrics only (gender/region).  
**Reason:** V1 is baseline; V2 expands monitoring and alerting for drift and fairness.
