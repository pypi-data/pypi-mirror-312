import abc

class ViewBuilder(abc.ABC):
    def __init__(self, session):
        self._session = session

    @abc.abstractmethod
    def fetch(self, id: str):
        pass

class QueryFacade():
    def __init__(self, s: ViewBuilder = None):
        self._session = s

    def register(self, view_builder: ViewBuilder):
        self._view_builder = view_builder

    def fetch(self, id: str):
        print("OK")
