import pygame as pg
from mayaa.event.event import EventSystem


class KeyMapper:
    def __init__(self) -> None:
        self.key_buffer = []
        self.mappings = {}
        self.key_count = 0
        self.is_buffer_clearable = False
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
        self.key_buffer.append(key)
        self.key_count += 1
        self.is_buffer_clearable = True

    def execute_callback(self):
        if tuple(self.key_buffer) in self.mappings:
            for event, data in self.mappings[tuple(self.key_buffer)]:
                self.event_system.emit(event, data)

    def clear_buffer(self):
        if self.is_buffer_clearable:
            self.execute_callback()
            self.key_buffer.clear()
            self.is_buffer_clearable = False
