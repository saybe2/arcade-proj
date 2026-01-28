import arcade

from game.config import SCREEN_HEIGHT, SCREEN_TITLE, SCREEN_WIDTH
from game.states.base import BaseView
from game.ui.button import Button


class MenuView(BaseView):
    def __init__(self, state_manager):
        super().__init__(state_manager)

        # Buttons - единая цветовая палитра (синие оттенки)
        button_width = 300
        button_height = 60
        center_x = SCREEN_WIDTH / 2
        start_y = SCREEN_HEIGHT / 2 + 50

        self.start_button = Button(
            center_x,
            start_y,
            button_width,
            button_height,
            "START GAME",
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

        self.exit_button = Button(
            center_x,
            start_y - 160,
            button_width,
            button_height,
            "EXIT",
            color=(40, 80, 120),
            hover_color=(60, 120, 180),
            click_color=(20, 40, 80),
        )

        # High score display
        high_scores = state_manager.data.get("high_scores", {})
        total_score = sum(high_scores.values())
        self._highscore_text = arcade.Text(
            f"Total High Score: {total_score}",
            SCREEN_WIDTH / 2,
            80,
            arcade.color.GOLD,
            16,
            anchor_x="center",
        )

        # Background
        self.background_texture = arcade.load_texture(
            "assets/backgrounds/menu_background.jpg"
        )

    def on_draw(self):
        self.clear()

        # Draw background (БЕЗ затемнения!)
        arcade.draw_texture_rect(
            self.background_texture,
            arcade.rect.XYWH(
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT
            ),
        )

        # Draw buttons
        self.start_button.draw()
        self.settings_button.draw()
        self.exit_button.draw()

        # Draw high score
        self._highscore_text.draw()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """Handle mouse movement for hover effects."""
        self.start_button.check_mouse_hover(x, y)
        self.settings_button.check_mouse_hover(x, y)
        self.exit_button.check_mouse_hover(x, y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """Handle mouse press."""
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.start_button.check_mouse_press(x, y):
                self.state_manager.sound.play_sfx("ui")
                self.state_manager.show_level_select()
            elif self.settings_button.check_mouse_press(x, y):
                self.state_manager.sound.play_sfx("ui")
                self.state_manager.show_settings()
            elif self.exit_button.check_mouse_press(x, y):
                self.state_manager.sound.play_sfx("ui")
                arcade.close_window()

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """Handle mouse release."""
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.start_button.check_mouse_release(x, y)
            self.settings_button.check_mouse_release(x, y)
            self.exit_button.check_mouse_release(x, y)

    def on_key_press(self, key, modifiers):
        """Keep keyboard shortcuts."""
        if key == arcade.key.ENTER:
            self.state_manager.show_level_select()
        elif key == arcade.key.O:
            self.state_manager.show_settings()
        elif key == arcade.key.ESCAPE:
            arcade.close_window()
