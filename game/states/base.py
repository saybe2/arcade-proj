import arcade


class BaseView(arcade.View):
    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
