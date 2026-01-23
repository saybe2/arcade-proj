from __future__ import annotations

from datetime import datetime
from typing import Optional

from game.systems.data import DataManager


class StateManager:
    def __init__(self, window):
        self.window = window
        self.current_level = 1
        self.last_score = 0
        self._game_view = None
        self.data_manager = DataManager()
        self.data = self.data_manager.load()

    def show_menu(self):
        from game.states.menu_state import MenuView

        self.window.show_view(MenuView(self))

    def show_level_select(self):
        from game.states.level_select_state import LevelSelectView

        self.window.show_view(LevelSelectView(self))

    def start_level(self, level_id: int):
        from game.states.game_state import GameView

        self.current_level = level_id
        self._game_view = GameView(self, level_id)
        self.window.show_view(self._game_view)

    def show_pause(self):
        from game.states.pause_state import PauseView

        if self._game_view is None:
            return
        self.window.show_view(PauseView(self, self._game_view))

    def resume_game(self):
        if self._game_view is None:
            return
        self.window.show_view(self._game_view)

    def show_game_over(self, won: bool):
        from game.states.game_over_state import GameOverView

        self.window.show_view(GameOverView(self, won))

    def set_last_score(self, score: int):
        self.last_score = score

    def update_progress(self, level_id: int, score: int, won: bool, time_elapsed: float):
        level_key = f"level_{level_id}"
        high_scores = self.data.setdefault("high_scores", {})
        current_best = high_scores.get(level_key, 0)
        if score > current_best:
            high_scores[level_key] = score

        if won:
            levels_completed = self.data.setdefault("levels_completed", [])
            if level_id not in levels_completed:
                levels_completed.append(level_id)

        total_playtime = self.data.get("total_playtime", 0)
        self.data["total_playtime"] = total_playtime + int(time_elapsed)
        self.data["last_played"] = datetime.now().isoformat(timespec="seconds")
        self.data_manager.save()

    def get_game_view(self) -> Optional[object]:
        return self._game_view
