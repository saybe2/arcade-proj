import json
from pathlib import Path

from game.config import DATA_FILE_PATH


class DataManager:
    def __init__(self, path: str = DATA_FILE_PATH):
        self.path = Path(path)
        self.data = self.default_data()

    @staticmethod
    def default_data():
        return {
            "player_name": "Player1",
            "levels_completed": [],
            "high_scores": {},
            "total_playtime": 0,
            "last_played": None,
        }

    def load(self):
        if self.path.exists():
            try:
                self.data = json.loads(self.path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                self.data = self.default_data()
        return self.data

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, indent=2), encoding="utf-8")
