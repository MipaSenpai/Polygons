from abc import ABC, abstractmethod


class BasePolygonForm(ABC):
    def __init__(self, config: dict):
        self._config = config

        self._textForms: dict = self._config.get("forms")
        self._title: str = self._textForms.get("title")
        self._messages: dict = self._config.get("messages")

    @abstractmethod
    def _onSubmit(self): pass
    
    @abstractmethod
    def _onClose(self): pass

    @abstractmethod
    def buildForm(self): pass

    @property
    def form(self): return self.buildForm()