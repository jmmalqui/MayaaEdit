import mayaa
from mayaa.event import GUIEvent


class FileTree:
    def __init__(self, screen: mayaa.screen.Screen) -> None:
        self.screen = screen
        self.line_size = self.screen.core.font.line_size
        self.divider = self.screen.ftreediv
        self.surface = mayaa.pygame_backend.Surface(
            [self.divider, self.screen.window_size.y - self.line_size]
        )
        self.screen.subscribe(GUIEvent.VIDEORESIZE, lambda data: self.resize(data))
        self.screen.subscribe(GUIEvent.FONTRESIZE, lambda data: self.resize_font(data))

    def resize(self, data):
        self.surface = mayaa.surf.Surface(
            [self.divider, self.screen.window_size.y - self.line_size],
            mayaa.pygame_backend.SRCALPHA,
        )

    def resize_font(self, data):
        self.font = data.font_type
        self.line_size = data.line_size
        self.status_text = self.font.render(
            f"--{self.status.name}--{data.size}", True, "white"
        )
        self.surface = mayaa.surf.Surface(
            [self.screen.window_size.x, self.line_size],
            mayaa.pygame_backend.SRCALPHA,
        )

    def render(self):
        self.surface.fill([40, 40, 40])
        self.screen.surface.blit(self.surface, [0, 0])
