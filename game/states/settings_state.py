import arcade

from game.config import SCREEN_HEIGHT, SCREEN_WIDTH
from game.states.base import BaseView


class SettingsView(BaseView):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self._title_text = arcade.Text(
            "Settings",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 80,
            arcade.color.WHITE,
            36,
            anchor_x="center",
        )
        self._music_text = arcade.Text(
            "",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 20,
            arcade.color.LIGHT_GRAY,
            18,
            anchor_x="center",
        )
        self._sfx_text = arcade.Text(
            "",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 10,
            arcade.color.LIGHT_GRAY,
            18,
            anchor_x="center",
        )
        self._controls_text = arcade.Text(
            "Up/Down: Music  Left/Right: SFX",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 50,
            arcade.color.LIGHT_GRAY,
            14,
            anchor_x="center",
        )
        self._toggle_text = arcade.Text(
            "M: mute music  S: mute SFX  ESC: back",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 75,
            arcade.color.LIGHT_GRAY,
            14,
            anchor_x="center",
        )
        self._update_texts()

    def _format_volume(self, value: float) -> int:
        return int(value * 100)

    def _update_texts(self):
        sound = self.state_manager.sound
        music_state = "Muted" if sound.music_muted else f"{self._format_volume(sound.music_volume)}%"
        sfx_state = "Muted" if sound.sfx_muted else f"{self._format_volume(sound.sfx_volume)}%"
        self._music_text.text = f"Music Volume: {music_state}"
        self._sfx_text.text = f"SFX Volume: {sfx_state}"

    def on_draw(self):
        self.clear()
        self._title_text.draw()
        self._music_text.draw()
        self._sfx_text.draw()
        self._controls_text.draw()
        self._toggle_text.draw()

    def on_key_press(self, key, modifiers):
        sound = self.state_manager.sound
        if key == arcade.key.UP:
            sound.set_music_volume(sound.music_volume + 0.1)
        elif key == arcade.key.DOWN:
            sound.set_music_volume(sound.music_volume - 0.1)
        elif key == arcade.key.RIGHT:
            sound.set_sfx_volume(sound.sfx_volume + 0.1)
        elif key == arcade.key.LEFT:
            sound.set_sfx_volume(sound.sfx_volume - 0.1)
        elif key == arcade.key.M:
            sound.set_music_muted(not sound.music_muted)
        elif key == arcade.key.S:
            sound.set_sfx_muted(not sound.sfx_muted)
        elif key == arcade.key.ESCAPE:
            self.state_manager.save_audio_settings()
            self.state_manager.show_menu()
            return
        else:
            return

        self.state_manager.save_audio_settings()
        self.state_manager.sound.play_sfx("ui")
        self._update_texts()
