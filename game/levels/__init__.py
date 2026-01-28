from __future__ import annotations

from pathlib import Path

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
from game.levels.tmx_loader import load_tmx_level


__all__ = [
    "CoinSpec",
    "EnemySpec",
    "HazardSpec",
    "LevelBuilder",
    "LevelSpec",
    "MovingPlatformSpec",
    "PlatformSpec",
    "get_level_specs",
    "load_tmx_level",
]


def get_level_specs():
    """
    Get all available level specifications.
    
    Loads levels from both Python files and TMX files.
    TMX files in levels/tmx/ folder will be automatically loaded.
    """
    levels = {}
    
    # Load Python-defined levels
    level_one = build_level_one()
    level_two = build_level_two()
    level_three = build_level_three()
    levels[1] = level_one
    levels[2] = level_two
    levels[3] = level_three
    
    # Load TMX levels from levels/tmx/ folder
    tmx_folder = Path("levels/tmx")
    if tmx_folder.exists():
        for tmx_file in tmx_folder.glob("*.tmx"):
            try:
                level_spec = load_tmx_level(str(tmx_file))
                if level_spec:
                    levels[level_spec.level_id] = level_spec
                    print(f"Loaded TMX level {level_spec.level_id} from {tmx_file.name}")
            except Exception as e:
                print(f"Failed to load TMX level {tmx_file.name}: {e}")
    
    return levels
