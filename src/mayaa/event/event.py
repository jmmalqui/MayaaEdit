class EventSystem:
    def __init__(self) -> None:
        self.event_list = {}

    def subscribe(self, event_name, callback):
        if event_name in self.event_list:
            self.event_list[event_name].append(callback)
        else:
            self.event_list[event_name] = [callback]

    def emit(self, event_name, data):
        if event_name in self.event_list:
            for callback in self.event_list[event_name]:
                callback(data)

    def unsubscribe(self, event_name):
        self.event_list.pop(event_name)
