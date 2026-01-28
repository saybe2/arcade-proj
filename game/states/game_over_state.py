import arcade

from game.config import SCREEN_HEIGHT, SCREEN_WIDTH
from game.levels import get_level_specs
from game.states.base import BaseView
from game.ui.button import Button


class GameOverView(BaseView):
    def __init__(self, state_manager, won: bool):
        super().__init__(state_manager)
        self.won = won
        self.current_level = state_manager.current_level
        self.max_level = max(get_level_specs().keys())

        # Title
        title = "LEVEL COMPLETE!" if self.won else "GAME OVER"
        title_color = arcade.color.GREEN if self.won else arcade.color.RED
        self._title_text = arcade.Text(
            title,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 120,
            title_color,
            48,
            anchor_x="center",
            bold=True,
        )

        # Score
        self._score_text = arcade.Text(
            f"Score: {state_manager.last_score}",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 80,
            arcade.color.GOLD,
            32,
            anchor_x="center",
            bold=True,
        )

        # Buttons - единая цветовая палитра
        button_width = 280
        button_height = 60
        center_x = SCREEN_WIDTH / 2
        start_y = SCREEN_HEIGHT / 2

        self.buttons = []

        # Next level button (only if won and not last level)
        if self.won and self.current_level < self.max_level:
            self.next_button = Button(
                center_x,
                start_y,
                button_width,
                button_height,
                "NEXT LEVEL",
                color=(40, 80, 120),
                hover_color=(60, 120, 180),
                click_color=(20, 40, 80),
            )
            self.buttons.append(self.next_button)
            start_y -= 80
        else:
            self.next_button = None

        # Retry button
        self.retry_button = Button(
            center_x,
            start_y,
            button_width,
            button_height,
            "RETRY",
            color=(40, 80, 120),
            hover_color=(60, 120, 180),
            click_color=(20, 40, 80),
        )
        self.buttons.append(self.retry_button)

        # Menu button
        self.menu_button = Button(
            center_x,
            start_y - 80,
            button_width,
            button_height,
            "MENU",
            color=(40, 80, 120),
            hover_color=(60, 120, 180),
            click_color=(20, 40, 80),
        )
        self.buttons.append(self.menu_button)

    def on_draw(self):
        self.clear()

        # Draw title
        self._title_text.draw()

        # Draw score
        self._score_text.draw()

        # Draw buttons
        for button in self.buttons:
            button.draw()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """Handle mouse movement for hover effects."""
        for button in self.buttons:
            button.check_mouse_hover(x, y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """Handle mouse press."""
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.next_button and self.next_button.check_mouse_press(x, y):
                self.state_manager.sound.play_sfx("ui")
                self.state_manager.start_level(self.current_level + 1)
            elif self.retry_button.check_mouse_press(x, y):
                self.state_manager.sound.play_sfx("ui")
                self.state_manager.start_level(self.current_level)
            elif self.menu_button.check_mouse_press(x, y):
                self.state_manager.sound.play_sfx("ui")
                self.state_manager.show_menu()

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """Handle mouse release."""
        if button == arcade.MOUSE_BUTTON_LEFT:
            for btn in self.buttons:
                btn.check_mouse_release(x, y)

    def on_key_press(self, key, modifiers):
        """Keep keyboard shortcuts."""
        if key in (arcade.key.M, arcade.key.ESCAPE, arcade.key.ENTER):
            self.state_manager.show_menu()
        elif key == arcade.key.R:
            self.state_manager.start_level(self.current_level)
        elif (
            key == arcade.key.N
            and self.won
            and self.current_level < self.max_level
        ):
            self.state_manager.start_level(self.current_level + 1)
