# V2 Risk Log

| Risk ID | Description | Impact | Likelihood | Mitigation | Status |
|---|---|---|---|---|---|
| V2-R01 | DQ checks too weak → dashboard misinformation | High | Medium | Maintain rule catalogue; block HIGH failures | Mitigated |
| V2-R02 | Pipeline paths break on Windows/Linux | Medium | Medium | Use relative paths; provide `.sh` and `.ps1` runners | Mitigated |
| V2-R03 | BI exports drift from KPI definitions | High | Low | Keep `kpi_definitions.csv` and `measure_catalogue.md` in sync | Open |
| V2-R04 | Monitoring not updated after changes | Medium | Medium | Snapshot files + monitoring playbook | Mitigated |

