import arcade

from game.config import (
    GRAVITY,
    PLAYER_JUMP_SPEED,
    PLAYER_JUMP_HOLD_FORCE,
    PLAYER_JUMP_HOLD_FRAMES,
    PLAYER_MOVE_SPEED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from game.entities.coin import Coin
from game.entities.hazard import Hazard
from game.entities.platform import Platform
from game.entities.enemy import JumpingEnemy, PatrolEnemy
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
        self.enemy_physics_engines = []
        self.camera = CameraManager(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            window=state_manager.window,
        )
        self.hud = HUD()

        self.score = 0
        self.time_elapsed = 0.0
        self.level_end_x = 0
        self.lives = 3
        self.spawn_point = (100, 150)
        
        # Используем set для отслеживания нажатых клавиш
        self.keys_pressed = set()
        self._jump_pressed = False
        self._jump_held = False
        self._jump_active = False
        self._jump_frames = 0

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
        self.lives = 3
        self.spawn_point = (100, 150)
        self.keys_pressed = set()
        self._jump_pressed = False
        self._jump_held = False
        self._jump_active = False
        self._jump_frames = 0

        if self.level_id == 1:
            self._setup_level_one()
        else:
            self.physics_engine = None

    def _setup_level_one(self):
        self.spawn_point = (100, 150)
        self._respawn_player()

        ground = Platform(2400, 40, color=arcade.color.DARK_SLATE_GRAY)
        ground.center_x = 1200
        ground.center_y = 20
        self.platform_list.append(ground)
        ground.color = arcade.color.DARK_SLATE_GRAY
        ground.alpha = 255

        platform_positions = [
            (300, 140),
            (520, 220),
            (760, 300),
            (980, 220),
            (1200, 160),
            (1450, 260),
            (1700, 200),
        ]

        platform_colors = [
            arcade.color.LIGHT_SLATE_GRAY,
            arcade.color.COOL_GREY,
        ]

        for index, (x, y) in enumerate(platform_positions):
            platform = Platform(120, 24, color=platform_colors[index % 2])
            platform.center_x = x
            platform.center_y = y
            self.platform_list.append(platform)
            platform.color = platform_colors[index % 2]
            platform.alpha = 255

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
            spikes.color = arcade.color.RED
            spikes.alpha = 255

        self.enemy_physics_engines.clear()
        patrol = PatrolEnemy(left_bound=260, right_bound=440, speed=2.0)
        patrol.center_x = 300
        patrol.center_y = 180
        self.enemy_list.append(patrol)
        self.enemy_physics_engines.append(
            arcade.PhysicsEnginePlatformer(patrol, self.platform_list, gravity_constant=GRAVITY)
        )

        jumper = JumpingEnemy(jump_interval_min=1.0, jump_interval_max=2.0, jump_strength=12.0)
        jumper.center_x = 980
        jumper.center_y = 260
        self.enemy_list.append(jumper)
        self.enemy_physics_engines.append(
            arcade.PhysicsEnginePlatformer(jumper, self.platform_list, gravity_constant=GRAVITY)
        )

        goal_platform = Platform(80, 24, color=arcade.color.LIME_GREEN)
        goal_platform.center_x = 2100
        goal_platform.center_y = 140
        self.platform_list.append(goal_platform)
        goal_platform.color = arcade.color.LIME_GREEN
        goal_platform.alpha = 255

        self.level_end_x = 2100
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, self.platform_list, gravity_constant=GRAVITY
        )
        self.hud.lives = self.lives

    def _respawn_player(self):
        self.player.center_x, self.player.center_y = self.spawn_point
        self.player.change_x = 0
        self.player.change_y = 0

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
        
        # Обновить движение и анимацию игрока
        self.player.update(delta_time, self.keys_pressed)
        self.player.update_animation(delta_time)
        
        if self.physics_engine:
            # Обработка прыжка
            if self._jump_pressed and self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP_SPEED
                self._jump_frames = 0
                self._jump_active = True
            self._jump_pressed = False

            if self._jump_active:
                if self._jump_held and self._jump_frames < PLAYER_JUMP_HOLD_FRAMES:
                    self.player.change_y += PLAYER_JUMP_HOLD_FORCE
                    self._jump_frames += 1
                    if self._jump_frames >= PLAYER_JUMP_HOLD_FRAMES:
                        self._jump_active = False
                elif not self._jump_held and self.player.change_y > 0:
                    self.player.change_y *= 0.6
                    self._jump_active = False
                    self._jump_frames = PLAYER_JUMP_HOLD_FRAMES
            
            self.physics_engine.update()

            for engine in self.enemy_physics_engines:
                engine.update()
        else:
            self.player_list.update()

        coins_hit = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in coins_hit:
            coin.remove_from_sprite_lists()
            self.score += getattr(coin, "value", 0)

        if arcade.check_for_collision_with_list(self.player, self.hazard_list):
            self._handle_death()
            return

        if arcade.check_for_collision_with_list(self.player, self.enemy_list):
            self._handle_death()
            return

        if self.level_end_x and self.player.center_x >= self.level_end_x:
            self.state_manager.set_last_score(self.score)
            self.state_manager.update_progress(
                self.level_id, self.score, True, self.time_elapsed
            )
            self.state_manager.show_game_over(True)
            return

        if self.player.center_y < -200:
            self._handle_death()
            return

        self.camera.update(self.player)

    def _handle_death(self):
        self.lives -= 1
        self.hud.lives = self.lives
        if self.lives <= 0:
            self.state_manager.set_last_score(self.score)
            self.state_manager.update_progress(
                self.level_id, self.score, False, self.time_elapsed
            )
            self.state_manager.show_game_over(False)
            return
        self._respawn_player()

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        
        if key == arcade.key.P:
            self.state_manager.show_pause()
        elif key == arcade.key.ESCAPE:
            self.state_manager.show_menu()
        elif key in (arcade.key.SPACE, arcade.key.W, arcade.key.UP):
            self._jump_pressed = True
            self._jump_held = True

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)
        
        if key in (arcade.key.SPACE, arcade.key.W, arcade.key.UP):
            self._jump_held = False
