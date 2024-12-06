from .event import Event
from .command import Command
from .unit_of_work import AbstractUnitOfWork
from typing import Callable, Dict, List, Union, Type, Any
import traceback

Message = Union[Command, Event, AbstractUnitOfWork]

class MessageBus:
    def __init__(
        self,
        event_handlers: Dict[Type[Event], List[Callable]],
        command_handlers: Dict[Type[Command], Callable],
        uows: Dict[str, AbstractUnitOfWork],
    ):
        self._event_handlers = event_handlers
        self._command_handlers = command_handlers
        self._uows = uows

    def handle(self, message: Message) -> Any:
        self.queue = [message]
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, Event):
                return self.handle_event(message)
            elif isinstance(message, Command):
                return self.handle_command(message)
            else:
                raise Exception(f"{message} was not an Event or Command")

    def handle_event(self, event: Event):
        for handler in self._event_handlers[type(event)]:
            try:
                handler(event)
                # self.queue.extend(self.uow.collect_new_events())
            except Exception:
                raise Exception(f"Error handling event {event}")

    def handle_command(self, command: Command) -> Any:
        try:
            handler = self._command_handlers.get(type(command))
            if not handler:
                raise Exception(f"No handler for {command}")

            return handler(command)
        except Exception as e:
            traceback.print_exc()
            raise Exception(f"Error handling command {command}") from e

    def print_debug(self):
        cmd_info: List[Dict[str, str]] = []
        for command, handler in self._command_handlers.items():
            cmd_info.append({
                "command": command.__name__,
                "handler": handler.__name__,
                "type": command.__type__,
                "aggregate_type": command.__aggregate_id__,
                "version": command.__version__,
                "created_by": command.__created_by__,
                "is_valid": command.__is_valid__
            })

        event_info: List[Dict[str, str]] = []
        for event, handler in self._event_handlers.items():
            event_info.append({
                "event": event.__name__,
                "handler": handler.__name__,
                "type": event.__type__,
                "aggregate_type": event.__aggregate_id__,
                "version": event.__version__,
                "created_by": event.__created_by__,
                "is_valid": event.__is_valid__
            })
        results = {
            "message": "OK",
            "commands": {
                "title": "Running Commands",
                "detail": cmd_info
            },
            "events": {
                "title": "Running Events",
                "detail":event_info
            },
            "uows": {
                "title": "Unit of Work",
                "detail": self._uows.keys()
            }
        }
        return results


    def get_repositories(self) -> List[Dict[str, Any]]:
        repositories = []
        for uow in self._uows.values():
            repositories.append(uow.get_driver().short_information())
        return repositories


