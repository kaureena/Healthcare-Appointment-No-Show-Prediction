# API (FastAPI)

Run locally:

```bash
pip install -r requirements.txt
uvicorn v2_mlops_modernisation.api.main:app --host 127.0.0.1 --port 8000
```

Open Swagger:
- http://127.0.0.1:8000/docs

Example request body:

```json
{
  "lead_time_days": 12,
  "sms_reminder_sent": 1,
  "prior_no_show_count": 1,
  "prior_show_count": 4,
  "age": 42,
  "gender": "F",
  "age_band": "30-44",
  "appointment_type": "General",
  "booking_channel": "Online",
  "appointment_hour": 10,
  "appointment_is_weekend": 0,
  "deprivation_index": 0.43,
  "clinic_id": "C01",
  "neighbourhood_id": "N005",
  "clinic_type": "Primary Care",
  "clinic_region": "North"
}
```
