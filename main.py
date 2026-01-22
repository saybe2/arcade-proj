import arcade

from game.config import SCREEN_HEIGHT, SCREEN_TITLE, SCREEN_WIDTH
from game.state_manager import StateManager


class PhysicsPlayWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.state_manager = StateManager(self)

    def setup(self):
        self.state_manager.show_menu()


def main():
    window = PhysicsPlayWindow()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
