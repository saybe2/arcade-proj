import pytest
import arcade

from game.systems.camera import CameraManager


class DummyTarget:
    def __init__(self, x, y):
        self.center_x = x
        self.center_y = y


def test_camera_manager_updates_position():
    try:
        window = arcade.Window(100, 100, "test", visible=False)
    except Exception as exc:  # pragma: no cover - depends on environment
        pytest.skip(f"Could not create Arcade window: {exc}")

    try:
        camera = CameraManager(100, 100, pan_speed=1.0, window=window)
        target = DummyTarget(50, 60)
        camera.update(target)

        pos = camera.world_camera.position
        assert round(pos[0]) == 50
        assert round(pos[1]) == 60
    finally:
        window.close()
        arcade.close_window()
