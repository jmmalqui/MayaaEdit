import pygame as pg


class PygameEventSystem:
    def __init__(self) -> None:
        self.event_list = []

    def pump(self, event: pg.Event):
        if event:
            self.event_list.append(event)
        else:
            self.event_list.clear()

    def get_events(self):
        return self.event_list.copy()
