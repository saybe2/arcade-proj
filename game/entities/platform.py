import arcade


class Platform(arcade.Sprite):
    def __init__(self, width: int = 128, height: int = 24):
        super().__init__()
        self.texture = arcade.make_soft_square_texture(width, arcade.color.GRAY, 255, 0)
