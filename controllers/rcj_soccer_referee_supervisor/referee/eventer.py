from referee.event_handlers import EventHandler


class Eventer:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber: EventHandler):
        self.subscribers.append(subscriber)

    def event(self, *args, **kwargs):
        for subscriber in self.subscribers:
            subscriber.handle(*args, **kwargs)
