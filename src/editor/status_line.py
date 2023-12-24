import mayaa
from mayaa.event import GUIEvent
from editor.states import EditorStates


class StatusLine:
    def __init__(self, screen: mayaa.screen.Screen) -> None:
        self.screen = screen
        self.font = self.screen.core.font.font_type
        self.line_size = self.screen.core.font.line_size
        self.status: EditorStates = self.screen.current_state
        self.status_text = self.font.render(f"--{self.status.name}--", True, "white")
        self.surface = mayaa.surf.Surface(
            [self.screen.window_size.x, self.screen.core.font.line_size],
            mayaa.pygame_backend.SRCALPHA,
        )
        self.screen.subscribe(GUIEvent.VIDEORESIZE, lambda data: self.resize(data))
        self.screen.subscribe(GUIEvent.FONTRESIZE, lambda data: self.resize_font(data))

    def update_status(self):
        self.status: EditorStates = self.screen.current_state
        self.status_text = self.font.render(f"--{self.status.name}--", True, "white")

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

    def resize(self, data):
        self.surface = mayaa.surf.Surface(
            [self.screen.window_size.x, self.line_size],
            mayaa.pygame_backend.SRCALPHA,
        )

    def render(self):
        self.surface.fill([30, 30, 30])
        self.surface.blit(self.status_text, [0, 0])
        self.screen.surface.blit(
            self.surface,
            [0, self.screen.window_size.y - self.surface.get_height()],
        )
