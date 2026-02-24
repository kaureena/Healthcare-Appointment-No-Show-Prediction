# V1 Test Matrix

| Area | Test | File | Why it matters |
|---|---|---|---|
| Schema | Required columns exist | `tests/test_schema.py` | Prevents silent breakage of EDA/model scripts |
| Label | No-show rate in realistic band | `tests/test_label_rate.py` | Flags accidental label corruption |
| Features | Processed features sanity | `tests/test_feature_table.py` | Ensures baseline modeling inputs remain stable |

Run:
```bash
pytest -q v1_mca_baseline/tests
```
