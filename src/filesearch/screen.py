import os
import mayaa
from mayaa.event import GUIEvent


"""
G+H: Go to Help Page 
ESC: Go back to Editor
RIGHTARROW: Go One Level Deeper 
LEFTARROW: Go One Level Higher
UPARROW: Move up
DOWNARROW: Move down 
SF: Select File
RF: Rename File 
AF: Add File
DF: Delete File
CF: Copy File 
XF: Cut File 
"""


class FileSearch(mayaa.screen.Screen):
    def __init__(self, screen_id, screen_manager) -> None:
        super().__init__(screen_id, screen_manager)
        self.subscribe(GUIEvent.GOBACKSCREEN, lambda data: self.go_back_to_editor(data))
        self.subscribe(GUIEvent.LINEUP, lambda data: self.move_up(data))
        self.subscribe(GUIEvent.LINEDOWN, lambda data: self.move_down(data))
        self.subscribe(GUIEvent.RIGHTKEY, lambda data: self.show_file_contents(data))
        self.subscribe(
            GUIEvent.LEFTKEY, lambda data: self.go_up_in_file_structure(data)
        )
        self.subscribe(GUIEvent.FONTRESIZE, lambda data: self.resize(data))
        self.subscribe(GUIEvent.RETURN, lambda data: self.load_file(data))
        self.font: mayaa.pygame_backend.Font = self.core.font.font_type
        self.line_size = self.core.font.line_size
        self.current_dir = self.core.current_dir
        self.list_dir: list = self.get_list_dir()
        self.entries: list[Entry] = self.make_entries()
        self.dir_id = 0

    def load_file(self, data):
        if self.screen_manager.current_screen.screen_id != self.screen_id:
            return
        selected_file = os.path.join(self.current_dir, self.list_dir[self.dir_id])
        if os.path.isdir(selected_file):
            return
        self.emit(GUIEvent.OPENFILE, selected_file)
        self.go_to("editor")

    def show_file_contents(self, data):
        current_dir_safe_copy = self.current_dir, self.list_dir
        join_path = os.path.join(self.current_dir, self.list_dir[self.dir_id])
        self.current_dir = join_path
        self.list_dir = self.get_list_dir()
        if self.list_dir is False:
            self.current_dir = current_dir_safe_copy[0]
            self.list_dir = current_dir_safe_copy[1]
            return
        self.entries: list[Entry] = self.make_entries()
        self.dir_id = 0

    def go_up_in_file_structure(self, data):
        current_dir_safe_copy = self.current_dir, self.list_dir
        print(self.current_dir)

        self.current_dir = os.path.abspath(os.path.join(self.current_dir, os.pardir))
        print(self.current_dir)
        self.list_dir = self.get_list_dir()
        if self.list_dir is False:
            self.current_dir = current_dir_safe_copy[0]
            self.list_dir = current_dir_safe_copy[1]
            return
        self.entries: list[Entry] = self.make_entries()
        self.dir_id = 0

    def resize(self, data):
        self.font = data.font_type
        self.line_size = data.line_size
        self.entries = self.make_entries()

    def make_entries(self):
        entries = []
        for directory in self.list_dir:
            entry = Entry(self, directory)
            entry.color = "white"
            entry.text_surface = self.font.render(
                f"{entry.path}", True, entry.color, None
            )
            entries.append(entry)
        return entries

    def move_up(self, data):
        if self.screen_manager.current_screen.screen_id != self.screen_id:
            return

        self.dir_id -= 1
        if self.dir_id < 0:
            self.dir_id = len(self.list_dir) - 1

    def move_down(self, data):
        if self.screen_manager.current_screen.screen_id != self.screen_id:
            return
        self.dir_id += 1
        if self.dir_id >= len(self.list_dir):
            self.dir_id = 0

    def get_list_dir(self):
        if os.path.isdir(self.current_dir):
            return os.listdir(self.current_dir)
        else:
            return False

    def go_back_to_editor(self, data):
        print(self.screen_id, self.screen_manager.current_screen.screen_id)
        if self.screen_manager.current_screen.screen_id == self.screen_id:
            self.screen_manager.go_to(self.screen_manager.last_screen_id)

    def render(self):
        self.surface.fill([30, 30, 30])
        mayaa.draw.rect(
            self.surface,
            [40, 40, 40],
            [0, self.dir_id * self.line_size, self.window_size.x, self.line_size],
            0,
        )
        mayaa.draw.rect(
            self.surface,
            [60, 60, 60],
            [0, self.dir_id * self.line_size, self.window_size.x, self.line_size],
            2,
        )

        accum = 0
        for entry in self.entries:
            self.surface.blit(entry.text_surface, [0, accum])
            accum += self.line_size
        return super().render()


class Entry:
    def __init__(self, filesearch: FileSearch, path) -> None:
        self.filesearch = filesearch
        self.path = path
        self.text_surface = None
