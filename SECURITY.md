# Security

## Secrets
- Do not commit `.env` files.
- Use `.env.example` as a template.

## Data policy
- Only synthetic data is used.
- No real patient data should ever be committed.

## Dependencies
This repository pins versions in `requirements.txt` for reproducibility.

For a real production build, use:
- dependency scanning
- containerisation
- secrets manager
- separate runtime vs dev dependencies
