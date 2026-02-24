# Install & Runbook

## Setup
```bash
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run pipeline
```bash
make all
```

Outputs are written under:
- `v2_mlops_modernisation/data/`
- `v2_mlops_modernisation/warehouse/`
- `v2_mlops_modernisation/reports/`

## Run API
```bash
make api
```

Then open:
- http://127.0.0.1:8000/docs

## Testing
```bash
make test
```
