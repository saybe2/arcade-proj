import arcade

from game.config import SCREEN_HEIGHT, SCREEN_WIDTH
from game.states.base import BaseView


class GameOverView(BaseView):
    def __init__(self, state_manager, won: bool):
        super().__init__(state_manager)
        self.won = won
        title = "Level Complete" if self.won else "Game Over"
        self._title_text = arcade.Text(
            title,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 40,
            arcade.color.WHITE,
            36,
            anchor_x="center",
        )
        self._menu_text = arcade.Text(
            "Press ENTER for menu",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.LIGHT_GRAY,
            18,
            anchor_x="center",
        )

    def on_draw(self):
        self.clear()
        self._title_text.draw()
        self._menu_text.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.state_manager.show_menu()
