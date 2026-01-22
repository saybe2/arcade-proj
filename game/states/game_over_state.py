import arcade

from game.config import SCREEN_HEIGHT, SCREEN_WIDTH
from game.states.base import BaseView


class GameOverView(BaseView):
    def __init__(self, state_manager, won: bool):
        super().__init__(state_manager)
        self.won = won

    def on_draw(self):
        self.clear()
        title = "Level Complete" if self.won else "Game Over"
        arcade.draw_text(
            title,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 40,
            arcade.color.WHITE,
            36,
            anchor_x="center",
        )
        arcade.draw_text(
            "Press ENTER for menu",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.LIGHT_GRAY,
            18,
            anchor_x="center",
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.state_manager.show_menu()
