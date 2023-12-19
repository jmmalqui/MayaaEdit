import pygame as pg
import random


class FontManager:
    def __init__(self) -> None:
        font = "padaukbook"
        self.main_font = pg.font.SysFont(
            font,
            20,
        )
        print(font)
