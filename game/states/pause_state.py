import arcade

from game.config import SCREEN_HEIGHT, SCREEN_WIDTH
from game.states.base import BaseView


class PauseView(BaseView):
    def __init__(self, state_manager, game_view):
        super().__init__(state_manager)
        self.game_view = game_view

    def on_draw(self):
        self.clear()
        if self.game_view:
            self.game_view.on_draw()

        arcade.draw_lrtb_rectangle_filled(
            0,
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            0,
            (0, 0, 0, 180),
        )
        arcade.draw_text(
            "Paused",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 40,
            arcade.color.WHITE,
            36,
            anchor_x="center",
        )
        arcade.draw_text(
            "Press P to resume",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.LIGHT_GRAY,
            18,
            anchor_x="center",
        )
        arcade.draw_text(
            "ESC - Menu",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 30,
            arcade.color.LIGHT_GRAY,
            16,
            anchor_x="center",
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.P:
            self.state_manager.resume_game()
        elif key == arcade.key.ESCAPE:
            self.state_manager.show_menu()
