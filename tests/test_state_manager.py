import arcade
import pytest

from game.state_manager import StateManager


class DummyWindow:
    def __init__(self):
        self.last_view = None

    def show_view(self, view):
        self.last_view = view


def test_state_manager_menu_and_level_select_views():
    try:
        window = arcade.Window(100, 100, "test", visible=False)
    except Exception as exc:  # pragma: no cover - depends on environment
        pytest.skip(f"Could not create Arcade window: {exc}")

    try:
        manager = StateManager(window)
        manager.show_menu()
        assert manager.get_game_view() is None
        assert manager.window is window

        manager.show_level_select()
        assert manager.get_game_view() is None
    finally:
        window.close()
        arcade.close_window()


def test_state_manager_tracks_score_and_level():
    window = DummyWindow()
    manager = StateManager(window)
    manager.set_last_score(250)

    assert manager.last_score == 250
    assert manager.current_level == 1
