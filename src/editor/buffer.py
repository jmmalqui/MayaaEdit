import time
from editor.states import EditorStates

import mayaa
from mayaa.event import GUIEvent
from editor.line import Line


class Buffer:
    def __init__(self, screen: mayaa.screen.Screen, text, position) -> None:
        self.screen = screen
        self.text = text
        self.position = mayaa.pygame_backend.Vector2([self.screen.ftreediv, 0])

        self.font = self.screen.core.font.font_type
        self.line_size = self.screen.core.font.line_size
        self.surface = self.make_surface()
        self.screen.subscribe(GUIEvent.FONTRESIZE, lambda data: self.resize(data))
        self.screen.subscribe(GUIEvent.TEXTINPUT, lambda data: self.add_text(data))
        self.screen.subscribe(
            GUIEvent.TEXTERASE, lambda data: self.erase_last_char(data)
        )
        self.screen.subscribe(
            GUIEvent.TEXTCURSORLEFT, lambda data: self.move_cursor_left(data)
        )
        self.screen.subscribe(
            GUIEvent.TEXTCURSORRIGHT, lambda data: self.move_cursor_right(data)
        )
        self.screen.subscribe(GUIEvent.RETURN, lambda data: self.add_line(data))
        self.screen.subscribe(GUIEvent.LINEUP, lambda data: self.moveup(data))
        self.screen.subscribe(GUIEvent.LINEDOWN, lambda data: self.movedown(data))

        self.screen.subscribe(
            GUIEvent.MOVEBYWORDLEFT, lambda data: self.movebyword_left(data)
        )
        self.screen.subscribe(
            GUIEvent.MOVEBYWORDRIGHT, lambda data: self.movebyword_right(data)
        )
        self.screen.subscribe(
            GUIEvent.VIDEORESIZE, lambda data: self.resize_screen(data)
        )

        self.screen.subscribe(GUIEvent.DROPFILE, lambda data: self.load_dropfile(data))
        self.screen.subscribe(GUIEvent.WHEEL, lambda data: self.mousemovement(data))
        self.screen.subscribe(GUIEvent.OPENFILE, lambda data: self.load_file(data))
        self.lines = [Line(self)]
        self.current_file = None
        self.active_line = 0
        self.pointer = 0
        self.buffer = self.lines[self.active_line].buffer
        self.metrics = mayaa.pygame_backend.Font.metrics(
            self.font, "".join(self.buffer)
        )
        self.pointer_pos = 0
        self.renderable_line_num = self.surface.get_height() // self.font.get_linesize()
        self.lineoffset = 0

    def make_surface(self):
        return mayaa.surf.Surface(
            [
                self.screen.window_size.x - self.screen.ftreediv,
                self.screen.window_size.y - self.screen.core.font.line_size,
            ],
            mayaa.pygame_backend.SRCALPHA,
        )

    def mousemovement(self, data):
        if data.y == 0:
            return
        self.lineoffset -= int(data.y / abs(data.y))
        self.lineoffset = max(0, self.lineoffset)

    def load_dropfile(self, data):
        self.current_file = data.file
        self.lines = self.load_file(data.file)

    def load_file(self, data):
        start = time.time()
        linelist = []
        filepath = data
        self.current_file = data
        with open(filepath) as file:
            for line in file.readlines():
                line_struct = Line(self)
                line_struct.buffer = list(line)
                line_struct.update_text_dimensions()
                linelist.append(line_struct)
        print(f"File read in {time.time() - start}")
        self.lines = linelist

    def resize(self, data):
        self.surface = self.make_surface()
        self.font = data.font_type
        self.line_size = data.line_size
        for line in self.lines:
            line.update_text_dimensions()
        self.renderable_line_num = self.surface.get_height() // self.line_size

    def resize_screen(self, data):
        self.surface = self.make_surface()
        self.renderable_line_num = self.surface.get_height() // self.line_size

    def movebyword_left(self, data):
        pointer_copy = self.pointer
        while True:
            if pointer_copy == 0:
                break
            if self.buffer[pointer_copy - 1].isalpha() == False:
                break
            pointer_copy -= 1

        self.pointer = pointer_copy
        self.update_pointer_pos()

    def movebyword_right(self, data):
        pointer_copy = self.pointer
        buffer_len = len(self.buffer)
        if pointer_copy >= buffer_len + 1:
            return
        if self.buffer[pointer_copy - 1].isalpha() == False:
            pointer_copy += 1

        while True:
            if pointer_copy == buffer_len:
                break
            if self.buffer[pointer_copy - 1].isalpha() == False:
                pointer_copy -= 1
                break
            pointer_copy += 1

        self.pointer = pointer_copy
        self.update_pointer_pos()

    def moveup(self, data):
        self.active_line -= 1
        if self.active_line < 0:
            self.active_line = 0
        if self.active_line < self.lineoffset:
            self.lineoffset -= 1
        self.get_buffer_from_active_line()
        self.metrics = mayaa.pygame_backend.Font.metrics(
            self.font, "".join(self.buffer)
        )
        if self.pointer > len(self.buffer):
            self.pointer = len(self.buffer)
        self.update_pointer_pos()

    def movedown(self, data):
        self.active_line += 1
        if self.active_line > len(self.lines) - 1:
            self.active_line -= 1
        if self.active_line > self.lineoffset + self.renderable_line_num - 1:
            self.lineoffset += 1
        self.get_buffer_from_active_line()
        self.metrics = mayaa.pygame_backend.Font.metrics(
            self.font, "".join(self.buffer)
        )
        self.update_pointer_pos()

    def add_line(self, data):
        self.lines[self.active_line].buffer = self.buffer[: self.pointer]
        self.lines[self.active_line].text_surface = self.font.render(
            f"{''.join(self.buffer[:self.pointer])}", "True", [100, 250, 150]
        )
        self.lines.insert(self.active_line + 1, Line(self))
        self.active_line += 1
        if self.active_line > self.lineoffset + self.renderable_line_num - 1:
            self.lineoffset += 1
        self.lines[self.active_line].buffer = self.buffer[self.pointer :]
        self.get_buffer_from_active_line()
        self.burn_textsurface_into_line_struct()
        self.pointer = 0
        self.pointer_pos = 0

    def get_buffer_from_active_line(self):
        self.buffer = self.lines[self.active_line].buffer

    def move_cursor_left(self, data):
        if self.pointer == 0 and self.active_line != 0:
            self.active_line -= 1
            self.pointer = len(self.lines[self.active_line].buffer)
            self.get_buffer_from_active_line()
            self.metrics = mayaa.pygame_backend.Font.metrics(
                self.font, "".join(self.buffer)
            )
            self.update_pointer_pos()
            return
        self.pointer -= 1

        self.metrics = mayaa.pygame_backend.Font.metrics(
            self.font, "".join(self.buffer)
        )
        self.update_pointer_pos()

    def move_cursor_right(self, data):
        if (
            self.pointer == len(self.lines[self.active_line].buffer)
            and self.active_line != len(self.lines) - 1
        ):
            self.active_line += 1
            self.pointer = 0
            self.get_buffer_from_active_line()
            self.metrics = mayaa.pygame_backend.Font.metrics(
                self.font, "".join(self.buffer)
            )
            self.update_pointer_pos()
            return
        self.pointer += 1
        bufferlen = len(self.buffer)
        if self.pointer > bufferlen:
            self.pointer -= 1
        self.metrics = mayaa.pygame_backend.Font.metrics(
            self.font, "".join(self.buffer)
        )
        self.update_pointer_pos()

    def erase_last_char(self, data):
        if self.screen.current_state == EditorStates.NORMAL:
            return
        if self.active_line == 0:
            if self.pointer == 0:
                return
        if self.pointer == 0:
            buffercopy = self.lines[self.active_line].buffer.copy()
            self.lines.pop(self.active_line)
            self.active_line -= 1
            if self.active_line < self.lineoffset:
                self.lineoffset -= 1
            self.pointer = len(self.lines[self.active_line].buffer)
            self.lines[self.active_line].buffer.extend(buffercopy)
            self.get_buffer_from_active_line()
            self.metrics = mayaa.pygame_backend.Font.metrics(
                self.font, "".join(self.buffer)
            )
            self.update_pointer_pos()
            self.burn_textsurface_into_line_struct()
            return
        if len(self.buffer) == 0:
            if self.pointer == 0:
                self.lines.pop(self.active_line)
                self.active_line -= 1
                return
        if len(self.buffer) != 0 and self.pointer > 0:
            self.buffer.pop(self.pointer - 1)
            self.pointer -= 1
            self.metrics = mayaa.pygame_backend.Font.metrics(
                self.font, "".join(self.buffer)
            )
            self.update_pointer_pos()
            self.burn_textsurface_into_line_struct()
            return

    def burn_textsurface_into_line_struct(self):
        self.lines[self.active_line].text_surface = self.font.render(
            f"{''.join(self.buffer)}", "True", [100, 250, 150]
        )

    def add_text(self, data):
        if self.screen.current_state == EditorStates.NORMAL:
            return
        self.buffer.insert(self.pointer, data)
        self.metrics = mayaa.pygame_backend.Font.metrics(
            self.font, "".join(self.buffer)
        )
        self.pointer += 1
        self.update_pointer_pos()
        self.burn_textsurface_into_line_struct()

    def update_pointer_pos(self):
        self.pointer_pos = sum([a[4] for a in self.metrics[: self.pointer]])

    def render(self):
        mayaa.pygame_backend.key.set_text_input_rect(
            [*self.position, *self.surface.get_size()]
        )
        self.surface.fill([20, 20, 20])

        self.draw_lines()
        self.draw_cursor()
        self.screen.surface.blit(self.surface, self.position)

    def draw_lines(self):
        accum = 0
        for index, line in enumerate(
            self.lines[self.lineoffset : self.lineoffset + self.renderable_line_num]
        ):
            real_index = self.lineoffset + index
            linenum = self.font.render(f"{real_index}", True, [100, 200, 100])
            if real_index == self.active_line:
                mayaa.draw.rect(
                    self.surface,
                    [60, 60, 70],
                    [
                        0,
                        accum,
                        self.surface.get_size()[0],
                        linenum.get_height(),
                    ],
                    0,
                )
                linenum = self.font.render(f"{real_index}", True, [100, 200, 200])

            self.surface.blit(
                linenum,
                [
                    70 - linenum.get_width(),
                    accum,
                ],
            )
            self.surface.blit(
                line.text_surface,
                [90, accum],
            )
            accum += line.text_surface.get_height()

    def draw_cursor(self):
        mayaa.draw.rect(
            self.surface,
            "white",
            [
                90 + self.pointer_pos,
                (self.active_line - self.lineoffset) * self.line_size,
                1,
                self.line_size,
            ],
            1,
        )
