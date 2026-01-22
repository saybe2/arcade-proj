from __future__ import annotations

import arcade


class SoundManager:
    def __init__(self):
        self.sfx = {}
        self.music = None
        self.volume = 0.5

    def load_sfx(self, key: str, path: str):
        self.sfx[key] = arcade.Sound(path)

    def play_sfx(self, key: str):
        sound = self.sfx.get(key)
        if sound:
            sound.play(volume=self.volume)

    def play_music(self, path: str):
        self.stop_music()
        self.music = arcade.Sound(path)
        self.music.play(volume=self.volume, loop=True)

    def stop_music(self):
        if self.music:
            self.music.stop()
            self.music = None

    def set_volume(self, volume: float):
        self.volume = max(0.0, min(1.0, volume))
