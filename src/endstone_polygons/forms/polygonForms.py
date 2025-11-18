import json

from abc import ABC, abstractmethod

from endstone.level import Location
from endstone import Player
from endstone.form import (
    ActionForm,
    ModalForm,
    TextInput,
    Label,
    Divider,
    Button
)

from ..database.repository import PolygonRepository
from ..cache import PolygonCache


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
    def __init__(self, config: dict, dbEngine, cache: PolygonCache, location: Location):
        super().__init__(config)
        self.dbEngine = dbEngine
        self.cache = cache
        self.location = location
    
    def _onSubmit(self, player: Player, data: str) -> None:
        formData: list = json.loads(data)
        polygonName: str = formData[2]
        
        if not polygonName or polygonName.strip() == "":
            player.send_message("§cОшибка: Введите имя полигона!")
            return
        
        blockX = int(self.location.x)
        blockY = int(self.location.y)
        blockZ = int(self.location.z)
        world = self.location.dimension.name
        
        radius = 10.0
        minX = self.location.x - radius
        minZ = self.location.z - radius
        maxX = self.location.x + radius
        maxZ = self.location.z + radius
        
        with self.dbEngine as session:
            repo = PolygonRepository(session)
            
            existing = repo.getPolygonByName(polygonName)
            if existing:
                player.send_message(f"§cПолигон с именем '{polygonName}' уже существует!")
                return
                        
            polygon = repo.createPolygon(
                name=polygonName,
                owner=player.name,
                world=world,
                centerX=blockX,
                centerY=blockY,
                centerZ=blockZ,
                minX=minX,
                minZ=minZ,
                maxX=maxX,
                maxZ=maxZ
            )
            
            # Add to cache with session to properly detach
            self.cache.addPolygon(polygon, session)
            
            player.send_message(f"§aПолигон '{polygon.name}' успешно создан!")
            player.send_message(f"§7Территория: {int(radius * 2)}x{int(radius * 2)} блоков")
            player.send_message(f"§7Центр: ({blockX}, {blockY}, {blockZ})")
            
    def _onClose(self, player: Player) -> None:
        player.send_message("§7Создание полигона отменено")

    def _buildForm(self) -> ModalForm:
        textForm: dict = self.config.get("forms").get("createPolygon")

        return ModalForm(
            title=self.title,
            controls=[
                Label("Создание нового полигона"),
                Label("Территория будет создана вокруг вашей позиции"),
                TextInput("Введите имя полигона:", "Мой дом")
            ],
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
                Button("Информация"), # ok
                Divider(),
                Button("1"),
                Divider(),
                Button("2"),
                Divider(),
                Button("3")
            ],
            on_submit=self._onSubmit,
            on_close=self._onClose
        )


class InfoPolygonForm(BasePolygonForm):
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
                Button("Вернуться")
            ],
            on_submit=self._onSubmit,
            on_close=self._onClose
        )


class ControlPolygonForm(BasePolygonForm):
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
                Button("Добавить игрока"),
                Divider(),
                Button("Удалить игрока"),
                Divider(),
                Button("Удалить полигон")
            ],
            on_submit=self._onSubmit,
            on_close=self._onClose
        )