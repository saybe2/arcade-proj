import arcade

from game.config import SCREEN_HEIGHT, SCREEN_WIDTH
from game.states.base import BaseView


class LevelSelectView(BaseView):
    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "Select Level",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 80,
            arcade.color.WHITE,
            36,
            anchor_x="center",
        )
        arcade.draw_text(
            "1 - Easy",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 20,
            arcade.color.LIGHT_GRAY,
            20,
            anchor_x="center",
        )
        arcade.draw_text(
            "2 - Medium",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 10,
            arcade.color.LIGHT_GRAY,
            20,
            anchor_x="center",
        )
        arcade.draw_text(
            "3 - Hard",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 40,
            arcade.color.LIGHT_GRAY,
            20,
            anchor_x="center",
        )
        arcade.draw_text(
            "ESC - Back",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 90,
            arcade.color.LIGHT_GRAY,
            16,
            anchor_x="center",
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.KEY_1:
            self.state_manager.start_level(1)
        elif key == arcade.key.KEY_2:
            self.state_manager.start_level(2)
        elif key == arcade.key.KEY_3:
            self.state_manager.start_level(3)
        elif key == arcade.key.ESCAPE:
            self.state_manager.show_menu()
