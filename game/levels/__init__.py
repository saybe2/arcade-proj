from __future__ import annotations

from game.levels.base import (
    CoinSpec,
    EnemySpec,
    HazardSpec,
    LevelBuilder,
    LevelSpec,
    MovingPlatformSpec,
    PlatformSpec,
)
from game.levels.level1 import build_level as build_level_one
from game.levels.level2 import build_level as build_level_two
from game.levels.level3 import build_level as build_level_three


__all__ = [
    "CoinSpec",
    "EnemySpec",
    "HazardSpec",
    "LevelBuilder",
    "LevelSpec",
    "MovingPlatformSpec",
    "PlatformSpec",
    "get_level_specs",
]


def get_level_specs():
    level_one = build_level_one()
    level_two = build_level_two()
    level_three = build_level_three()
    return {1: level_one, 2: level_two, 3: level_three}
