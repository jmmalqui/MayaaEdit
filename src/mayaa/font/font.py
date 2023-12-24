import pygame as pg
import random


class FontManager:
    def __init__(self) -> None:
        font = "JetBrainsMono Nerd Font"
        self.main_font = pg.font.SysFont(font, 30)
