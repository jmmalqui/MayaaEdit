import pygame as pg
from mayaa.event.event import EventSystem


class KeyMapper:
    def __init__(self) -> None:
        self.key_buffer = []
        self.mappings = {}
        self.key_count = 0
        self.event_system: EventSystem = None

    def connect_to_event_system(self, event_system: EventSystem):
        self.event_system = event_system

    def remap(self, event, key_succesion: list, data=None):
        set_key_succesion = tuple(key_succesion)
        if set_key_succesion in self.mappings:
            self.mappings[set_key_succesion].append([event, data])
        else:
            self.mappings[set_key_succesion] = [[event, data]]

    def add_key(self, key):
        if key in [pg.K_LCTRL, pg.K_RCTRL, pg.KMOD_SHIFT, pg.K_SPACE]:
            self.key_buffer.clear()
        single_key_exec = self.execute_callback_key(key)
        if single_key_exec:
            return
        self.key_buffer.append(key)
        self.key_count += 1
        self.execute_callback()

    def execute_callback_key(self, key):
        if tuple([key]) in self.mappings:
            for event, data in self.mappings[tuple([key])]:
                self.event_system.emit(event, data)
                self.key_buffer.clear()
            return True
        else:
            return False

    def execute_callback(self):
        if tuple(self.key_buffer) in self.mappings:
            for event, data in self.mappings[tuple(self.key_buffer)]:
                self.event_system.emit(event, data)
                self.key_buffer.clear()
        else:
            return
