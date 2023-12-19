import pygame as pg

from mayaa.screen.screen import Screen


class Area:
    def __init__(self, screen: Screen) -> None:
        self.ui_element_list = []
        self.size = pg.Vector2(screen.surface.get_size())
