# pylint: disable=too-few-public-methods
import abc

class AbstractNotification(abc.ABC):
    @abc.abstractmethod
    def send(self, destination, message):
        raise NotImplementedError
