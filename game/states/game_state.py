import arcade

from game.config import SCREEN_HEIGHT, SCREEN_WIDTH
from game.entities.player import Player
from game.states.base import BaseView
from game.systems.camera import CameraManager
from game.ui.hud import HUD


class GameView(BaseView):
    def __init__(self, state_manager, level_id: int):
        super().__init__(state_manager)
        self.level_id = level_id

        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.hazard_list = arcade.SpriteList()
        self.ui_button_list = arcade.SpriteList()

        self.player = None
        self.physics_engine = None
        self.camera = CameraManager(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            window=state_manager.window,
        )
        self.hud = HUD()

        self.score = 0
        self.time_elapsed = 0.0

    def setup(self):
        self.player_list.clear()
        self.enemy_list.clear()
        self.platform_list.clear()
        self.coin_list.clear()
        self.hazard_list.clear()
        self.ui_button_list.clear()

        self.player = Player()
        self.player_list.append(self.player)

    def on_show_view(self):
        super().on_show_view()
        self.setup()

    def on_draw(self):
        self.clear()
        self.camera.use_world()
        self.platform_list.draw()
        self.coin_list.draw()
        self.hazard_list.draw()
        self.enemy_list.draw()
        self.player_list.draw()

        self.camera.use_hud()
        self.hud.score = self.score
        self.hud.time_elapsed = self.time_elapsed
        self.hud.draw()

    def on_update(self, delta_time: float):
        self.time_elapsed += delta_time
        self.player_list.update()
        self.enemy_list.update()
        if self.physics_engine:
            self.physics_engine.update()
        self.camera.update(self.player)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.P:
            self.state_manager.show_pause()
