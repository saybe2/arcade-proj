import arcade

from game.config import SCREEN_HEIGHT, SCREEN_WIDTH


class HUD:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.time_elapsed = 0.0
        self._score_text = arcade.Text(
            "Score: 0",
            20,
            SCREEN_HEIGHT - 30,
            arcade.color.WHITE,
            14,
        )
        self._lives_text = arcade.Text(
            "Lives: 3",
            20,
            SCREEN_HEIGHT - 50,
            arcade.color.WHITE,
            14,
        )
        self._time_text = arcade.Text(
            "Time: 0",
            SCREEN_WIDTH - 140,
            SCREEN_HEIGHT - 30,
            arcade.color.WHITE,
            14,
        )

    def draw(self):
        self._score_text.text = f"Score: {self.score}"
        self._lives_text.text = f"Lives: {self.lives}"
        self._time_text.text = f"Time: {int(self.time_elapsed)}"
        self._score_text.draw()
        self._lives_text.draw()
        self._time_text.draw()
