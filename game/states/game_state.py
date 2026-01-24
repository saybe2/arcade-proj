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
from game.entities.player import FaceDirection, Player
from game.levels import LevelBuilder, get_level_specs
from game.states.base import BaseView
from game.systems.camera import CameraManager
from game.systems.particles import ParticleEmitter, ParticleManager
from game.ui.hud import HUD


class GameView(BaseView):
    def __init__(self, state_manager, level_id: int):
        super().__init__(state_manager)
        self.level_id = level_id

        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList()
        self.moving_platform_list = arcade.SpriteList()
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
        self.particles = ParticleManager()

        self.score = 0
        self.time_elapsed = 0.0
        self.level_end_x = 0
        self.lives = 3
        self.spawn_point = (100, 150)
        self._move_left = False
        self._move_right = False
        self._jump_pressed = False
        self._jump_held = False
        self._jump_active = False
        self._jump_frames = 0
        self._moving_platform_last_pos = {}

    def setup(self):
        self.player_list.clear()
        self.enemy_list.clear()
        self.platform_list.clear()
        self.moving_platform_list.clear()
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
        self._move_left = False
        self._move_right = False
        self._jump_pressed = False
        self._jump_held = False
        self._jump_active = False
        self._jump_frames = 0
        self._moving_platform_last_pos = {}
        self.particles.clear()

        level_specs = get_level_specs()
        spec = level_specs.get(self.level_id)
        if spec is None:
            self.physics_engine = None
            return

        builder = LevelBuilder(self)
        builder.build(spec)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            platforms=self.moving_platform_list,
            walls=self.platform_list,
            gravity_constant=GRAVITY,
        )

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
        self.moving_platform_list.draw()
        self.coin_list.draw()
        self.hazard_list.draw()
        self.enemy_list.draw()
        self.player_list.draw()
        self.particles.draw()

        self.camera.use_hud()
        self.hud.score = self.score
        self.hud.time_elapsed = self.time_elapsed
        self.hud.draw()

    def on_update(self, delta_time: float):
        self.time_elapsed += delta_time
        self.particles.update(delta_time)
        self.enemy_list.update()

        player_prev_x = self.player.center_x
        player_prev_y = self.player.center_y
        prev_positions = {
            platform: self._moving_platform_last_pos.get(
                platform, (platform.center_x, platform.center_y)
            )
            for platform in self.moving_platform_list
        }

        direction = (-1 if self._move_left else 0) + (1 if self._move_right else 0)
        input_dx = direction * PLAYER_MOVE_SPEED
        self.player.change_x = input_dx
        self._update_player_animation(delta_time)

        if self._jump_pressed and self.physics_engine and self.physics_engine.can_jump():
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

        if self.physics_engine:
            self.physics_engine.update()

        platform_under = self._platform_under_player()
        if platform_under and not self._jump_active:
            prev_x, prev_y = prev_positions.get(
                platform_under, (platform_under.center_x, platform_under.center_y)
            )
            delta_x = platform_under.center_x - prev_x
            delta_y = platform_under.center_y - prev_y
            player_dx = self.player.center_x - player_prev_x
            extra_dx = player_dx - input_dx
            carry_x = delta_x

            if delta_x != 0 and extra_dx != 0 and (delta_x > 0) == (extra_dx > 0):
                carry_x = delta_x - extra_dx

            if delta_x > 0:
                carry_x = max(0, min(delta_x, carry_x))
            elif delta_x < 0:
                carry_x = min(0, max(delta_x, carry_x))

            self.player.center_x += carry_x
            if delta_y:
                self.player.center_y += delta_y

        for platform in self.moving_platform_list:
            self._moving_platform_last_pos[platform] = (
                platform.center_x,
                platform.center_y,
            )

        for engine in self.enemy_physics_engines:
            engine.update()

        coins_hit = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in coins_hit:
            self._spawn_particles(
                (coin.center_x, coin.center_y),
                color=arcade.color.GOLD,
                count=6,
                speed_range=(40, 120),
                lifetime_range=(0.25, 0.55),
                size_range=(3, 6),
            )
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

    def _update_player_animation(self, delta_time: float):
        if self._move_left:
            self.player.face_direction = FaceDirection.LEFT
        elif self._move_right:
            self.player.face_direction = FaceDirection.RIGHT
        self.player.is_walking = self._move_left or self._move_right
        self.player.update_animation(delta_time)

    def _spawn_particles(
        self,
        position,
        color,
        count=8,
        speed_range=(40, 140),
        lifetime_range=(0.3, 0.7),
        size_range=(3, 6),
    ):
        emitter = ParticleEmitter()
        emitter.emit_burst(
            position=position,
            color=color,
            count=count,
            speed_range=speed_range,
            lifetime_range=lifetime_range,
            size_range=size_range,
        )
        self.particles.emitters.append(emitter)

    def _platform_under_player(self):
        if not self.moving_platform_list:
            return None
        if self.player.change_y > 0:
            return None
        original_y = self.player.center_y
        self.player.center_y -= 10
        candidates = arcade.check_for_collision_with_list(
            self.player, self.moving_platform_list
        )
        self.player.center_y = original_y
        if not candidates:
            return None
        best_platform = None
        best_top = None
        for platform in candidates:
            if self.player.right <= platform.left or self.player.left >= platform.right:
                continue
            if self.player.center_y < platform.center_y:
                continue
            if best_top is None or platform.top > best_top:
                best_platform = platform
                best_top = platform.top
        return best_platform

    def _handle_death(self):
        self._spawn_particles(
            (self.player.center_x, self.player.center_y),
            color=arcade.color.RED,
            count=14,
            speed_range=(80, 200),
            lifetime_range=(0.4, 0.9),
            size_range=(4, 7),
        )
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
        if key in (arcade.key.LEFT, arcade.key.A):
            self._move_left = True
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self._move_right = True
        elif key in (arcade.key.SPACE, arcade.key.W, arcade.key.UP):
            self._jump_pressed = True
            self._jump_held = True
        elif key == arcade.key.P:
            self.state_manager.show_pause()
        elif key == arcade.key.ESCAPE:
            self.state_manager.show_menu()

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self._move_left = False
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self._move_right = False
        elif key in (arcade.key.SPACE, arcade.key.W, arcade.key.UP):
            self._jump_held = False
