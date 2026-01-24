from __future__ import annotations

from datetime import datetime
from typing import Optional

from game.config import MUSIC_LEVEL, MUSIC_MENU, SFX_COIN, SFX_DEATH, SFX_JUMP, SFX_UI
from game.systems.audio import SoundManager
from game.systems.data import DataManager


class StateManager:
    def __init__(self, window):
        self.window = window
        self.current_level = 1
        self.last_score = 0
        self._game_view = None
        self.data_manager = DataManager()
        self.data = self.data_manager.load()
        self.sound = SoundManager()
        self.sound.load_sfx("coin", SFX_COIN)
        self.sound.load_sfx("jump", SFX_JUMP)
        self.sound.load_sfx("death", SFX_DEATH)
        self.sound.load_sfx("ui", SFX_UI)
        self.sound.play_music(MUSIC_MENU)

    def show_menu(self):
        from game.states.menu_state import MenuView

        self.sound.play_music(MUSIC_MENU)
        self.window.show_view(MenuView(self))

    def show_level_select(self):
        from game.states.level_select_state import LevelSelectView

        self.sound.play_sfx("ui")
        self.window.show_view(LevelSelectView(self))

    def start_level(self, level_id: int):
        from game.states.game_state import GameView

        self.current_level = level_id
        self._game_view = GameView(self, level_id)
        self.sound.play_sfx("ui")
        self.sound.play_music(MUSIC_LEVEL)
        self.window.show_view(self._game_view)

    def show_pause(self):
        from game.states.pause_state import PauseView

        if self._game_view is None:
            return
        self.sound.play_sfx("ui")
        self.window.show_view(PauseView(self, self._game_view))

    def resume_game(self):
        if self._game_view is None:
            return
        self.sound.play_sfx("ui")
        self.window.show_view(self._game_view)

    def show_game_over(self, won: bool):
        from game.states.game_over_state import GameOverView

        self.sound.play_sfx("ui")
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
