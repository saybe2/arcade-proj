from game.levels import get_level_specs


def test_level_specs_contains_levels():
    specs = get_level_specs()
    assert 1 in specs
    assert 2 in specs
    assert 3 in specs


def test_level_two_requires_all_coins_and_no_jumper():
    spec = get_level_specs()[2]
    assert spec.requires_all_coins is True
    assert all(enemy.kind != "jumping" for enemy in spec.enemies)


def test_level_three_has_time_limit():
    spec = get_level_specs()[3]
    assert spec.time_limit is not None
    assert spec.time_limit > 0
