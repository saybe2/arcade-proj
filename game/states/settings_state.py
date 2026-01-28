import arcade

from game.config import SCREEN_HEIGHT, SCREEN_WIDTH
from game.states.base import BaseView
from game.ui.slider import Slider
from game.ui.button import Button


class SettingsView(BaseView):
    def __init__(self, state_manager):
        super().__init__(state_manager)

        # Title
        self._title_text = arcade.Text(
            "SETTINGS",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 100,
            arcade.color.WHITE,
            42,
            anchor_x="center",
            bold=True,
        )

        # Sliders
        center_x = SCREEN_WIDTH / 2
        slider_width = 300
        slider_height = 20

        sound = state_manager.sound

        self.music_slider = Slider(
            center_x + 80,
            SCREEN_HEIGHT / 2 + 80,
            slider_width,
            slider_height,
            min_value=0.0,
            max_value=1.0,
            initial_value=sound.music_volume,
            label="Music Volume:",
        )

        self.sfx_slider = Slider(
            center_x + 80,
            SCREEN_HEIGHT / 2 + 20,
            slider_width,
            slider_height,
            min_value=0.0,
            max_value=1.0,
            initial_value=sound.sfx_volume,
            label="SFX Volume:",
        )

        # Toggle buttons - единая цветовая палитра
        button_width = 200
        button_height = 50

        music_text = "UNMUTE MUSIC" if sound.music_muted else "MUTE MUSIC"
        self.music_toggle_button = Button(
            center_x - 120,
            SCREEN_HEIGHT / 2 - 60,
            button_width,
            button_height,
            music_text,
            color=(40, 80, 120),
            hover_color=(60, 120, 180),
            click_color=(20, 40, 80),
        )

        sfx_text = "UNMUTE SFX" if sound.sfx_muted else "MUTE SFX"
        self.sfx_toggle_button = Button(
            center_x + 120,
            SCREEN_HEIGHT / 2 - 60,
            button_width,
            button_height,
            sfx_text,
            color=(40, 80, 120),
            hover_color=(60, 120, 180),
            click_color=(20, 40, 80),
        )

        # Back button
        self.back_button = Button(
            center_x,
            100,
            250,
            50,
            "BACK",
            color=(40, 80, 120),
            hover_color=(60, 120, 180),
            click_color=(20, 40, 80),
        )

    def on_draw(self):
        self.clear()

        # Draw title
        self._title_text.draw()

        # Draw sliders
        self.music_slider.draw()
        self.sfx_slider.draw()

        # Draw buttons
        self.music_toggle_button.draw()
        self.sfx_toggle_button.draw()
        self.back_button.draw()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """Handle mouse movement."""
        self.music_toggle_button.check_mouse_hover(x, y)
        self.sfx_toggle_button.check_mouse_hover(x, y)
        self.back_button.check_mouse_hover(x, y)

        # Update sliders if dragging
        if self.music_slider.is_dragging:
            self.music_slider.check_mouse_drag(x, y)
            self.state_manager.sound.set_music_volume(self.music_slider.value)
            self.state_manager.save_audio_settings()

        if self.sfx_slider.is_dragging:
            self.sfx_slider.check_mouse_drag(x, y)
            self.state_manager.sound.set_sfx_volume(self.sfx_slider.value)
            self.state_manager.save_audio_settings()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """Handle mouse press."""
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Check sliders
            if self.music_slider.check_mouse_press(x, y):
                self.state_manager.sound.set_music_volume(self.music_slider.value)
                self.state_manager.save_audio_settings()
                return

            if self.sfx_slider.check_mouse_press(x, y):
                self.state_manager.sound.set_sfx_volume(self.sfx_slider.value)
                self.state_manager.save_audio_settings()
                return

            # Check buttons
            if self.music_toggle_button.check_mouse_press(x, y):
                sound = self.state_manager.sound
                sound.set_music_muted(not sound.music_muted)
                new_text = "UNMUTE MUSIC" if sound.music_muted else "MUTE MUSIC"
                self.music_toggle_button.update_text(new_text)
                self.state_manager.save_audio_settings()
                self.state_manager.sound.play_sfx("ui")

            elif self.sfx_toggle_button.check_mouse_press(x, y):
                sound = self.state_manager.sound
                sound.set_sfx_muted(not sound.sfx_muted)
                new_text = "UNMUTE SFX" if sound.sfx_muted else "MUTE SFX"
                self.sfx_toggle_button.update_text(new_text)
                self.state_manager.save_audio_settings()
                self.state_manager.sound.play_sfx("ui")

            elif self.back_button.check_mouse_press(x, y):
                self.state_manager.sound.play_sfx("ui")
                self.state_manager.show_menu()

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """Handle mouse release."""
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.music_slider.check_mouse_release(x, y)
            self.sfx_slider.check_mouse_release(x, y)
            self.music_toggle_button.check_mouse_release(x, y)
            self.sfx_toggle_button.check_mouse_release(x, y)
            self.back_button.check_mouse_release(x, y)

    def on_key_press(self, key, modifiers):
        """Keep keyboard shortcuts."""
        sound = self.state_manager.sound
        if key == arcade.key.UP:
            sound.set_music_volume(sound.music_volume + 0.1)
            self.music_slider.value = sound.music_volume
        elif key == arcade.key.DOWN:
            sound.set_music_volume(sound.music_volume - 0.1)
            self.music_slider.value = sound.music_volume
        elif key == arcade.key.RIGHT:
            sound.set_sfx_volume(sound.sfx_volume + 0.1)
            self.sfx_slider.value = sound.sfx_volume
        elif key == arcade.key.LEFT:
            sound.set_sfx_volume(sound.sfx_volume - 0.1)
            self.sfx_slider.value = sound.sfx_volume
        elif key == arcade.key.M:
            sound.set_music_muted(not sound.music_muted)
            new_text = "UNMUTE MUSIC" if sound.music_muted else "MUTE MUSIC"
            self.music_toggle_button.update_text(new_text)
        elif key == arcade.key.S:
            sound.set_sfx_muted(not sound.sfx_muted)
            new_text = "UNMUTE SFX" if sound.sfx_muted else "MUTE SFX"
            self.sfx_toggle_button.update_text(new_text)
        elif key == arcade.key.ESCAPE:
            self.state_manager.save_audio_settings()
            self.state_manager.show_menu()
            return
        else:
            return

        self.state_manager.save_audio_settings()
        self.state_manager.sound.play_sfx("ui")
