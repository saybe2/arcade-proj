import arcade

from game.config import SCREEN_HEIGHT, SCREEN_TITLE, SCREEN_WIDTH
from game.states.base import BaseView


class MenuView(BaseView):
    def on_draw(self):
        self.clear()
        arcade.draw_text(
            SCREEN_TITLE,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 80,
            arcade.color.WHITE,
            48,
            anchor_x="center",
        )
        arcade.draw_text(
            "Press ENTER to start",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.LIGHT_GRAY,
            20,
            anchor_x="center",
        )
        arcade.draw_text(
            "Press ESC to quit",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 30,
            arcade.color.LIGHT_GRAY,
            16,
            anchor_x="center",
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.state_manager.show_level_select()
        elif key == arcade.key.ESCAPE:
            arcade.close_window()
