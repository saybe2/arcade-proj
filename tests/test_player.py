import arcade

from game.entities.player import FaceDirection, Player


def test_player_update_no_keys():
    player = Player(100, 100)
    before = (player.center_x, player.center_y)
    player.update(1 / 60, None)
    after = (player.center_x, player.center_y)
    assert before == after
    assert player.is_walking is False


def test_player_update_moves_and_sets_direction():
    player = Player(100, 100)
    keys = {arcade.key.RIGHT}
    player.update(1 / 60, keys)
    assert player.center_x > 100
    assert player.face_direction == FaceDirection.RIGHT
    assert player.is_walking is True
