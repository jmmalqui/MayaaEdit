import mayaa
from mayaa.event import GUIEvent
from editor.status_line import StatusLine
from editor.buffer import Buffer
from editor.states import EditorStates
from editor.filetree import FileTree


class Editor(mayaa.screen.Screen):
    def __init__(self, screen_id, screen_manager) -> None:
        super().__init__(screen_id, screen_manager)
        self.ftreediv = 240
        self.filetree = FileTree(self)
        self.buffer = Buffer(self, "Text Demo", [10, 10])
        self.current_state = EditorStates.NORMAL

        self.statusline = StatusLine(self)
        self.key_mapper.remap(
            GUIEvent.SEARCHFILE,
            [
                mayaa.pygame_backend.K_SPACE,
                mayaa.pygame_backend.K_o,
                mayaa.pygame_backend.K_f,
            ],
            None,
        )
        self.key_mapper.remap(
            GUIEvent.TRANSITIONNORMAL, [mayaa.pygame_backend.K_ESCAPE], None
        )
        self.key_mapper.remap(
            GUIEvent.TRANSITIONINSERT, [mayaa.pygame_backend.K_i], None
        )
        self.key_mapper.connect_to_event_system(self.event_system)
        self.subscribe(GUIEvent.SEARCHFILE, lambda data: self.search_for_file(data))
        self.subscribe(
            GUIEvent.TRANSITIONINSERT, lambda data: self.transition_insert(data)
        )
        self.subscribe(
            GUIEvent.TRANSITIONNORMAL, lambda data: self.transition_normal(data)
        )

    def transition_normal(self, data):
        if self.current_state == EditorStates.INSERT:
            self.current_state = EditorStates.NORMAL
            self.statusline.update_status()
        ...

    def transition_insert(self, data):
        if self.current_state == EditorStates.NORMAL:
            self.current_state = EditorStates.INSERT
            self.statusline.update_status()

    def search_for_file(self, data):
        if self.screen_manager.current_screen.screen_id != self.screen_id:
            return
        if self.current_state == EditorStates.NORMAL:
            print("OPENING FILE")
            self.go_to("filesearch")

    def render(self):
        self.surface.fill([30, 30, 30])
        self.filetree.render()
        self.buffer.render()
        self.statusline.render()
        return super().render()
