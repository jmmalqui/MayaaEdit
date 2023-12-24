import pygame as pg

from mayaa.ui.ui_manager import UIManager


class Screen:
    def __init__(self, screen_id, screen_manager) -> None:
        self.screen_id: int = screen_id
        self.screen_manager: ScreenManager = screen_manager
        self.core = self.screen_manager.core
        self.key_mapper = self.screen_manager.key_mapper
        self.window_size: pg.Vector2 = self.core.window_size
        self.font_manager = self.screen_manager.font_manager
        self.event_system = self.screen_manager.event_system
        self.surface: pg.Surface = self.core.display
        self.ui_manager: UIManager = UIManager(self)
        self.screen_manager.add_screen(self)

    def go_to(self, screen_id):
        self.screen_manager.last_screen_id = (
            self.screen_manager.current_screen.screen_id
        )
        self.screen_manager.go_to(screen_id)

    def subscribe(self, event_name, callback):
        self.screen_manager.event_system.subscribe(
            event_name=event_name, callback=callback
        )

    def emit(self, event_name, data):
        self.screen_manager.event_system.emit(event_name, data)

    def get_events(self):
        return self.screen_manager.get_events()

    def update(self):
        ...

    def render(self):
        ...

    def screen_update(self):
        self.update()
        self.ui_manager.update()

    def screen_render(self):
        self.render()
        self.ui_manager.render()


class ScreenManager:
    def __init__(self, core) -> None:
        from mayaa.core.core import Core

        self.core: Core = core
        self.event_system = self.core.event_system
        self.font_manager = self.core.font_manager
        self.screen_dict = {}
        self.current_screen: Screen = None
        self.key_mapper = self.core.key_mapper
        self.last_screen_id = None

    def get_events(self):
        return self.core.pygame_event_system.get_events()

    def get_screen_by_id(self, screen_id):
        return self.screen_dict[screen_id]

    def set_initial_screen(self, screen_id):
        self.current_screen = self.get_screen_by_id(screen_id)

    def add_screen(self, screen_object: Screen):
        self.screen_dict[screen_object.screen_id] = screen_object

    def go_to(self, scene_id):
        self.current_screen = self.get_screen_by_id(scene_id)

    def update(self):
        self.current_screen.screen_update()

    def render(self):
        self.current_screen.screen_render()
