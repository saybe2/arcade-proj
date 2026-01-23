import arcade

from game.config import (
    GRAVITY,
    PLAYER_JUMP_SPEED,
    PLAYER_MOVE_SPEED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from game.entities.coin import Coin
from game.entities.hazard import Hazard
from game.entities.platform import Platform
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
        self.level_end_x = 0
        self._move_left = False
        self._move_right = False
        self._jump_requested = False

    def setup(self):
        self.player_list.clear()
        self.enemy_list.clear()
        self.platform_list.clear()
        self.coin_list.clear()
        self.hazard_list.clear()
        self.ui_button_list.clear()

        self.player = Player()
        self.player_list.append(self.player)

        self.score = 0
        self.time_elapsed = 0.0
        self.level_end_x = 0
        self._move_left = False
        self._move_right = False
        self._jump_requested = False

        if self.level_id == 1:
            self._setup_level_one()
        else:
            self.physics_engine = None

    def _setup_level_one(self):
        self.player.center_x = 100
        self.player.center_y = 150

        ground = Platform(2400, 40)
        ground.center_x = 1200
        ground.center_y = 20
        self.platform_list.append(ground)

        platform_positions = [
            (300, 140),
            (520, 220),
            (760, 300),
            (980, 220),
            (1200, 160),
            (1450, 260),
            (1700, 200),
        ]

        for x, y in platform_positions:
            platform = Platform(120, 24)
            platform.center_x = x
            platform.center_y = y
            self.platform_list.append(platform)

        for x, y in [(300, 180), (520, 260), (760, 340), (980, 260), (1450, 300)]:
            coin = Coin()
            coin.center_x = x
            coin.center_y = y
            self.coin_list.append(coin)

        for x, y in [(620, 60), (1320, 60), (1900, 60)]:
            spikes = Hazard(width=32, height=32, damage=10, color=arcade.color.RED)
            spikes.center_x = x
            spikes.center_y = y
            self.hazard_list.append(spikes)

        self.level_end_x = 2100
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, self.platform_list, gravity_constant=GRAVITY
        )

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
        self.enemy_list.update()
        if self.physics_engine:
            direction = (-1 if self._move_left else 0) + (1 if self._move_right else 0)
            self.player.change_x = direction * PLAYER_MOVE_SPEED * delta_time
            if self._jump_requested and self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP_SPEED * delta_time
                self._jump_requested = False
            if hasattr(self.physics_engine, "gravity_constant"):
                self.physics_engine.gravity_constant = GRAVITY * delta_time
            self.physics_engine.update()
        else:
            self.player_list.update()

        coins_hit = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in coins_hit:
            coin.remove_from_sprite_lists()
            self.score += getattr(coin, "value", 0)

        if arcade.check_for_collision_with_list(self.player, self.hazard_list):
            self.state_manager.set_last_score(self.score)
            self.state_manager.show_game_over(False)
            return

        if self.level_end_x and self.player.center_x >= self.level_end_x:
            self.state_manager.set_last_score(self.score)
            self.state_manager.show_game_over(True)
            return

        if self.player.center_y < -200:
            self.state_manager.set_last_score(self.score)
            self.state_manager.show_game_over(False)
            return

        self.camera.update(self.player)

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self._move_left = True
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self._move_right = True
        elif key == arcade.key.SPACE:
            self._jump_requested = True
        elif key == arcade.key.P:
            self.state_manager.show_pause()
        elif key == arcade.key.ESCAPE:
            self.state_manager.show_menu()

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self._move_left = False
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self._move_right = False
