import arcade

from game.config import SCREEN_HEIGHT, SCREEN_WIDTH
from game.states.base import BaseView


class LevelSelectView(BaseView):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self._title_text = arcade.Text(
            "Select Level",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 80,
            arcade.color.WHITE,
            36,
            anchor_x="center",
        )
        self._header_text = arcade.Text(
            "High Scores",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 50,
            arcade.color.LIGHT_GRAY,
            16,
            anchor_x="center",
        )
        high_scores = state_manager.data.get("high_scores", {})
        level_one_score = high_scores.get("level_1", 0)
        level_two_score = high_scores.get("level_2", 0)
        level_three_score = high_scores.get("level_3", 0)
        self._level_one_text = arcade.Text(
            f"1 - Easy  (Best: {level_one_score})",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 20,
            arcade.color.LIGHT_GRAY,
            20,
            anchor_x="center",
        )
        self._level_two_text = arcade.Text(
            f"2 - Medium  (Best: {level_two_score})",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 10,
            arcade.color.LIGHT_GRAY,
            20,
            anchor_x="center",
        )
        self._level_three_text = arcade.Text(
            f"3 - Hard  (Best: {level_three_score})",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 40,
            arcade.color.LIGHT_GRAY,
            20,
            anchor_x="center",
        )
        self._back_text = arcade.Text(
            "ESC - Back",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 90,
            arcade.color.LIGHT_GRAY,
            16,
            anchor_x="center",
        )

    def on_draw(self):
        self.clear()
        self._title_text.draw()
        self._header_text.draw()
        self._level_one_text.draw()
        self._level_two_text.draw()
        self._level_three_text.draw()
        self._back_text.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.KEY_1:
            self.state_manager.start_level(1)
        elif key == arcade.key.KEY_2:
            self.state_manager.start_level(2)
        elif key == arcade.key.KEY_3:
            self.state_manager.start_level(3)
        elif key == arcade.key.ESCAPE:
            self.state_manager.show_menu()
