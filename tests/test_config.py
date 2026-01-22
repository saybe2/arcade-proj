from game import config


def test_config_has_expected_values():
    assert config.SCREEN_WIDTH > 0
    assert config.SCREEN_HEIGHT > 0
    assert config.TARGET_FPS == 60
    assert config.GRAVITY > 0
    assert config.PLAYER_MOVE_SPEED > 0
    assert config.PLAYER_JUMP_SPEED > 0
