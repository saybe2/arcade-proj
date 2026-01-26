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
