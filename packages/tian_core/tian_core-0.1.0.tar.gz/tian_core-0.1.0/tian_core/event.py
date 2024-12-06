from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
import inspect

class Event:
    def __init__(self):
        self.id = uuid4()
        self.timestamp = datetime.now()
        self.version = 1
        self.aggregate_type = "Event"
        self.is_valid = True

    def __repr__(self):
        return str(self.__dict__)

    def Version(self):
        return self.version

    def AggregateType(self):
        return self.aggregate_type

    def AggregateID(self):
        return self.id

    def is_valid(self):
        return self.is_valid


class EventHandler:
    def handle(self, event: Event):
        raise NotImplementedError

# Dict[Type[Event], List[Callable]]
class EventRegister:
    def __init__(self):
        self._handlers: Dict[Type[Event], List[Callable]] = {}

    def register(self, event_cls, handler):
        if event_cls not in self._handlers:
            self._handlers[event_cls] = []
        self._handlers[event_cls].append(handler)


    def get(self, event_cls):
        return self._handlers[event_cls]

    def items(self):
        return self._handlers

    def count(self):
        return len(self._handlers)

    def info(self):
        result: List[Dict[str, str]] = []
        for event_cls, handlers in self._handlers.items():
            result.append({
                "event": event_cls.__name__,
                "handlers": [handler.__name__ for handler in handlers],
            })
        return result

    def inject(self, dependencies):
        return {
            event_type: [
                inject_dependencies(handler, dependencies)
                for handler in event_handlers
            ]
            for event_type, event_handlers in self._handlers.items()
        }

def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    return lambda message: handler(message, **deps)
