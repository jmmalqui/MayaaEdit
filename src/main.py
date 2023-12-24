import os
from filesearch.screen import FileSearch
import mayaa
from editor.screen import Editor
from mayaa.event import GUIEvent


class AppFont:
    def __init__(self, fontname, fontsize) -> None:
        self.name = fontname
        self.size = fontsize
        self.font_type = mayaa.pygame_backend.font.SysFont(self.name, self.size)
        self.line_size = self.font_type.get_linesize()

    def update_font(self):
        self.font_type = mayaa.pygame_backend.font.SysFont(self.name, self.size)
        self.line_size = self.font_type.get_linesize()


class MayaaEdit(mayaa.core.Core):
    def __init__(self, win_size, win_name: str) -> None:
        super().__init__(win_size, win_name)
        self.current_dir = os.getcwd()

        self.font = AppFont("JetBrainsMono Nerd Font", 30)

        self.key_mapper.remap(
            GUIEvent.GOBACKSCREEN, [mayaa.pygame_backend.K_ESCAPE], None
        )
        self.key_mapper.connect_to_event_system(self.event_system)
        self.editor = Editor("editor", self.screen_manager)
        self.filesearch = FileSearch("filesearch", self.screen_manager)
        self.screen_manager.set_initial_screen("editor")
        self.fps = 6000

        self.event_system.subscribe(
            GUIEvent.RESIZEDOWN, lambda data: self.resize_font_down(data)
        )
        self.event_system.subscribe(
            GUIEvent.RESIZEUP, lambda data: self.resize_font_up(data)
        )

    def resize_font_down(self, data):
        self.font.size -= 5
        self.font.size = max(10, self.font.size)
        self.font.update_font()

        self.event_system.emit(GUIEvent.FONTRESIZE, self.font)

    def resize_font_up(self, data):
        self.font.size += 5
        self.font.size = min(100, self.font.size)
        self.font.update_font()
        self.event_system.emit(GUIEvent.FONTRESIZE, self.font)

    def render_key_buffer(self):
        text = self.font.font_type.render(
            f"FPS: {self.clock.get_fps():.1f} ", True, "white"
        )
        self.display.blit(
            text,
            [
                self.window_size.x - text.get_width(),
                0,
            ],
        )

    def render(self):
        self.render_key_buffer()
        return super().render()


if __name__ == "__main__":
    app = MayaaEdit([320 * 3, 180 * 3], "MayaaEdit")
    app.run()
