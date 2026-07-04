from datetime import datetime
import json
from pathlib import Path

from src.config.paths import ROOT_DIR


def create_eval_run_dir(base_dir: Path = ROOT_DIR / "reports/evaluation") -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = base_dir / timestamp
    run_dir.mkdir(parents=True, exist_ok=False)
    return run_dir


def save_json(path: Path, data: dict | list):
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
