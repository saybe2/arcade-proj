import arcade

from game.config import SCREEN_HEIGHT, SCREEN_WIDTH
from game.states.base import BaseView


class PauseView(BaseView):
    def __init__(self, state_manager, game_view):
        super().__init__(state_manager)
        self.game_view = game_view
        self._title_text = arcade.Text(
            "Paused",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 40,
            arcade.color.WHITE,
            36,
            anchor_x="center",
        )
        self._resume_text = arcade.Text(
            "Press P to resume",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.LIGHT_GRAY,
            18,
            anchor_x="center",
        )
        self._menu_text = arcade.Text(
            "ESC - Menu",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 30,
            arcade.color.LIGHT_GRAY,
            16,
            anchor_x="center",
        )

    def on_draw(self):
        self.clear()
        if self.game_view:
            self.game_view.on_draw()

        arcade.draw_lrbt_rectangle_filled(
            0,
            SCREEN_HEIGHT,
            0,
            SCREEN_WIDTH,
            (0, 0, 0, 180),
        )
        self._title_text.draw()
        self._resume_text.draw()
        self._menu_text.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.P:
            self.state_manager.resume_game()
        elif key == arcade.key.ESCAPE:
            self.state_manager.show_menu()
