import arcade

from game.config import SCREEN_HEIGHT, SCREEN_TITLE, SCREEN_WIDTH
from game.states.base import BaseView


class MenuView(BaseView):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self._start_text = arcade.Text(
            "Press ENTER to start",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.LIGHT_GRAY,
            20,
            anchor_x="center",
        )
        self._exit_text = arcade.Text(
            "Press ESC to quit",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 30,
            arcade.color.LIGHT_GRAY,
            16,
            anchor_x="center",
        )
        self.background_texture = arcade.load_texture(
            "assets/backgrounds/menu_background.jpeg"
        )

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.background_texture,
            arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self._start_text.draw()
        self._exit_text.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.state_manager.show_level_select()
        elif key == arcade.key.ESCAPE:
            arcade.close_window()
