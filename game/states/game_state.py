import arcade

from game.config import (
    GRAVITY,
    PLAYER_JUMP_SPEED,
    PLAYER_JUMP_HOLD_FORCE,
    PLAYER_JUMP_HOLD_FRAMES,
    PLAYER_MOVE_SPEED,
    PYMUNK_JUMP_IMPULSE,
    PYMUNK_MAX_VERTICAL_SPEED,
    PYMUNK_MOVE_SPEED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from game.entities.player import Player
from game.levels import LevelBuilder, get_level_specs
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
        self.moving_platform_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.hazard_list = arcade.SpriteList()
        self.ui_button_list = arcade.SpriteList()

        self.player = None
        self.physics_engine = None
        self.pymunk_engine = None
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
        self._move_left = False
        self._move_right = False
        self._jump_pressed = False
        self._jump_held = False
        self._jump_active = False
        self._jump_frames = 0
        self._moving_platform_last_pos = {}
        self._platform_under = None

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
        self._platform_under = None


        level_specs = get_level_specs()
        spec = level_specs.get(self.level_id)
        if spec is None:
            self.physics_engine = None
            self.pymunk_engine = None
            return

        builder = LevelBuilder(self)
        builder.build(spec)

        if spec.physics == "platformer":
            self.physics_engine = arcade.PhysicsEnginePlatformer(
                self.player,
                platforms=self.moving_platform_list,
                walls=self.platform_list,
                gravity_constant=GRAVITY,
            )
            self.pymunk_engine = None
        elif spec.physics == "pymunk":
            self.physics_engine = None
            self.pymunk_engine = arcade.PymunkPhysicsEngine(
                gravity=spec.pymunk_gravity,
                damping=spec.pymunk_damping,
            )
            self.pymunk_engine.add_sprite(
                self.player,
                mass=1.0,
                friction=0.8,
                elasticity=0.0,
                moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF,
                max_vertical_velocity=PYMUNK_MAX_VERTICAL_SPEED,
            )
            self.pymunk_engine.space.iterations = 30
            if self.platform_list:
                self.pymunk_engine.add_sprite_list(
                    self.platform_list,
                    body_type=arcade.PymunkPhysicsEngine.STATIC,
                    friction=0.8,
                    elasticity=0.0,
                )
            if self.moving_platform_list:
                self.pymunk_engine.add_sprite_list(
                    self.moving_platform_list,
                    body_type=arcade.PymunkPhysicsEngine.KINEMATIC,
                    friction=0.8,
                    elasticity=0.0,
                )
        else:
            self.physics_engine = None
            self.pymunk_engine = None

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

        self.camera.use_hud()
        self.hud.score = self.score
        self.hud.time_elapsed = self.time_elapsed
        self.hud.draw()

    def on_update(self, delta_time: float):
        self.time_elapsed += delta_time
        self.enemy_list.update()
        if self.physics_engine:
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
        elif self.pymunk_engine:
            direction = (-1 if self._move_left else 0) + (1 if self._move_right else 0)
            self.pymunk_engine.set_horizontal_velocity(
                self.player, direction * PYMUNK_MOVE_SPEED
            )
            if self._jump_pressed and self._can_jump_pymunk():
                self.pymunk_engine.apply_impulse(self.player, (0, PYMUNK_JUMP_IMPULSE))
            self._jump_pressed = False
            sub_steps = 4
            step_dt = (1 / 60) / sub_steps
            for step in range(sub_steps):
                self.pymunk_engine.step(step_dt, resync_sprites=step == sub_steps - 1)
            self.pymunk_engine.set_rotation(self.player, 0)
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

    def _can_jump_pymunk(self):
        if arcade.check_for_collision_with_list(self.player, self.platform_list):
            return True
        if arcade.check_for_collision_with_list(self.player, self.moving_platform_list):
            return True
        return False

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
