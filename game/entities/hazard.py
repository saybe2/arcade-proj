import arcade


class Hazard(arcade.SpriteSolidColor):
    def __init__(
        self,
        width: int = 24,
        height: int = 24,
        damage: int = 1,
        color=arcade.color.DARK_RED,
    ):
        super().__init__(width, height, color)
        self.damage = damage
