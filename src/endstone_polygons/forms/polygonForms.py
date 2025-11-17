import json

from abc import ABC, abstractmethod

from endstone import Player
from endstone.form import (
    ActionForm,
    ModalForm,
    TextInput,
    Label,
    Divider,
    Button
)


class BasePolygonForm(ABC):
    def __init__(self, config: dict):
        self.config = config
        self.title = self.config.get("forms").get("title")

    @abstractmethod
    def _onSubmit(self): pass
    
    @abstractmethod
    def _onClose(self): pass

    @abstractmethod
    def _buildForm(self): pass

    @property
    def form(self): return self._buildForm()
    

class CreatePolygonForm(BasePolygonForm):
    def _onSubmit(self, player: Player, data: str) -> None:
        namePolygon = json.loads(data)
        print(player.name, "открыл создание")
        print(namePolygon[1])

    def _onClose(self, player: Player) -> None:
        print(player.name, "закрыл создание")

    def _buildForm(self) -> ModalForm:
        textForm: dict = self.config.get("forms").get("createPolygon")

        return ModalForm(
            title=self.title,
            controls=[Label("тест2"), TextInput("тест", "")],
            on_submit=self._onSubmit,
            on_close=self._onClose
        )
    


class MenuPolygonForm(BasePolygonForm):
    def _onSubmit(self, player: Player, data: str) -> None:
        print(player.name, "открыл меню")
        print(data) # String

    def _onClose(self, player: Player) -> None:
        print(player.name, "закрыл меню")

    def _buildForm(self) -> ActionForm:
        textForm: dict = self.config.get("forms").get("menuPolygon")

        return ActionForm(
            title=self.title,
            content="test",
            buttons=[
                Button("Мои полигоны"),
                Divider(),
                Button("Удалить полигон"),
                Divider(),
                Button("Информация"),
            ],
            on_submit=self._onSubmit,
            on_close=self._onClose
        )
    

    
# delete pg
# info pg -> back button
# managment pg -> delete/add player