import arcade

from game.config import SCREEN_HEIGHT, SCREEN_WIDTH
from game.states.base import BaseView
from game.ui.button import Button


class LevelSelectView(BaseView):
    def __init__(self, state_manager):
        super().__init__(state_manager)

        # Title
        self._title_text = arcade.Text(
            "SELECT LEVEL",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 100,
            arcade.color.WHITE,
            42,
            anchor_x="center",
            bold=True,
        )

        # Get high scores
        high_scores = state_manager.data.get("high_scores", {})
        level_one_score = high_scores.get("level_1", 0)
        level_two_score = high_scores.get("level_2", 0)
        level_three_score = high_scores.get("level_3", 0)

        # Level buttons - единая цветовая палитра
        button_width = 400
        button_height = 70
        center_x = SCREEN_WIDTH / 2
        start_y = SCREEN_HEIGHT / 2 + 80

        self.level1_button = Button(
            center_x,
            start_y,
            button_width,
            button_height,
            f"LEVEL 1 - EASY\nBest: {level_one_score}",
            color=(40, 80, 120),
            hover_color=(60, 120, 180),
            click_color=(20, 40, 80),
            font_size=20,
        )

        self.level2_button = Button(
            center_x,
            start_y - 100,
            button_width,
            button_height,
            f"LEVEL 2 - MEDIUM\nBest: {level_two_score}",
            color=(40, 80, 120),
            hover_color=(60, 120, 180),
            click_color=(20, 40, 80),
            font_size=20,
        )

        self.level3_button = Button(
            center_x,
            start_y - 200,
            button_width,
            button_height,
            f"LEVEL 3 - HARD\nBest: {level_three_score}",
            color=(40, 80, 120),
            hover_color=(60, 120, 180),
            click_color=(20, 40, 80),
            font_size=20,
        )

        self.back_button = Button(
            center_x,
            100,
            250,
            50,
            "BACK",
            color=(40, 80, 120),
            hover_color=(60, 120, 180),
            click_color=(20, 40, 80),
        )

    def on_draw(self):
        self.clear()

        # Draw title
        self._title_text.draw()

        # Draw buttons
        self.level1_button.draw()
        self.level2_button.draw()
        self.level3_button.draw()
        self.back_button.draw()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """Handle mouse movement for hover effects."""
        self.level1_button.check_mouse_hover(x, y)
        self.level2_button.check_mouse_hover(x, y)
        self.level3_button.check_mouse_hover(x, y)
        self.back_button.check_mouse_hover(x, y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """Handle mouse press."""
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.level1_button.check_mouse_press(x, y):
                self.state_manager.sound.play_sfx("ui")
                self.state_manager.start_level(1)
            elif self.level2_button.check_mouse_press(x, y):
                self.state_manager.sound.play_sfx("ui")
                self.state_manager.start_level(2)
            elif self.level3_button.check_mouse_press(x, y):
                self.state_manager.sound.play_sfx("ui")
                self.state_manager.start_level(3)
            elif self.back_button.check_mouse_press(x, y):
                self.state_manager.sound.play_sfx("ui")
                self.state_manager.show_menu()

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """Handle mouse release."""
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.level1_button.check_mouse_release(x, y)
            self.level2_button.check_mouse_release(x, y)
            self.level3_button.check_mouse_release(x, y)
            self.back_button.check_mouse_release(x, y)

    def on_key_press(self, key, modifiers):
        """Keep keyboard shortcuts."""
        if key == arcade.key.KEY_1:
            self.state_manager.start_level(1)
        elif key == arcade.key.KEY_2:
            self.state_manager.start_level(2)
        elif key == arcade.key.KEY_3:
            self.state_manager.start_level(3)
        elif key == arcade.key.ESCAPE:
            self.state_manager.show_menu()
