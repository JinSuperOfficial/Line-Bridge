import json
import os
from pathlib import Path
from typing import Any, Dict


class SaveSystem:
    def __init__(self) -> None:
        appdata = os.getenv("APPDATA") or str(Path.home() / ".linebridge")
        self.save_dir = Path(appdata) / "LineBridge"
        self.save_file = self.save_dir / "data.json"
        self.default_data = {
            "username": "",
            "level": 0,
            "hints": 0,
            "progress": {},
            "achievements": [],
            "rewards": 0,
            "streak_success": 0,
            "fail_count": 0,
            "night_wins": 0,
            "shape_set": [],
            "easter_eggs": [],
        }

    def load(self) -> Dict[str, Any]:
        self.save_dir.mkdir(parents=True, exist_ok=True)
        if not self.save_file.exists():
            self.save(self.default_data)
            return dict(self.default_data)
        with self.save_file.open("r", encoding="utf-8") as f:
            data = json.load(f)
        for k, v in self.default_data.items():
            data.setdefault(k, v)
        return data

    def save(self, data: Dict[str, Any]) -> None:
        self.save_dir.mkdir(parents=True, exist_ok=True)
        with self.save_file.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
