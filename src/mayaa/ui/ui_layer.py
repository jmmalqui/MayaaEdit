from mayaa.flag.display import DisplayMode
from mayaa.ui.ui_object import Properties

"""

This is getting messy, clean later!!!

"""


class BodyProps(Properties):
    background_color = "black"


class UILayer:
    def __init__(self, manager) -> None:
        from mayaa.ui.ui_manager import UIManager
        from mayaa.ui.ui_object import UIObject

        self.properties = BodyProps()
        self.z_id = 0
        self.manager: UIManager = manager
        self.manager.add_layer(self)
        self.ui_objects: list[UIObject] = []

        self.key_mapper = self.manager.key_mapper
        self.event_system = self.manager.event_system
        self.window_size = self.manager.window_size
        self.surface = self.manager.surface
        self.active = False
        self.focus = False

    def inject_body_properties(self, properties: Properties):
        self.properties = properties

    def add_ui_object(self, ui_object):
        self.ui_objects.append(ui_object)

    def set_active_state(self, state: bool):
        """Sets whether the layer should be rendered or not"""
        self.active = state
        if self.manager.highest_renderable_z_order < self.z_id:
            self.manager.highest_renderable_z_order = self.z_id

    def set_z_id(self, z_id: int):
        self.z_id = z_id

    def layer_update(self):
        for ui_object in self.ui_objects:
            ...
        self.update()

    def render_ui_objects(self):
        rendering_style = self.properties.display
        if rendering_style == None:
            for object in self.ui_objects:
                ...

    def layer_render(self):
        self.surface.fill(self.properties.background_color)
        self.render_ui_objects()
        self.render()

    def update(self):
        ...

    def render(self):
        ...
