import arcade


class Hazard(arcade.Sprite):
    def __init__(self, damage: int = 1, color=arcade.color.DARK_RED):
        super().__init__()
        self.texture = arcade.make_soft_square_texture(24, color, 255, 0)
        self.damage = damage
