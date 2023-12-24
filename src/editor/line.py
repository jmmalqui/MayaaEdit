import mayaa
import random


class Line:
    def __init__(self, master) -> None:
        self.master = master
        self.buffer = []
        self.text_surface: mayaa.pygame_backend.Surface = self.master.font.render(
            f"{''.join(self.buffer)}", "True", [255, 255, 255]
        )
        highlight = mayaa.surf.Surface(
            self.text_surface.get_size(), mayaa.pygame_backend.SRCALPHA
        )
        highlight.fill(
            [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        )
        self.text_surface.blit(
            highlight, [0, 0], special_flags=mayaa.pygame_backend.BLEND_MULT
        )

    def update_text_dimensions(self):
        self.text_surface = self.master.font.render(
            f"{''.join(self.buffer)}", "True", [255, 255, 255]
        )
        highlight = mayaa.surf.Surface(
            self.text_surface.get_size(), mayaa.pygame_backend.SRCALPHA
        )
        highlight.fill(
            [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        )
        self.text_surface.blit(
            highlight, [0, 0], special_flags=mayaa.pygame_backend.BLEND_MULT
        )
