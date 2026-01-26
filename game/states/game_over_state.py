import arcade

from game.config import SCREEN_HEIGHT, SCREEN_WIDTH
from game.levels import get_level_specs
from game.states.base import BaseView


class GameOverView(BaseView):
    def __init__(self, state_manager, won: bool):
        super().__init__(state_manager)
        self.won = won
        self.current_level = state_manager.current_level
        self.max_level = max(get_level_specs().keys())
        title = "Level Complete" if self.won else "Game Over"
        self._title_text = arcade.Text(
            title,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 40,
            arcade.color.WHITE,
            36,
            anchor_x="center",
        )
        self._score_text = arcade.Text(
            f"Score: {state_manager.last_score}",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 5,
            arcade.color.LIGHT_GRAY,
            18,
            anchor_x="center",
        )
        lines = []
        if self.won and self.current_level < self.max_level:
            lines.append("N - Next Level")
        lines.append("R - Retry")
        lines.append("M / ESC - Menu")
        self._action_text = arcade.Text(
            "   ".join(lines),
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 30,
            arcade.color.LIGHT_GRAY,
            16,
            anchor_x="center",
        )

    def on_draw(self):
        self.clear()
        self._title_text.draw()
        self._score_text.draw()
        self._action_text.draw()

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.M, arcade.key.ESCAPE, arcade.key.ENTER):
            self.state_manager.show_menu()
        elif key == arcade.key.R:
            self.state_manager.start_level(self.current_level)
        elif (
            key == arcade.key.N
            and self.won
            and self.current_level < self.max_level
        ):
            self.state_manager.start_level(self.current_level + 1)
