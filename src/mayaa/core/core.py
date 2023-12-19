import pygame as pg
from mayaa.event.event import EventSystem
from mayaa.event.pygame_event import PygameEventSystem
from mayaa.font.font import FontManager
from mayaa.screen.screen import ScreenManager
from mayaa.event.gui_event import GUIEvent
from mayaa.event.key_mapper import KeyMapper


class Core:
    def __init__(self, win_size, win_name: str) -> None:
        pg.init()
        self.display = pg.display.set_mode(win_size, pg.RESIZABLE)
        self.clock = pg.Clock()
        self.window_size = pg.Vector2(win_size)
        self.fps = None
        self.background_color = [20, 20, 20]
        """ Systems """
        self.event_system = EventSystem()
        self.key_mapper = KeyMapper()
        self.key_mapper.connect_to_event_system(self.event_system)
        self.pygame_event_system = PygameEventSystem()
        """ Managers """
        self.font_manager = FontManager()
        self.screen_manager = ScreenManager(self)
        self.event_system.subscribe(
            GUIEvent.VIDEORESIZE, lambda data: self.on_videoresize(data)
        )

        pg.display.set_caption(win_name)

    def remap(self, event, key_succesion: list, data: None):
        self.key_mapper.remap(event, key_succesion, data)

    def on_videoresize(self, data):
        self.window_size.x = data.w
        self.window_size.y = data.h

    def check_events(self):
        self.pygame_event_system.pump(None)

        for event in pg.event.get():
            self.pygame_event_system.pump(event)
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.VIDEORESIZE:
                self.event_system.emit(GUIEvent.VIDEORESIZE, event)
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.event_system.emit(GUIEvent.LEFTMOUSEDOWN, event)
            if event.type == pg.KEYDOWN:
                self.key_mapper.add_key(event.key)
            if event.type == pg.KEYUP:
                self.key_mapper.clear_buffer()

    def update(self):
        ...

    def render(self):
        ...

    def _update(self):
        self.screen_manager.update()
        self.update()

    def _render(self):
        self.screen_manager.render()
        self.render()
        pg.display.flip()

    def run(self):
        while True:
            if self.fps == None:
                self.delta_time = self.clock.tick()
            else:
                self.delta_time = self.clock.tick(self.fps)
            self.check_events()
            self._update()
            self._render()
