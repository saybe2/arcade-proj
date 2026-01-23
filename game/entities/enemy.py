import math
import random

import arcade


class Enemy(arcade.Sprite):
    def __init__(self, color=arcade.color.RED):
        super().__init__()
        self.texture = arcade.make_soft_square_texture(28, color, 255, 0)
        self.damage = 1

    def update_ai(self, delta_time: float):
        pass

    def update(self, delta_time: float = 1 / 60):
        self.update_ai(delta_time)
        super().update()


class PatrolEnemy(Enemy):
    def __init__(self, left_bound: float, right_bound: float, speed: float = 2.0):
        super().__init__(arcade.color.ORANGE_RED)
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.change_x = speed

    def update_ai(self, delta_time: float):
        if self.center_x <= self.left_bound or self.center_x >= self.right_bound:
            self.change_x *= -1


class JumpingEnemy(Enemy):
    def __init__(
        self,
        jump_interval_min: float = 1.0,
        jump_interval_max: float = 2.0,
        jump_strength: float = 12.0,
    ):
        super().__init__(arcade.color.PURPLE)
        self.jump_interval_min = jump_interval_min
        self.jump_interval_max = jump_interval_max
        self.jump_strength = jump_strength
        self.time_to_jump = random.uniform(jump_interval_min, jump_interval_max)

    def update_ai(self, delta_time: float):
        self.time_to_jump -= delta_time
        if self.time_to_jump <= 0:
            self.change_y = self.jump_strength
            self.time_to_jump = random.uniform(self.jump_interval_min, self.jump_interval_max)


class FlyingEnemy(Enemy):
    def __init__(self, amplitude: float = 40.0, speed: float = 2.5):
        super().__init__(arcade.color.AIR_FORCE_BLUE)
        self.amplitude = amplitude
        self.speed = speed
        self.base_y = 0
        self.phase = 0.0

    def update_ai(self, delta_time: float):
        self.phase += delta_time * 2
        self.change_x = self.speed
        self.center_y = self.base_y + math.sin(self.phase) * self.amplitude
