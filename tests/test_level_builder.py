import arcade

from game.levels.base import (
    CoinSpec,
    HazardSpec,
    LevelBuilder,
    LevelSpec,
    MovingPlatformSpec,
    PlatformSpec,
)


class DummyHUD:
    def __init__(self):
        self.lives = 0


class DummyView:
    def __init__(self):
        self.platform_list = arcade.SpriteList()
        self.moving_platform_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.hazard_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.enemy_physics_engines = []
        self.hud = DummyHUD()
        self.lives = 3
        self.level_end_x = 0
        self.spawn_point = (0, 0)
        self._moving_platform_last_pos = {}
        self._respawned = False

    def _respawn_player(self):
        self._respawned = True


def test_level_builder_populates_lists():
    view = DummyView()
    spec = LevelSpec(
        level_id=99,
        spawn_point=(120, 140),
        platforms=[PlatformSpec(100, 50, 80, 20, arcade.color.GRAY)],
        moving_platforms=[
            MovingPlatformSpec(
                200,
                100,
                60,
                16,
                arcade.color.GREEN,
                change_x=1.0,
                boundary_left=180,
                boundary_right=240,
            )
        ],
        coins=[CoinSpec(150, 90)],
        hazards=[HazardSpec(180, 60)],
        end_x=500,
    )

    builder = LevelBuilder(view)
    builder.build(spec)

    assert view._respawned is True
    assert view.spawn_point == (120, 140)
    assert len(view.platform_list) == 1
    assert len(view.moving_platform_list) == 1
    assert len(view.coin_list) == 1
    assert len(view.hazard_list) == 1
    assert view.level_end_x == 500
