import mayaa
import pygame as pg


class WhiteButton(mayaa.ui.Properties):
    width = 300
    height = 400
    color = "white"
    background_color = [244, 122, 32]


class WhiteButtonBlackText(WhiteButton):
    color = "black"


class MyBodyProps(mayaa.ui.Properties):
    background_color = [20, 120, 20]


class MyBodyPropsWhiteBG(MyBodyProps):
    background_color = [50, 50, 50]


def make_radial(color, x, y, idk=10):
    store_x = x
    store_y = y
    someconstant = min(x, y)
    ratio = int(someconstant // idk)
    if ratio % 2 == 0:
        ratio += 1
    x = ratio
    y = ratio
    surface = pg.Surface([x, y], pg.SRCALPHA)
    for _x in range(x):
        for _y in range(y):
            alpha = min(
                255,
                int(255 * ((_x - x // 2) ** 2 + (_y - y // 2) ** 2) / ((x // 2) ** 2)),
            )
            surface.set_at([_x, _y], [*color, 255 - alpha])
    surface = pg.transform.smoothscale(surface, [store_x, store_y])
    # pg.draw.rect(surface, "green", surface.get_rect(), 1)
    return surface


class Layer1(mayaa.ui.UILayer):
    def __init__(self, manager) -> None:
        super().__init__(manager)
        self.set_active_state(False)
        self.inject_body_properties(MyBodyProps)
        self.event_system.subscribe("PRINTHELLO", lambda data: self.printhello(data))
        self.mock_surf = make_radial([255, 0, 255], 400, 400, 5)
        self.mock_surf2 = make_radial([255, 0, 0], 400, 400, 5)
        self.mock_surf3 = make_radial([0, 255, 0], 400, 400, 5)
        self.mock_surf4 = make_radial([0, 0, 255], 400, 400, 5)

        self.osaka = pg.image.load("osaka.jpeg").convert_alpha()
        self.osaka = pg.transform.smoothscale(self.osaka, [400, 400])
        self.mock_surf.blit(self.osaka, [0, 0], special_flags=pg.BLEND_MAX)
        self.mock_surf2.blit(self.osaka, [0, 0], special_flags=pg.BLEND_MAX)
        self.mock_surf3.blit(self.osaka, [0, 0], special_flags=pg.BLEND_MAX)
        self.mock_surf4.blit(self.osaka, [0, 0], special_flags=pg.BLEND_MAX)
        self.mock_surf = pg.transform.average_surfaces(
            [self.mock_surf2, self.mock_surf3, self.mock_surf3, self.mock_surf4],
            palette_colors=True,
        )
        self.mock_surf = pg.transform.box_blur(self.mock_surf2, 100, True)
        self.mock_surf = pg.transform.laplacian(self.mock_surf)
        self.mock_surfcopy = self.mock_surf.copy()
        self.a = 0
        self.testsurface = pg.Surface([200, 50], pg.SRCALPHA)
        self.font = pg.font.SysFont("mono", 30, True)
        self.text = self.font.render("Sample Text", True, "orange")

    def printhello(self, data):
        print(data)

    def render(self):
        pg.draw.rect(self.testsurface, "blue", self.testsurface.get_rect(), 0, 25)
        self.testsurface.blit(self.text, [0, 0], special_flags=pg.BLEND_RGB_ADD)
        self.surface.blit(self.testsurface, [50, 50])


class ListTest:
    def __init__(
        self,
        layer: mayaa.ui.UILayer,
        width,
        height,
        title,
        elements: list["str"],
    ) -> None:
        self.layer = layer
        self.layer.event_system.subscribe(
            mayaa.event.GUIEvent.LEFTMOUSEDOWN, lambda data: self.open_list(data)
        )
        self.font = pg.font.SysFont("Arial", 12)
        self.elements = elements
        self.width = width
        self.height = height
        self.title = self.font.render(title, True, "yellow")
        self.text_surfaces = [
            self.font.render(f"{e}", "True", "white") for e in self.elements
        ]
        surface_height = sum([e.get_height() for e in self.text_surfaces]) + self.height
        self.surface = pg.Surface([width, surface_height], flags=pg.SRCALPHA)
        self.surface.fill([30, 30, 30])
        self.surface.blit(self.title, [5, 5])
        self.accum = self.height
        for t in self.text_surfaces:
            self.surface.fill([40, 40, 40], [0, self.accum, self.width, t.get_height()])
            self.surface.blit(t, [0, self.accum])
            self.accum += t.get_height()
        self.animation = mayaa.animation.Animation()
        self.showable_height = mayaa.animation.DynamicObject(self.animation, height)
        self.open = False

    def open_list(self, data):
        self.open = not self.open
        if self.open:
            self.showable_height.go_to(
                self.accum, 40, mayaa.animation.EasingFunctions.EASE_IN_OUT_SINE
            )
        else:
            self.showable_height.go_to(
                self.height, 40, mayaa.animation.EasingFunctions.EASE_IN_OUT_SINE
            )

    def update(self):
        self.animation.update()

    def render(self, surface, pos):
        renderable_area = self.surface.subsurface(
            [0, 0, self.width, self.showable_height.get_value()]
        )
        surface.blit(renderable_area, pos)


def rotate_center(surface, degree):
    ...


class Layer2(mayaa.ui.UILayer):
    def __init__(self, manager) -> None:
        super().__init__(manager)
        self.set_active_state(True)
        self.inject_body_properties(MyBodyPropsWhiteBG)
        # self.hellomaya = mayaa.ui.UIObject(self, content=mayaa.ui.Text("Hello maya"))
        self.test = ListTest(
            self,
            200,
            25,
            "pg.time ",
            pg.time.__dict__,
        )
        self.fonts = ListTest(
            self,
            200,
            25,
            "pg.surface ",
            pg.surface.__dict__,
        )
        self.image = ListTest(
            self,
            200,
            25,
            "pg.image ",
            pg.image.__dict__,
        )

        self.transform = ListTest(
            self,
            200,
            25,
            "pg.transform ",
            pg.transform.__dict__,
        )
        self.threads = ListTest(
            self,
            200,
            25,
            "pg.threads ",
            pg.threads.__dict__,
        )

    def update(self):
        self.test.update()
        self.fonts.update()
        self.image.update()
        self.transform.update()
        self.threads.update()

    def render(self):
        self.test.render(self.surface, [20, 20])
        self.fonts.render(self.surface, [220, 20])
        self.image.render(self.surface, [420, 20])
        self.transform.render(self.surface, [620, 20])
        self.threads.render(self.surface, [820, 20])


class Layer3(mayaa.ui.UILayer):
    def __init__(self, manager) -> None:
        super().__init__(manager)

    def render(self):
        mayaa.draw.rect(
            self.surface,
            [0, 0, 20],
            [self.window_size.x // 2 - 250, self.window_size.y // 2 - 50, 500, 100],
            0,
        )
        mayaa.draw.rect(
            self.surface,
            [0, 0, 250],
            [self.window_size.x // 2 - 250, self.window_size.y // 2 - 50, 500, 100],
            1,
        )


class DefScreen(mayaa.screen.Screen):
    def __init__(self, screen_id, screen_manager) -> None:
        super().__init__(screen_id, screen_manager)
        self.layer1 = Layer1(self.ui_manager)
        self.layer2 = Layer2(self.ui_manager)
        self.layer3 = Layer3(self.ui_manager)

    def update(self):
        mayaa.pygame_backend.display.set_caption(f"{self.core.clock.get_fps() :.1f}")
        for e in self.get_events():
            if e.type == mayaa.pygame_backend.KEYDOWN:
                if e.key == mayaa.pygame_backend.K_UP:
                    self.ui_manager.highest_renderable_z_order += 1
                if e.key == mayaa.pygame_backend.K_DOWN:
                    self.ui_manager.highest_renderable_z_order -= 1
                self.ui_manager.highest_renderable_z_order = max(
                    0, self.ui_manager.highest_renderable_z_order
                )

    def render(self):
        self.surface.fill("black")
        return super().render()


class App(mayaa.core.Core):
    def __init__(self, win_size, win_name: str) -> None:
        super().__init__(win_size, win_name)
        self.screen = DefScreen("def", self.screen_manager)
        self.screen_manager.set_initial_screen("def")


if __name__ == "__main__":
    app = App([320 * 3, 180 * 3], "layer test")
    app.run()
