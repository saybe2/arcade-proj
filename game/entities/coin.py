import arcade


class Coin(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.make_soft_circle_texture(18, arcade.color.GOLD, 255, 0)
        self.value = 10
