#!/bin/bash
export PYTHONPATH=.:$PYTHONPATH
python -m uvicorn app.main:app --host 0.0.0.0 --port ${X_ZOHO_CATALYST_LISTEN_PORT:-8000}
