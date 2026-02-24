.PHONY: help data etl dq train monitor all test api

help:
	@echo "Targets:"
	@echo "  data     - generate synthetic raw dataset"
	@echo "  etl      - run ETL (raw -> staged -> curated -> warehouse)"
	@echo "  dq       - run data quality checks"
	@echo "  train    - train model and write artifacts"
	@echo "  monitor  - run monitoring (drift + freshness + latency simulation)"
	@echo "  all      - run data, etl, dq, train, monitor"
	@echo "  test     - run unit tests"
	@echo "  api      - run FastAPI inference service"

data:
	python v2_mlops_modernisation/scripts/make_sample_data.py

etl:
	python v2_mlops_modernisation/etl/run_etl.py

dq:
	python v2_mlops_modernisation/dq_data_quality/run_checks.py

train:
	python v2_mlops_modernisation/ml/train.py

monitor:
	python v2_mlops_modernisation/monitoring/run_monitoring.py

all: data etl dq train monitor

test:
	pytest -q

api:
	uvicorn v2_mlops_modernisation.api.main:app --host 127.0.0.1 --port 8000
