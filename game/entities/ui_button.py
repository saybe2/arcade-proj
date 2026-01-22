import arcade


class UIButton(arcade.Sprite):
    def __init__(self, label: str, color=arcade.color.GREEN):
        super().__init__()
        self.texture = arcade.make_soft_square_texture(160, color, 255, 0)
        self.label = label
        self._label_text = None

    def draw_label(self):
        if self._label_text is None:
            self._label_text = arcade.Text(
                self.label,
                self.center_x,
                self.center_y,
                arcade.color.BLACK,
                14,
                anchor_x="center",
                anchor_y="center",
            )
        else:
            self._label_text.text = self.label
            self._label_text.x = self.center_x
            self._label_text.y = self.center_y
        self._label_text.draw()
