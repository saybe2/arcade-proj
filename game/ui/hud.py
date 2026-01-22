import arcade

from game.config import SCREEN_HEIGHT, SCREEN_WIDTH


class HUD:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.time_elapsed = 0.0

    def draw(self):
        arcade.draw_text(
            f"Score: {self.score}",
            20,
            SCREEN_HEIGHT - 30,
            arcade.color.WHITE,
            14,
        )
        arcade.draw_text(
            f"Lives: {self.lives}",
            20,
            SCREEN_HEIGHT - 50,
            arcade.color.WHITE,
            14,
        )
        arcade.draw_text(
            f"Time: {int(self.time_elapsed)}",
            SCREEN_WIDTH - 140,
            SCREEN_HEIGHT - 30,
            arcade.color.WHITE,
            14,
        )
