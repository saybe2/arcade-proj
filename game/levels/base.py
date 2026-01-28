from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import arcade

from game.config import GRAVITY
from game.entities.coin import Coin
from game.entities.enemy import JumpingEnemy, PatrolEnemy
from game.entities.hazard import Hazard
from game.entities.platform import Platform


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
    gravity_constant: float = GRAVITY
    requires_all_coins: bool = False
    time_limit: Optional[float] = None


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
            
            # Зеленые платформы - это финишные платформы
            if platform_spec.color in (arcade.color.LIME_GREEN, arcade.color.GREEN, arcade.color.DARK_GREEN):
                self.view.finish_platform_list.append(platform)
            
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
                    gravity_constant=spec.gravity_constant,
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
