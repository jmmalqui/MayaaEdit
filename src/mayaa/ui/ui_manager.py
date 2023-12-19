from mayaa.ui.ui_layer import UILayer


class UIManager:
    def __init__(self, screen) -> None:
        from mayaa.screen.screen import Screen

        self.screen: Screen = screen
        self.key_mapper = self.screen.key_mapper
        self.surface = self.screen.surface
        self.event_system = self.screen.event_system
        self.window_size = self.screen.window_size
        self.layers: list[UILayer] = []
        self.layer_count = 0
        self.highest_renderable_z_order = 0

    def add_layer(self, layer: UILayer):
        layer.set_z_id(self.layer_count)
        self.layer_count += 1
        self.layers.append(layer)

    def update(self):
        for layer in self.layers:
            if layer.active:
                layer.layer_update()

    def render(self):
        for z, layer in enumerate(self.layers):
            if z > self.highest_renderable_z_order:
                break
            layer.layer_render()
