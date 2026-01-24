from __future__ import annotations

from pathlib import Path

import arcade


class SoundManager:
    def __init__(self):
        self.sfx = {}
        self.music = None
        self.music_player = None
        self.volume = 0.5

    def load_sfx(self, key: str, path: str):
        if not Path(path).exists():
            return False
        self.sfx[key] = arcade.Sound(path)
        return True

    def play_sfx(self, key: str):
        sound = self.sfx.get(key)
        if sound:
            sound.play(volume=self.volume)

    def play_music(self, path: str):
        if not Path(path).exists():
            return False
        self.stop_music()
        self.music = arcade.Sound(path)
        self.music_player = self.music.play(volume=self.volume, loop=True)
        return True

    def stop_music(self):
        if self.music_player:
            try:
                self.music_player.pause()
            except Exception:
                pass
            try:
                if hasattr(self.music_player, "seek"):
                    self.music_player.seek(0)
            except Exception:
                pass
            try:
                self.music_player.delete()
            except Exception:
                pass
            self.music_player = None
        self.music = None

    def set_volume(self, volume: float):
        self.volume = max(0.0, min(1.0, volume))
