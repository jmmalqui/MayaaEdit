import mayaa
from mayaa.core.core import Core
import pygame as pg

from mayaa.screen.screen import Screen
from mayaa.ui.ui_layer import UILayer


class Pause(UILayer):
    def __init__(self, manager) -> None:
        super().__init__(manager)


class DisplayOptions(UILayer):
    def __init__(self, manager) -> None:
        super().__init__(manager)


class HelloScreen(Screen):
    def __init__(self, screen_id, screen_manager) -> None:
        super().__init__(screen_id, screen_manager)
        self.title = self.font_manager.main_font.render("Hello cow", True, "white")
        self.pause = Pause(self.ui_manager)
        self.display_options = DisplayOptions(self.ui_manager)
        self.circle_size = 50
        self.subscribe("Click", lambda data: self.click(data))
        self.subscribe("CircleResize", lambda data: self.circ_res(data))
        self.subscribe("CircleCount", lambda data: self.count_circ(data))
        self.subscribe("showanother", lambda data: self.anot(data))
        self.subscribe("videoresize", lambda data: self.video(data))

        self.circles = []
        self.circcount = self.font_manager.main_font.render(
            f"Circles: {len(self.circles)}", True, "green"
        )
        self.anothersurf = pg.Surface(self.surface.get_size(), pg.SRCALPHA)
        self.anotherrender = False

    def video(self, data):
        self.anothersurf = pg.Surface(self.surface.get_size(), pg.SRCALPHA)

    def anot(self, data):
        self.anotherrender = not self.anotherrender

    def count_circ(self, data):
        self.circcount = self.font_manager.main_font.render(
            f"Circles: {len(self.circles)}", True, "green"
        )

    def circ_res(self, data):
        self.circle_size += data * 8

    def click(self, data):
        self.circles.append([data["pos"], self.circle_size])

    def _render(self):
        self.surface.fill([20, 20, 20])

        self.anothersurf.fill([200, 200, 200, 20])

        self.title = self.font_manager.main_font.render(
            f"{self.ui_manager.layers}", True, "white"
        )
        self.surface.blit(self.title, [10, 10])
        for c in self.circles:
            pg.draw.circle(self.anothersurf, [200, 200, 200], c[0], c[1], 0)
        pg.draw.circle(
            self.surface, [200, 100, 200], pg.mouse.get_pos(), self.circle_size, 5
        )
        if self.anotherrender:
            self.surface.blit(self.anothersurf, [0, 0])
        self.surface.blit(self.circcount, [20, 50])
        return super()._render()

    def _update(self):
        for event in self.get_events():
            if event.type == pg.MOUSEMOTION:
                if event.buttons[0]:
                    self.emit("Click", event.dict)
                    self.emit("CircleCount", None)
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.emit("showanother", None)
            if event.type == pg.MOUSEWHEEL:
                self.emit("CircleResize", event.y)
            if event.type == pg.VIDEORESIZE:
                self.emit("videoresize", event.size)


class OptionsScreen(Screen):
    def __init__(self, screen_id, screen_manager) -> None:
        super().__init__(screen_id, screen_manager)

    def _render(self):
        self.surface.fill("white")
        return super()._render()


class App(Core):
    def __init__(self, win_size, win_name: str) -> None:
        super().__init__(win_size, win_name)
        self.hello_screen = HelloScreen("hello", self.screen_manager)
        self.options_screen = OptionsScreen("options", self.screen_manager)
        self.screen_manager.set_initial_screen("hello")

    def render(self):
        return super().render()


if __name__ == "__main__":
    app = App([400, 400], "mayaa app")
    app.run()
