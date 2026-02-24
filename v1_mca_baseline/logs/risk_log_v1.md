# V1 Risk Log

| Risk ID | Description | Impact | Likelihood | Mitigation | Status |
|---|---|---|---|---|---|
| V1-R01 | Missing or null patient_id values in raw dataset | High | Medium | Filtered invalid records during preprocessing | Resolved |
| V1-R02 | Inconsistent datetime formats affecting lead time calculation | High | Medium | Standardised datetime parsing and validated formats | Resolved |
| V1-R03 | Imbalanced no-show vs attended records affecting model accuracy | Medium | High | Evaluated class distribution and monitored performance metrics | Accepted |
| V1-R04 | Limited feature availability reducing predictive capability | Medium | Medium | Created derived features such as lead_time_days and appointment_dow | Resolved |
| V1-R05 | Duplicate appointment records causing analysis distortion | High | Low | Identified and removed duplicate records during cleaning | Resolved |
| V1-R06 | Data quality inconsistencies across multiple records | Medium | Medium | Performed validation checks and manual review during EDA | Resolved |
| V1-R07 | Overfitting risk due to small analysis period | Medium | Low | Used validation split and evaluated model performance | Mitigated |
| V1-R08 | Lack of structured storage limiting scalability | Low | High | Documented need for structured warehouse architecture | Closed |
| V1-R09 | Manual preprocessing introducing potential human error | Medium | Medium | Documented preprocessing steps in notebooks | Mitigated |
| V1-R10 | Lack of monitoring for model performance over time | Medium | High | Identified monitoring as future enhancement (implemented in V2) | Closed |

