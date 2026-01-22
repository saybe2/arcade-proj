import arcade


class UIButton(arcade.Sprite):
    def __init__(self, label: str, color=arcade.color.GREEN):
        super().__init__()
        self.texture = arcade.make_soft_square_texture(160, color, 255, 0)
        self.label = label

    def draw_label(self):
        arcade.draw_text(
            self.label,
            self.center_x,
            self.center_y,
            arcade.color.BLACK,
            14,
            anchor_x="center",
            anchor_y="center",
        )
