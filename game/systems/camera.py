import arcade

from game.config import CAMERA_PAN_SPEED

try:
    CameraClass = arcade.Camera
    CAMERA_MODE = "legacy"
except AttributeError:
    from arcade.camera import Camera2D as CameraClass

    CAMERA_MODE = "camera2d"


class CameraManager:
    def __init__(
        self,
        width: int,
        height: int,
        pan_speed: float = CAMERA_PAN_SPEED,
        window=None,
    ):
        if CAMERA_MODE == "legacy":
            self.world_camera = CameraClass(width, height)
            self.hud_camera = CameraClass(width, height)
        else:
            self.world_camera = CameraClass(window=window)
            self.hud_camera = CameraClass(window=window)
        self.pan_speed = pan_speed

    def use_world(self):
        self.world_camera.use()

    def use_hud(self):
        self.hud_camera.use()

    def update(self, target_sprite):
        if target_sprite is None:
            return
        if CAMERA_MODE == "legacy":
            screen_center_x = (
                target_sprite.center_x - self.world_camera.viewport_width / 2
            )
            screen_center_y = (
                target_sprite.center_y - self.world_camera.viewport_height / 2
            )
            self.world_camera.move_to((screen_center_x, screen_center_y), self.pan_speed)
            return

        current = self.world_camera.position
        target = (target_sprite.center_x, target_sprite.center_y)
        if self.pan_speed <= 0:
            self.world_camera.position = target
            return

        new_x = current[0] + (target[0] - current[0]) * self.pan_speed
        new_y = current[1] + (target[1] - current[1]) * self.pan_speed
        self.world_camera.position = (new_x, new_y)
