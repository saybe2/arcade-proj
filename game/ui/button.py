import arcade


class Button:
    """Interactive button with hover and click effects."""

    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        text: str,
        color: tuple[int, int, int] = arcade.color.GRAY,
        hover_color: tuple[int, int, int] = arcade.color.LIGHT_GRAY,
        click_color: tuple[int, int, int] = arcade.color.DARK_GRAY,
        text_color: tuple[int, int, int] = arcade.color.WHITE,
        font_size: int = 18,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.click_color = click_color
        self.text_color = text_color
        self.font_size = font_size

        self.is_hovered = False
        self.is_pressed = False
        self.enabled = True

        self._text_obj = arcade.Text(
            text,
            x,
            y,
            text_color,
            font_size,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )

    def update_text(self, new_text: str):
        """Update button text."""
        self.text = new_text
        self._text_obj.text = new_text

    def check_mouse_hover(self, mouse_x: float, mouse_y: float) -> bool:
        """Check if mouse is hovering over button."""
        if not self.enabled:
            self.is_hovered = False
            return False

        half_width = self.width / 2
        half_height = self.height / 2

        self.is_hovered = (
            self.x - half_width <= mouse_x <= self.x + half_width
            and self.y - half_height <= mouse_y <= self.y + half_height
        )
        return self.is_hovered

    def check_mouse_press(self, mouse_x: float, mouse_y: float) -> bool:
        """Check if button was clicked."""
        if not self.enabled:
            return False

        half_width = self.width / 2
        half_height = self.height / 2

        clicked = (
            self.x - half_width <= mouse_x <= self.x + half_width
            and self.y - half_height <= mouse_y <= self.y + half_height
        )

        if clicked:
            self.is_pressed = True

        return clicked

    def check_mouse_release(self, mouse_x: float, mouse_y: float) -> bool:
        """Check if button was released (completes click action)."""
        if not self.enabled:
            self.is_pressed = False
            return False

        was_pressed = self.is_pressed
        self.is_pressed = False

        if not was_pressed:
            return False

        half_width = self.width / 2
        half_height = self.height / 2

        return (
            self.x - half_width <= mouse_x <= self.x + half_width
            and self.y - half_height <= mouse_y <= self.y + half_height
        )

    def draw(self):
        """Draw the button."""
        if not self.enabled:
            current_color = tuple(c // 2 for c in self.color)
        elif self.is_pressed:
            current_color = self.click_color
        elif self.is_hovered:
            current_color = self.hover_color
        else:
            current_color = self.color

        # Draw button background
        arcade.draw_lrbt_rectangle_filled(
            self.x - self.width / 2,
            self.x + self.width / 2,
            self.y - self.height / 2,
            self.y + self.height / 2,
            current_color,
        )

        # Draw border
        border_color = arcade.color.WHITE if self.is_hovered else arcade.color.DARK_GRAY
        arcade.draw_lrbt_rectangle_outline(
            self.x - self.width / 2,
            self.x + self.width / 2,
            self.y - self.height / 2,
            self.y + self.height / 2,
            border_color,
            2,
        )

        # Draw text
        self._text_obj.draw()
