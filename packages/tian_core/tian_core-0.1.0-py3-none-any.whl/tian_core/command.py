from abc import ABC, abstractmethod
from typing import Dict, List, Union, Type, TYPE_CHECKING
import inspect
from typing import (Any, AnyStr, Dict, Tuple, Union)
from uuid import uuid4
from datetime import datetime
from .entity import Command


       
   
    
class CommandHandler(ABC):
    @abstractmethod
    def handle(self, command: Command):
        raise NotImplementedError

class CommandRegister:
    def __init__(self):
        self._handlers: Dict[Type[Command], CommandHandler] = {}

    def register(self, command_cls: Type[Command], handler: CommandHandler):
        self._handlers[command_cls] = handler

    def get(self, command_cls: Type[Command]) -> CommandHandler:
        return self._handlers[command_cls]

    def items(self) -> Dict[Type[Command], CommandHandler]:
        return self._handlers.items()

    def count(self):
        return len(self._handlers)

    def inject(self, dependencies) :
        return {
            command_type: inject_dependencies(handler, dependencies)
            for command_type, handler in self._handlers.items()
        }

def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    return lambda message: handler(message, **deps)
