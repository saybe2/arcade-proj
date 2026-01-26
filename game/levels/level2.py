from __future__ import annotations

import arcade

from game.levels.base import (
    CoinSpec,
    EnemySpec,
    HazardSpec,
    LevelSpec,
    MovingPlatformSpec,
    PlatformSpec,
)


def build_level() -> LevelSpec:
    return LevelSpec(
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
            EnemySpec("patrol", 2350, 340, {"left_bound": 2280, "right_bound": 2480}),
        ],
        end_x=2900,
        physics="platformer",
        requires_all_coins=True,
    )
