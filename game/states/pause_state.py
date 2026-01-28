import arcade

from game.config import SCREEN_HEIGHT, SCREEN_WIDTH
from game.states.base import BaseView
from game.ui.button import Button


class PauseView(BaseView):
    def __init__(self, state_manager, game_view):
        super().__init__(state_manager)
        self.game_view = game_view

        # Title
        self._title_text = arcade.Text(
            "PAUSED",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 120,
            arcade.color.WHITE,
            48,
            anchor_x="center",
            bold=True,
        )

        # Buttons - единая цветовая палитра
        button_width = 300
        button_height = 60
        center_x = SCREEN_WIDTH / 2
        start_y = SCREEN_HEIGHT / 2 + 20

        self.resume_button = Button(
            center_x,
            start_y,
            button_width,
            button_height,
            "RESUME",
            color=(40, 80, 120),
            hover_color=(60, 120, 180),
            click_color=(20, 40, 80),
        )

        self.settings_button = Button(
            center_x,
            start_y - 80,
            button_width,
            button_height,
            "SETTINGS",
            color=(40, 80, 120),
            hover_color=(60, 120, 180),
            click_color=(20, 40, 80),
        )

        self.quit_button = Button(
            center_x,
            start_y - 160,
            button_width,
            button_height,
            "QUIT TO MENU",
            color=(40, 80, 120),
            hover_color=(60, 120, 180),
            click_color=(20, 40, 80),
        )

    def on_draw(self):
        self.clear()

        # Draw game in background
        if self.game_view:
            self.game_view.on_draw()

        # Draw semi-transparent overlay
        arcade.draw_lrbt_rectangle_filled(
            0,
            SCREEN_WIDTH,
            0,
            SCREEN_HEIGHT,
            (0, 0, 0, 180),
        )

        # Draw title
        self._title_text.draw()

        # Draw buttons
        self.resume_button.draw()
        self.settings_button.draw()
        self.quit_button.draw()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """Handle mouse movement for hover effects."""
        self.resume_button.check_mouse_hover(x, y)
        self.settings_button.check_mouse_hover(x, y)
        self.quit_button.check_mouse_hover(x, y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """Handle mouse press."""
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.resume_button.check_mouse_press(x, y):
                self.state_manager.sound.play_sfx("ui")
                self.state_manager.resume_game()
            elif self.settings_button.check_mouse_press(x, y):
                self.state_manager.sound.play_sfx("ui")
                self.state_manager.show_settings()
            elif self.quit_button.check_mouse_press(x, y):
                self.state_manager.sound.play_sfx("ui")
                self.state_manager.show_menu()

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """Handle mouse release."""
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.resume_button.check_mouse_release(x, y)
            self.settings_button.check_mouse_release(x, y)
            self.quit_button.check_mouse_release(x, y)

    def on_key_press(self, key, modifiers):
        """Keep keyboard shortcuts."""
        if key == arcade.key.P:
            self.state_manager.resume_game()
        elif key == arcade.key.ESCAPE:
            self.state_manager.show_menu()
