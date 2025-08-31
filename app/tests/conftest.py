# app/tests/conftest.py
import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]   # .../TFM_CERT_Support_System/app
API_DIR = APP_DIR / "api"

# Asegura que 'app' y 'app/api' están en sys.path (al principio)
for p in (str(API_DIR), str(APP_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

