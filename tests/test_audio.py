from game.systems.audio import SoundManager


def test_audio_missing_files_are_safe(tmp_path):
    manager = SoundManager()
    missing_wav = tmp_path / "missing.wav"
    missing_ogg = tmp_path / "missing.ogg"

    assert manager.load_sfx("missing", str(missing_wav)) is False
    assert manager.play_music(str(missing_ogg)) is False

    # Should not raise if key is missing
    manager.play_sfx("nope")
    manager.stop_music()
