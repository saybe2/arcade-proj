import arcade
from pathlib import Path
import enum


class FaceDirection(enum.Enum):
    """Facing direction for the player."""
    LEFT = 0
    RIGHT = 1


class Player(arcade.Sprite):
    def __init__(self, x: float = 100, y: float = 150, scale: float = 1.5):
        super().__init__()

        self.scale = scale
        self.speed = 300
        self.health = 100

        # Load animations
        self.idle_textures = []
        self.walking_textures = []
        self.jump_textures = []
        self.fall_textures = []

        # Load idle animation
        idle_path = Path("assets/player/anim/idle")
        if idle_path.exists():
            for i in range(10):
                frame_path = idle_path / f"{i}.png"
                if frame_path.exists():
                    self.idle_textures.append(arcade.load_texture(str(frame_path)))

        # Load walking animation
        walking_path = Path("assets/player/anim/walking")
        if walking_path.exists():
            for i in range(10):
                frame_path = walking_path / f"{i}.png"
                if frame_path.exists():
                    self.walking_textures.append(arcade.load_texture(str(frame_path)))

        # Load jump animation
        jump_path = Path("assets/player/anim/jump")
        if jump_path.exists():
            for i in range(10):
                frame_path = jump_path / f"{i}.png"
                if frame_path.exists():
                    self.jump_textures.append(arcade.load_texture(str(frame_path)))

        # Load fall animation
        fall_path = Path("assets/player/anim/fall")
        if fall_path.exists():
            for i in range(10):
                frame_path = fall_path / f"{i}.png"
                if frame_path.exists():
                    self.fall_textures.append(arcade.load_texture(str(frame_path)))

        # Set default texture
        if self.idle_textures:
            self.texture = self.idle_textures[0]
        elif self.walking_textures:
            self.texture = self.walking_textures[0]
        else:
            self.texture = arcade.make_soft_square_texture(
                32, arcade.color.BLUE, 255, 0
            )

        self.current_frame = 0
        self.frame_counter = 0.0
        self.frame_duration = 0.1

        self.is_walking = False
        self.is_jumping = False
        self.is_falling = False
        self.face_direction = FaceDirection.RIGHT

        self.center_x = x
        self.center_y = y
        self.is_alive = True

    def update_animation(self, delta_time: float = 1 / 60):
        """Update player animation based on current state."""
        self.frame_counter += delta_time

        # Determine which animation to use
        current_textures = None
        
        # Priority: jump > fall > walking > idle
        if self.is_jumping and self.jump_textures:
            current_textures = self.jump_textures
        elif self.is_falling and self.fall_textures:
            current_textures = self.fall_textures
        elif self.is_walking and self.walking_textures:
            current_textures = self.walking_textures
        elif self.idle_textures:
            current_textures = self.idle_textures
        elif self.walking_textures:
            current_textures = self.walking_textures
        
        # Update frame
        if current_textures and self.frame_counter >= self.frame_duration:
            self.frame_counter = 0.0
            self.current_frame = (self.current_frame + 1) % len(current_textures)
            
            # Apply texture with correct facing direction
            if self.face_direction == FaceDirection.RIGHT:
                self.texture = current_textures[self.current_frame]
            else:
                self.texture = current_textures[self.current_frame].flip_horizontally()

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
