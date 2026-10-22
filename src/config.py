from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "fraud_model.pk1"
SCALER_PATH = BASE_DIR / "models" / "scaler.pk1"
