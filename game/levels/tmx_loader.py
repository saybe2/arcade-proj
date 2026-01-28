"""
TMX Level Loader for Tiled Map Editor files.

This module loads levels created in Tiled Map Editor (.tmx files)
and converts them to LevelSpec objects that the game can use.

Supports both Tile Layers (for visuals) and Object Layers (for game logic).
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import arcade

from game.levels.base import (
    CoinSpec,
    EnemySpec,
    HazardSpec,
    LevelSpec,
    MovingPlatformSpec,
    PlatformSpec,
)


class TMXLevelLoader:
    """Loads levels from Tiled Map Editor .tmx files."""

    def __init__(self, tmx_path: str):
        """
        Initialize the TMX loader.

        Args:
            tmx_path: Path to the .tmx file
        """
        self.tmx_path = tmx_path
        self.tile_map = None
        self.visual_layers = {}  # Store visual tile layers

    def load(self) -> Optional[LevelSpec]:
        """
        Load a level from a .tmx file.

        Supports:
        - Tile Layers: Background, Ground, Decorations, Collision (visual)
        - Object Layers: Spawn, Platforms, MovingPlatforms, Coins, Hazards, Enemies, Finish

        Returns:
            LevelSpec object or None if loading failed
        """
        if not Path(self.tmx_path).exists():
            print(f"TMX file not found: {self.tmx_path}")
            return None

        try:
            # Load the tile map
            self.tile_map = arcade.load_tilemap(self.tmx_path)

            # Extract level properties
            level_id = self._get_property("level_id", 1, int)
            time_limit = self._get_property("time_limit", None, float)
            requires_all_coins = self._get_property("requires_all_coins", False, bool)
            gravity = self._get_property("gravity", 1.0, float)

            # Extract spawn point
            spawn_point = self._extract_spawn_point()

            # Extract game objects from OBJECT layers
            platforms = self._extract_platforms()
            moving_platforms = self._extract_moving_platforms()
            coins = self._extract_coins()
            hazards = self._extract_hazards()
            enemies = self._extract_enemies()
            end_x = self._extract_end_x()

            # Extract visual TILE layers
            self._extract_visual_layers()

            # Create LevelSpec
            level_spec = LevelSpec(
                level_id=level_id,
                spawn_point=spawn_point,
                platforms=platforms,
                moving_platforms=moving_platforms,
                coins=coins,
                hazards=hazards,
                enemies=enemies,
                end_x=end_x,
                physics="platformer",
                gravity_constant=gravity,
                requires_all_coins=requires_all_coins,
                time_limit=time_limit,
            )

            # Attach visual layers to level spec
            level_spec.visual_layers = self.visual_layers

            return level_spec

        except Exception as e:
            print(f"Error loading TMX file: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _extract_visual_layers(self):
        """Extract visual tile layers for rendering."""
        if not self.tile_map or not hasattr(self.tile_map, 'sprite_lists'):
            return

        # Common visual layer names
        visual_layer_names = [
            "Background",
            "Ground", 
            "Decorations",
            "Foreground",
            "Collision"  # Visual collision layer (for debugging)
        ]

        for layer_name in visual_layer_names:
            if layer_name in self.tile_map.sprite_lists:
                self.visual_layers[layer_name] = self.tile_map.sprite_lists[layer_name]
                print(f"Loaded visual layer: {layer_name}")

    def _get_property(self, name: str, default, prop_type=str):
        """Get a property from the tile map."""
        if not self.tile_map or not hasattr(self.tile_map, "properties"):
            return default

        value = self.tile_map.properties.get(name, default)
        if value is None:
            return default

        try:
            return prop_type(value)
        except (ValueError, TypeError):
            return default

    def _extract_spawn_point(self) -> tuple[float, float]:
        """Extract player spawn point from Spawn object layer."""
        if not self.tile_map:
            return (100, 150)

        # Look for Spawn object layer
        spawn_layer = self.tile_map.object_lists.get("Spawn")
        if spawn_layer and len(spawn_layer) > 0:
            spawn_obj = spawn_layer[0]
            return (spawn_obj.shape[0], spawn_obj.shape[1])

        return (100, 150)

    def _extract_platforms(self) -> list[PlatformSpec]:
        """Extract static platforms from Platforms object layer."""
        platforms = []

        if not self.tile_map:
            return platforms

        platform_layer = self.tile_map.object_lists.get("Platforms")
        if not platform_layer:
            return platforms

        for obj in platform_layer:
            # Get position and size
            x, y = obj.shape[0], obj.shape[1]
            width = int(obj.properties.get("width", obj.shape[2] if len(obj.shape) > 2 else 100))
            height = int(obj.properties.get("height", obj.shape[3] if len(obj.shape) > 3 else 24))

            # Get color
            color_hex = obj.properties.get("color", "#708090")
            color = self._hex_to_rgb(color_hex)

            platforms.append(
                PlatformSpec(x=x, y=y, width=width, height=height, color=color)
            )

        return platforms

    def _extract_moving_platforms(self) -> list[MovingPlatformSpec]:
        """Extract moving platforms from MovingPlatforms object layer."""
        moving_platforms = []

        if not self.tile_map:
            return moving_platforms

        moving_layer = self.tile_map.object_lists.get("MovingPlatforms")
        if not moving_layer:
            return moving_platforms

        for obj in moving_layer:
            x, y = obj.shape[0], obj.shape[1]
            width = int(obj.properties.get("width", 100))
            height = int(obj.properties.get("height", 20))
            color_hex = obj.properties.get("color", "#2E8B57")
            color = self._hex_to_rgb(color_hex)

            change_x = float(obj.properties.get("change_x", 0.0))
            change_y = float(obj.properties.get("change_y", 0.0))
            boundary_left = obj.properties.get("boundary_left")
            boundary_right = obj.properties.get("boundary_right")
            boundary_bottom = obj.properties.get("boundary_bottom")
            boundary_top = obj.properties.get("boundary_top")

            if boundary_left is not None:
                boundary_left = float(boundary_left)
            if boundary_right is not None:
                boundary_right = float(boundary_right)
            if boundary_bottom is not None:
                boundary_bottom = float(boundary_bottom)
            if boundary_top is not None:
                boundary_top = float(boundary_top)

            moving_platforms.append(
                MovingPlatformSpec(
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    color=color,
                    change_x=change_x,
                    change_y=change_y,
                    boundary_left=boundary_left,
                    boundary_right=boundary_right,
                    boundary_bottom=boundary_bottom,
                    boundary_top=boundary_top,
                )
            )

        return moving_platforms

    def _extract_coins(self) -> list[CoinSpec]:
        """Extract coins from Coins object layer."""
        coins = []

        if not self.tile_map:
            return coins

        coin_layer = self.tile_map.object_lists.get("Coins")
        if not coin_layer:
            return coins

        for obj in coin_layer:
            x, y = obj.shape[0], obj.shape[1]
            coins.append(CoinSpec(x=x, y=y))

        return coins

    def _extract_hazards(self) -> list[HazardSpec]:
        """Extract hazards from Hazards object layer."""
        hazards = []

        if not self.tile_map:
            return hazards

        hazard_layer = self.tile_map.object_lists.get("Hazards")
        if not hazard_layer:
            return hazards

        for obj in hazard_layer:
            x, y = obj.shape[0], obj.shape[1]
            width = int(obj.properties.get("width", 32))
            height = int(obj.properties.get("height", 32))
            damage = int(obj.properties.get("damage", 10))
            color_hex = obj.properties.get("color", "#8B0000")
            color = self._hex_to_rgb(color_hex)

            hazards.append(
                HazardSpec(
                    x=x, y=y, width=width, height=height, damage=damage, color=color
                )
            )

        return hazards

    def _extract_enemies(self) -> list[EnemySpec]:
        """Extract enemies from Enemies object layer."""
        enemies = []

        if not self.tile_map:
            return enemies

        enemy_layer = self.tile_map.object_lists.get("Enemies")
        if not enemy_layer:
            return enemies

        for obj in enemy_layer:
            x, y = obj.shape[0], obj.shape[1]
            enemy_type = obj.properties.get("type", "patrol")

            params = {}
            if enemy_type == "patrol":
                params["left_bound"] = float(
                    obj.properties.get("left_bound", x - 60)
                )
                params["right_bound"] = float(
                    obj.properties.get("right_bound", x + 60)
                )
                params["speed"] = float(obj.properties.get("speed", 2.0))
            elif enemy_type == "jumping":
                params["interval_min"] = float(
                    obj.properties.get("interval_min", 1.0)
                )
                params["interval_max"] = float(
                    obj.properties.get("interval_max", 2.0)
                )
                params["jump_strength"] = float(
                    obj.properties.get("jump_strength", 12.0)
                )
            elif enemy_type == "flying":
                params["amplitude"] = float(obj.properties.get("amplitude", 40.0))
                params["speed"] = float(obj.properties.get("speed", 2.5))

            enemies.append(EnemySpec(kind=enemy_type, x=x, y=y, params=params))

        return enemies

    def _extract_end_x(self) -> float:
        """Extract level end position from Finish/Exit object layer."""
        if not self.tile_map:
            return 0.0

        # Try both "Finish" and "Exit" layer names
        finish_layer = self.tile_map.object_lists.get("Finish") or self.tile_map.object_lists.get("Exit")
        if finish_layer and len(finish_layer) > 0:
            finish_obj = finish_layer[0]
            return finish_obj.shape[0]

        return 0.0

    def _hex_to_rgb(self, hex_color: str) -> tuple[int, int, int]:
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip("#")
        try:
            return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
        except (ValueError, IndexError):
            return (128, 128, 128)  # Default gray


def load_tmx_level(tmx_path: str) -> Optional[LevelSpec]:
    """
    Convenience function to load a TMX level.

    Args:
        tmx_path: Path to the .tmx file

    Returns:
        LevelSpec object or None if loading failed
    """
    loader = TMXLevelLoader(tmx_path)
    return loader.load()
