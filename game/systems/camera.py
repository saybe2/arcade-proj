import arcade

from game.config import CAMERA_PAN_SPEED

try:
    CameraClass = arcade.Camera
except AttributeError:
    from arcade.camera import Camera as CameraClass


class CameraManager:
    def __init__(self, width: int, height: int, pan_speed: float = CAMERA_PAN_SPEED):
        self.world_camera = CameraClass(width, height)
        self.hud_camera = CameraClass(width, height)
        self.pan_speed = pan_speed

    def use_world(self):
        self.world_camera.use()

    def use_hud(self):
        self.hud_camera.use()

    def update(self, target_sprite):
        if target_sprite is None:
            return
        screen_center_x = target_sprite.center_x - self.world_camera.viewport_width / 2
        screen_center_y = target_sprite.center_y - self.world_camera.viewport_height / 2
        self.world_camera.move_to((screen_center_x, screen_center_y), self.pan_speed)
