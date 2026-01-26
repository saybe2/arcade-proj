from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import arcade

from game.entities.coin import Coin
from game.entities.enemy import JumpingEnemy, PatrolEnemy
from game.entities.hazard import Hazard
from game.entities.platform import Platform
from game.config import GRAVITY


@dataclass
class PlatformSpec:
    x: float
    y: float
    width: int
    height: int
    color: arcade.Color


@dataclass
class MovingPlatformSpec(PlatformSpec):
    change_x: float = 0.0
    change_y: float = 0.0
    boundary_left: Optional[float] = None
    boundary_right: Optional[float] = None
    boundary_bottom: Optional[float] = None
    boundary_top: Optional[float] = None


@dataclass
class CoinSpec:
    x: float
    y: float


@dataclass
class HazardSpec:
    x: float
    y: float
    width: int = 32
    height: int = 32
    damage: int = 10
    color: arcade.Color = arcade.color.RED


@dataclass
class EnemySpec:
    kind: str
    x: float
    y: float
    params: Dict[str, float] = field(default_factory=dict)


@dataclass
class LevelSpec:
    level_id: int
    spawn_point: Tuple[float, float]
    platforms: List[PlatformSpec] = field(default_factory=list)
    moving_platforms: List[MovingPlatformSpec] = field(default_factory=list)
    coins: List[CoinSpec] = field(default_factory=list)
    hazards: List[HazardSpec] = field(default_factory=list)
    enemies: List[EnemySpec] = field(default_factory=list)
    end_x: float = 0.0
    physics: str = "platformer"
    pymunk_gravity: Tuple[float, float] = (0, -900)
    pymunk_damping: float = 0.9


class LevelBuilder:
    def __init__(self, view):
        self.view = view

    def build(self, spec: LevelSpec):
        self.view.spawn_point = spec.spawn_point
        self.view._respawn_player()

        for platform_spec in spec.platforms:
            platform = Platform(
                platform_spec.width,
                platform_spec.height,
                color=platform_spec.color,
            )
            platform.center_x = platform_spec.x
            platform.center_y = platform_spec.y
            platform.color = platform_spec.color
            platform.alpha = 255
            self.view.platform_list.append(platform)

        for moving_spec in spec.moving_platforms:
            platform = Platform(
                moving_spec.width,
                moving_spec.height,
                color=moving_spec.color,
            )
            platform.center_x = moving_spec.x
            platform.center_y = moving_spec.y
            platform.change_x = moving_spec.change_x
            platform.change_y = moving_spec.change_y
            platform.boundary_left = moving_spec.boundary_left
            platform.boundary_right = moving_spec.boundary_right
            platform.boundary_bottom = moving_spec.boundary_bottom
            platform.boundary_top = moving_spec.boundary_top
            platform.color = moving_spec.color
            platform.alpha = 255
            self.view.moving_platform_list.append(platform)
            self.view._moving_platform_last_pos[platform] = (
                platform.center_x,
                platform.center_y,
            )

        for coin_spec in spec.coins:
            coin = Coin()
            coin.center_x = coin_spec.x
            coin.center_y = coin_spec.y
            self.view.coin_list.append(coin)

        for hazard_spec in spec.hazards:
            hazard = Hazard(
                width=hazard_spec.width,
                height=hazard_spec.height,
                damage=hazard_spec.damage,
                color=hazard_spec.color,
            )
            hazard.center_x = hazard_spec.x
            hazard.center_y = hazard_spec.y
            hazard.color = hazard_spec.color
            hazard.alpha = 255
            self.view.hazard_list.append(hazard)

        self.view.enemy_physics_engines.clear()
        for enemy_spec in spec.enemies:
            enemy = self._build_enemy(enemy_spec)
            if enemy is None:
                continue
            self.view.enemy_list.append(enemy)
            self.view.enemy_physics_engines.append(
                arcade.PhysicsEnginePlatformer(
                    enemy,
                    platforms=self.view.moving_platform_list,
                    walls=self.view.platform_list,
                    gravity_constant=GRAVITY,
                )
            )

        self.view.level_end_x = spec.end_x
        self.view.hud.lives = self.view.lives

    def _build_enemy(self, enemy_spec: EnemySpec):
        if enemy_spec.kind == "patrol":
            enemy = PatrolEnemy(
                left_bound=enemy_spec.params.get("left_bound", enemy_spec.x - 60),
                right_bound=enemy_spec.params.get("right_bound", enemy_spec.x + 60),
                speed=enemy_spec.params.get("speed", 2.0),
            )
        elif enemy_spec.kind == "jumping":
            enemy = JumpingEnemy(
                jump_interval_min=enemy_spec.params.get("interval_min", 1.0),
                jump_interval_max=enemy_spec.params.get("interval_max", 2.0),
                jump_strength=enemy_spec.params.get("jump_strength", 12.0),
            )
        else:
            return None

        enemy.center_x = enemy_spec.x
        enemy.center_y = enemy_spec.y
        return enemy


def get_level_specs() -> Dict[int, LevelSpec]:
    level_one = LevelSpec(
        level_id=1,
        spawn_point=(100, 150),
        platforms=[
            PlatformSpec(1200, 20, 2400, 40, arcade.color.DARK_SLATE_GRAY),
            PlatformSpec(300, 140, 120, 24, arcade.color.LIGHT_SLATE_GRAY),
            PlatformSpec(520, 220, 120, 24, arcade.color.COOL_GREY),
            PlatformSpec(760, 300, 120, 24, arcade.color.LIGHT_SLATE_GRAY),
            PlatformSpec(980, 220, 120, 24, arcade.color.COOL_GREY),
            PlatformSpec(1200, 160, 120, 24, arcade.color.LIGHT_SLATE_GRAY),
            PlatformSpec(1450, 260, 120, 24, arcade.color.COOL_GREY),
            PlatformSpec(1700, 200, 120, 24, arcade.color.LIGHT_SLATE_GRAY),
            PlatformSpec(2100, 140, 80, 24, arcade.color.LIME_GREEN),
        ],
        moving_platforms=[
            MovingPlatformSpec(
                1120,
                320,
                100,
                20,
                arcade.color.SEA_GREEN,
                change_x=1.5,
                boundary_left=1040,
                boundary_right=1320,
            )
        ],
        coins=[
            CoinSpec(300, 180),
            CoinSpec(520, 260),
            CoinSpec(760, 340),
            CoinSpec(980, 260),
            CoinSpec(1450, 300),
        ],
        hazards=[
            HazardSpec(620, 60),
            HazardSpec(1320, 60),
            HazardSpec(1900, 60),
        ],
        enemies=[
            EnemySpec("patrol", 300, 180, {"left_bound": 260, "right_bound": 440}),
            EnemySpec("jumping", 980, 260, {"jump_strength": 12.0}),
        ],
        end_x=2100,
        physics="platformer",
    )

    level_two = LevelSpec(
        level_id=2,
        spawn_point=(120, 200),
        platforms=[
            PlatformSpec(1600, 20, 3200, 40, arcade.color.DIM_GRAY),
            PlatformSpec(350, 160, 140, 24, arcade.color.LIGHT_STEEL_BLUE),
            PlatformSpec(600, 240, 140, 24, arcade.color.LIGHT_STEEL_BLUE),
            PlatformSpec(850, 320, 140, 24, arcade.color.LIGHT_STEEL_BLUE),
            PlatformSpec(1100, 240, 140, 24, arcade.color.LIGHT_STEEL_BLUE),
            PlatformSpec(1350, 160, 140, 24, arcade.color.LIGHT_STEEL_BLUE),
            PlatformSpec(1650, 220, 140, 24, arcade.color.LIGHT_STEEL_BLUE),
            PlatformSpec(1880, 300, 140, 24, arcade.color.LIGHT_STEEL_BLUE),
            PlatformSpec(2100, 380, 140, 24, arcade.color.LIGHT_STEEL_BLUE),
            PlatformSpec(2350, 300, 140, 24, arcade.color.LIGHT_STEEL_BLUE),
            PlatformSpec(2600, 220, 140, 24, arcade.color.LIGHT_STEEL_BLUE),
            PlatformSpec(2900, 160, 120, 24, arcade.color.LIME_GREEN),
        ],
        moving_platforms=[
            MovingPlatformSpec(
                1180,
                420,
                100,
                20,
                arcade.color.SEA_GREEN,
                change_x=1.8,
                boundary_left=1040,
                boundary_right=1320,
            ),
            MovingPlatformSpec(
                1780,
                250,
                100,
                20,
                arcade.color.DARK_SEA_GREEN,
                change_y=1.2,
                boundary_bottom=180,
                boundary_top=320,
            ),
        ],
        coins=[
            CoinSpec(350, 200),
            CoinSpec(600, 280),
            CoinSpec(850, 360),
            CoinSpec(1100, 280),
            CoinSpec(1650, 260),
            CoinSpec(1880, 340),
            CoinSpec(2100, 420),
            CoinSpec(2350, 340),
            CoinSpec(2600, 260),
        ],
        hazards=[
            HazardSpec(760, 60),
            HazardSpec(1500, 60),
            HazardSpec(2200, 60),
            HazardSpec(2800, 60),
        ],
        enemies=[
            EnemySpec("patrol", 600, 260, {"left_bound": 520, "right_bound": 720}),
            EnemySpec("jumping", 1880, 340, {"jump_strength": 12.0}),
            EnemySpec("patrol", 2350, 340, {"left_bound": 2280, "right_bound": 2480}),
        ],
        end_x=2900,
        physics="platformer",
    )

    return {1: level_one, 2: level_two}
