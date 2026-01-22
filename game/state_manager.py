from __future__ import annotations

from typing import Optional


class StateManager:
    def __init__(self, window):
        self.window = window
        self.current_level = 1
        self.last_score = 0
        self._game_view = None

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

    def get_game_view(self) -> Optional[object]:
        return self._game_view
