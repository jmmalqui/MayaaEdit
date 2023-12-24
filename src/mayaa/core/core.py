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
        pg.key.set_repeat(500, 50)

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

            if event.type == pg.TEXTINPUT:
                self.event_system.emit(GUIEvent.TEXTINPUT, event.text)
            if event.type == pg.KEYDOWN:
                if event.key == 8:
                    self.event_system.emit(GUIEvent.TEXTERASE, None)
                if event.key == pg.K_LEFT:
                    self.event_system.emit(GUIEvent.TEXTCURSORLEFT, None)
                    self.event_system.emit(GUIEvent.LEFTKEY, None)
                if event.key == pg.K_UP:
                    self.event_system.emit(GUIEvent.LINEUP, None)
                if event.key == pg.K_DOWN:
                    self.event_system.emit(GUIEvent.LINEDOWN, None)
                if event.key == pg.K_RIGHT:
                    self.event_system.emit(GUIEvent.TEXTCURSORRIGHT, None)
                    self.event_system.emit(GUIEvent.RIGHTKEY, None)
                if event.key == pg.K_RETURN:
                    self.event_system.emit(GUIEvent.RETURN, None)
                if event.mod == 64 and event.key == pg.K_LEFT:
                    self.event_system.emit(GUIEvent.MOVEBYWORDLEFT, None)
                if event.mod == 64 and event.key == pg.K_RIGHT:
                    self.event_system.emit(GUIEvent.MOVEBYWORDRIGHT, None)
                if event.mod == 64 and event.key == pg.K_MINUS:
                    self.event_system.emit(GUIEvent.RESIZEDOWN, None)
                if event.mod == 66 and event.key == 59:
                    self.event_system.emit(GUIEvent.RESIZEUP, None)
            if event.type == pg.DROPFILE:
                self.event_system.emit(GUIEvent.DROPFILE, event)
            if event.type == pg.MOUSEWHEEL:
                self.event_system.emit(GUIEvent.WHEEL, event)

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
