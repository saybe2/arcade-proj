from __future__ import annotations

from pathlib import Path

import arcade


class SoundManager:
    def __init__(self):
        self.sfx = {}
        self.music = None
        self.music_player = None
        self.current_music_path = None
        self.sfx_volume = 0.5
        self.music_volume = 0.5
        self.sfx_muted = False
        self.music_muted = False

    def load_sfx(self, key: str, path: str):
        if not Path(path).exists():
            return False
        self.sfx[key] = arcade.Sound(path)
        return True

    def play_sfx(self, key: str):
        sound = self.sfx.get(key)
        if sound:
            volume = 0.0 if self.sfx_muted else self.sfx_volume
            sound.play(volume=volume)

    def play_music(self, path: str):
        if not Path(path).exists():
            return False
        
        # Если эта музыка уже играет - не перезапускать
        if self.current_music_path == path and self.music_player:
            return True
        
        self.stop_music()
        self.music = arcade.Sound(path)
        self.music_player = self.music.play(
            volume=self._music_effective_volume(), loop=True
        )
        self.current_music_path = path
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
        self.current_music_path = None

    def set_volume(self, volume: float):
        self.set_sfx_volume(volume)
        self.set_music_volume(volume)

    def set_sfx_volume(self, volume: float):
        self.sfx_volume = max(0.0, min(1.0, volume))

    def set_music_volume(self, volume: float):
        self.music_volume = max(0.0, min(1.0, volume))
        if self.music_player:
            self.music_player.volume = self._music_effective_volume()

    def set_sfx_muted(self, muted: bool):
        self.sfx_muted = bool(muted)

    def set_music_muted(self, muted: bool):
        self.music_muted = bool(muted)
        if self.music_player:
            self.music_player.volume = self._music_effective_volume()

    def _music_effective_volume(self) -> float:
        return 0.0 if self.music_muted else self.music_volume
