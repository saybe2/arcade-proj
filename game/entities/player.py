import arcade
from pathlib import Path
import enum


class FaceDirection(enum.Enum):
    """Facing direction for the player."""
    LEFT = 0
    RIGHT = 1


class Player(arcade.Sprite):
    def __init__(self, x: float = 100, y: float = 150, scale: float = 0.1):
        super().__init__()

        self.scale = scale
        self.speed = 300
        self.health = 100

        self.walking_textures = []
        walking_path = Path("assets/player/anim/walking")

        if walking_path.exists():
            for i in range(9):
                frame_path = walking_path / f"{i}.png"
                if frame_path.exists():
                    self.walking_textures.append(arcade.load_texture(str(frame_path)))

        if self.walking_textures:
            self.idle_texture = self.walking_textures[0]
            self.texture = self.idle_texture
        else:
            self.idle_texture = arcade.make_soft_square_texture(
                32, arcade.color.BLUE, 255, 0
            )
            self.texture = self.idle_texture

        self.current_frame = 0
        self.frame_counter = 0.0
        self.frame_duration = 0.1

        self.is_walking = False
        self.face_direction = FaceDirection.RIGHT

        self.center_x = x
        self.center_y = y
        self.is_alive = True

    def update_animation(self, delta_time: float = 1 / 60):
        if self.is_walking and self.walking_textures:
            self.frame_counter += delta_time

            if self.frame_counter >= self.frame_duration:
                self.frame_counter = 0.0
                self.current_frame = (self.current_frame + 1) % len(self.walking_textures)

                if self.face_direction == FaceDirection.RIGHT:
                    self.texture = self.walking_textures[self.current_frame]
                else:
                    self.texture = self.walking_textures[
                        self.current_frame
                    ].flip_horizontally()
        else:
            if self.face_direction == FaceDirection.RIGHT:
                self.texture = self.idle_texture
            else:
                self.texture = self.idle_texture.flip_horizontally()

    def update(self, delta_time: float = 1 / 60, keys_pressed: set | None = None):
        if not keys_pressed:
            self.is_walking = False
            return

        dx, dy = 0.0, 0.0

        if arcade.key.LEFT in keys_pressed or arcade.key.A in keys_pressed:
            dx -= self.speed * delta_time
        if arcade.key.RIGHT in keys_pressed or arcade.key.D in keys_pressed:
            dx += self.speed * delta_time
        if arcade.key.UP in keys_pressed or arcade.key.W in keys_pressed:
            dy += self.speed * delta_time
        if arcade.key.DOWN in keys_pressed or arcade.key.S in keys_pressed:
            dy -= self.speed * delta_time

        if dx != 0 and dy != 0:
            factor = 0.7071
            dx *= factor
            dy *= factor

        self.center_x += dx
        self.center_y += dy

        if dx < 0:
            self.face_direction = FaceDirection.LEFT
        elif dx > 0:
            self.face_direction = FaceDirection.RIGHT

        self.is_walking = (dx != 0) or (dy != 0)
