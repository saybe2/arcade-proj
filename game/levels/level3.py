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
        level_id=3,
        spawn_point=(120, 200),
        platforms=[
            PlatformSpec(1700, 20, 3400, 40, arcade.color.DARK_GRAY),
            PlatformSpec(340, 180, 140, 24, arcade.color.LIGHT_STEEL_BLUE),
            PlatformSpec(620, 260, 140, 24, arcade.color.LIGHT_STEEL_BLUE),
            PlatformSpec(900, 340, 140, 24, arcade.color.LIGHT_STEEL_BLUE),
            PlatformSpec(1180, 260, 140, 24, arcade.color.LIGHT_STEEL_BLUE),
            PlatformSpec(1460, 180, 140, 24, arcade.color.LIGHT_STEEL_BLUE),
            PlatformSpec(1760, 260, 140, 24, arcade.color.LIGHT_STEEL_BLUE),
            PlatformSpec(2040, 340, 140, 24, arcade.color.LIGHT_STEEL_BLUE),
            PlatformSpec(2320, 260, 140, 24, arcade.color.LIGHT_STEEL_BLUE),
            PlatformSpec(2600, 180, 140, 24, arcade.color.LIGHT_STEEL_BLUE),
            PlatformSpec(3000, 200, 120, 24, arcade.color.LIME_GREEN),
        ],
        moving_platforms=[
            MovingPlatformSpec(
                1520,
                420,
                100,
                20,
                arcade.color.SEA_GREEN,
                change_x=2.0,
                boundary_left=1360,
                boundary_right=1680,
            ),
            MovingPlatformSpec(
                2240,
                220,
                100,
                20,
                arcade.color.DARK_SEA_GREEN,
                change_y=1.6,
                boundary_bottom=160,
                boundary_top=320,
            ),
        ],
        coins=[
            CoinSpec(340, 220),
            CoinSpec(620, 300),
            CoinSpec(900, 380),
            CoinSpec(1180, 300),
            CoinSpec(1760, 300),
            CoinSpec(2040, 380),
            CoinSpec(2320, 300),
            CoinSpec(2600, 220),
        ],
        hazards=[
            HazardSpec(520, 60),
            HazardSpec(980, 60),
            HazardSpec(1400, 60),
            HazardSpec(1960, 60),
            HazardSpec(2480, 60),
        ],
        enemies=[
            EnemySpec("patrol", 620, 280, {"left_bound": 540, "right_bound": 740}),
            EnemySpec("jumping", 1180, 300, {"jump_strength": 12.0}),
            EnemySpec("patrol", 2040, 360, {"left_bound": 1960, "right_bound": 2200}),
        ],
        end_x=3000,
        physics="platformer",
        time_limit=45.0,
    )
