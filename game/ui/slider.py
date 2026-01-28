import arcade


class Slider:
    """Interactive slider for adjusting values."""

    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        min_value: float = 0.0,
        max_value: float = 1.0,
        initial_value: float = 0.5,
        label: str = "",
        bar_color: tuple[int, int, int] = arcade.color.GRAY,
        handle_color: tuple[int, int, int] = arcade.color.WHITE,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.label = label
        self.bar_color = bar_color
        self.handle_color = handle_color

        self.is_dragging = False
        self.handle_width = 12
        self.handle_height = height + 10

        self._label_text = arcade.Text(
            label,
            x - width / 2 - 10,
            y,
            arcade.color.WHITE,
            14,
            anchor_x="right",
            anchor_y="center",
        )

        self._value_text = arcade.Text(
            self._format_value(),
            x + width / 2 + 10,
            y,
            arcade.color.WHITE,
            14,
            anchor_x="left",
            anchor_y="center",
        )

    def _format_value(self) -> str:
        """Format value as percentage."""
        percentage = int(
            ((self.value - self.min_value) / (self.max_value - self.min_value)) * 100
        )
        return f"{percentage}%"

    def _get_handle_x(self) -> float:
        """Calculate handle X position based on current value."""
        normalized = (self.value - self.min_value) / (self.max_value - self.min_value)
        return self.x - self.width / 2 + normalized * self.width

    def _value_from_x(self, mouse_x: float) -> float:
        """Calculate value from mouse X position."""
        left = self.x - self.width / 2
        right = self.x + self.width / 2
        clamped_x = max(left, min(right, mouse_x))
        normalized = (clamped_x - left) / self.width
        return self.min_value + normalized * (self.max_value - self.min_value)

    def check_mouse_press(self, mouse_x: float, mouse_y: float) -> bool:
        """Check if slider handle was pressed."""
        handle_x = self._get_handle_x()
        half_handle_width = self.handle_width / 2
        half_handle_height = self.handle_height / 2

        if (
            handle_x - half_handle_width <= mouse_x <= handle_x + half_handle_width
            and self.y - half_handle_height <= mouse_y <= self.y + half_handle_height
        ):
            self.is_dragging = True
            return True

        # Also check if clicked on bar
        if (
            self.x - self.width / 2 <= mouse_x <= self.x + self.width / 2
            and self.y - self.height / 2 <= mouse_y <= self.y + self.height / 2
        ):
            self.value = self._value_from_x(mouse_x)
            self._value_text.text = self._format_value()
            self.is_dragging = True
            return True

        return False

    def check_mouse_release(self, mouse_x: float, mouse_y: float):
        """Handle mouse release."""
        self.is_dragging = False

    def check_mouse_drag(self, mouse_x: float, mouse_y: float):
        """Handle mouse drag."""
        if self.is_dragging:
            self.value = self._value_from_x(mouse_x)
            self._value_text.text = self._format_value()

    def draw(self):
        """Draw the slider."""
        # Draw bar background
        arcade.draw_lrbt_rectangle_filled(
            self.x - self.width / 2,
            self.x + self.width / 2,
            self.y - self.height / 2,
            self.y + self.height / 2,
            self.bar_color,
        )

        # Draw filled portion
        handle_x = self._get_handle_x()
        filled_width = handle_x - (self.x - self.width / 2)
        if filled_width > 0:
            arcade.draw_lrbt_rectangle_filled(
                self.x - self.width / 2,
                self.x - self.width / 2 + filled_width,
                self.y - self.height / 2,
                self.y + self.height / 2,
                arcade.color.GREEN,
            )

        # Draw bar outline
        arcade.draw_lrbt_rectangle_outline(
            self.x - self.width / 2,
            self.x + self.width / 2,
            self.y - self.height / 2,
            self.y + self.height / 2,
            arcade.color.WHITE,
            2,
        )

        # Draw handle
        arcade.draw_lrbt_rectangle_filled(
            handle_x - self.handle_width / 2,
            handle_x + self.handle_width / 2,
            self.y - self.handle_height / 2,
            self.y + self.handle_height / 2,
            self.handle_color,
        )
        arcade.draw_lrbt_rectangle_outline(
            handle_x - self.handle_width / 2,
            handle_x + self.handle_width / 2,
            self.y - self.handle_height / 2,
            self.y + self.handle_height / 2,
            arcade.color.BLACK,
            2,
        )

        # Draw label and value
        self._label_text.draw()
        self._value_text.draw()
