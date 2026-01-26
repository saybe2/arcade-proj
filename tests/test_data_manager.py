from game.systems.data import DataManager


def test_default_data_shape():
    data = DataManager.default_data()
    assert data["player_name"] == "Player1"
    assert data["levels_completed"] == []
    assert data["high_scores"] == {}
    assert data["best_times"] == {}
    assert data["last_times"] == {}
    assert data["total_playtime"] == 0
    assert data["last_played"] is None


def test_save_and_load_round_trip(tmp_path):
    save_path = tmp_path / "game_data.json"
    manager = DataManager(path=str(save_path))
    manager.data["player_name"] = "Tester"
    manager.data["levels_completed"] = [1, 2]
    manager.data["high_scores"] = {"level_1": 123}
    manager.data["best_times"] = {"level_1": 45}
    manager.data["last_times"] = {"level_1": 50}
    manager.data["total_playtime"] = 42
    manager.data["last_played"] = "2026-01-22T00:00:00"
    manager.save()

    reloaded = DataManager(path=str(save_path))
    data = reloaded.load()

    assert data["player_name"] == "Tester"
    assert data["levels_completed"] == [1, 2]
    assert data["high_scores"]["level_1"] == 123
    assert data["best_times"]["level_1"] == 45
    assert data["last_times"]["level_1"] == 50
    assert data["total_playtime"] == 42
    assert data["last_played"] == "2026-01-22T00:00:00"
