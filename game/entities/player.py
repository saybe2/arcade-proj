import arcade


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.make_soft_square_texture(32, arcade.color.BLUE, 255, 0)
        self.center_x = 100
        self.center_y = 150
        self.is_alive = True

    def update_animation(self, delta_time: float = 1 / 60):
        pass
