import arcade


class Platform(arcade.SpriteSolidColor):
    def __init__(self, width: int = 128, height: int = 24, color=arcade.color.GRAY):
        super().__init__(width, height, color)
