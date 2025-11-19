import json

from abc import ABC, abstractmethod

from endstone import Player
from endstone.plugin import Plugin
from endstone.level import Location

from endstone.form import (
    ActionForm,
    ModalForm,
    TextInput,
    Label,
    Divider,
    Button
)

from ..cache import PolygonCache
from ..database.engine import DatabaseEngine
from ..database.repository import PolygonRepository


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
    def _buildForm(self): pass

    @property
    def form(self): return self._buildForm()
    

class CreatePolygonForm(BasePolygonForm):
    def __init__(
            self,
            plugin: Plugin,
            dbEngine: DatabaseEngine,
            cache: PolygonCache,
            config: dict,
            location: Location,
            size: int
        ):
        super().__init__(config)

        self._cache = cache
        self._dbEngine = dbEngine

        self._plugin = plugin
        self._location = location
        self._size = size

    def _onSubmit(self, player: Player, data: str) -> None:
        formData: list = json.loads(data)
        polygonName: str = formData[2]
        
        if not polygonName or polygonName.strip() == "":
            player.send_message(self._messages.get("notName"))
            player.send_form(self._buildForm())
            return
        
        radius = (self._size - 1) / 2

        blockX = int(self._location.x)
        blockY = int(self._location.y)
        blockZ = int(self._location.z)

        minX = int(blockX - radius)
        minY = int(blockY - radius)
        minZ = int(blockZ - radius)

        maxX = int(blockX + radius)
        maxY = int(blockY + radius)
        maxZ = int(blockZ + radius)
        
        world = self._location.dimension.name

        with self._dbEngine as session:
            repo = PolygonRepository(session)
            existing = repo.getPolygonByName(polygonName)

            if existing:
                player.send_message(self._messages.get("existName").format(name=polygonName)) # toast
                return
                        
            polygon = repo.createPolygon(
                name=polygonName, owner=player.name, world=world,
                centerX=blockX, centerY=blockY, centerZ=blockZ,
                minX=minX, minY=minY, minZ=minZ, 
                maxX=maxX, maxY=maxY, maxZ=maxZ
            )
            
            self._cache.addPolygon(polygon, session)
            
        player.send_message(self._messages.get("create").format(name=polygonName))
                
        if self._config.get("visualBorder"):
            maxX, maxY, maxZ = maxX + 1, maxY + 1, maxZ + 1

            def visualBorder():
                for x in range(minX, maxX):
                    player.spawn_particle("ll:pointP1", x, minY, minZ)
                    player.spawn_particle("ll:pointP1", x, minY, maxZ)
                for z in range(minZ, maxZ):
                    player.spawn_particle("ll:pointP1", minX, minY, z)
                    player.spawn_particle("ll:pointP1", maxX, minY, z)
                
                for x in range(minX, maxX):
                    player.spawn_particle("ll:pointP1", x, maxY, minZ)
                    player.spawn_particle("ll:pointP1", x, maxY, maxZ)
                for z in range(minZ, maxZ):
                    player.spawn_particle("ll:pointP1", minX, maxY, z)
                    player.spawn_particle("ll:pointP1", maxX, maxY, z)
                
                for y in range(minY, maxY):
                    player.spawn_particle("ll:pointP1", minX, y, minZ)
                    player.spawn_particle("ll:pointP1", maxX, y, minZ)
                    player.spawn_particle("ll:pointP1", minX, y, maxZ)
                    player.spawn_particle("ll:pointP1", maxX, y, maxZ)

            visualBorder()
            for i in range(1, 11):
                self._plugin.server.scheduler.run_task(self._plugin, visualBorder, delay=i * 40)
            
    def _onClose(self, player: Player) -> None:
        player.send_message(self._messages.get("cancelCreate"))

    def _buildForm(self) -> ModalForm:
        return ModalForm(
            title=self._title,
            controls=[
                Label(self._textForms.get("createPolygon").get("labelUp")),
                Label(self._textForms.get("createPolygon").get("labelDown")),
                TextInput(self._textForms.get("createPolygon").get("input"), self._textForms.get("createPolygon").get("inputPlaceholder"))
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
        return ActionForm(
            title=self._title,
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
        textForm: dict = self._config.get("forms").get("menuPolygon")

        return ActionForm(
            title=self._title,
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
        textForm: dict = self._config.get("forms").get("menuPolygon")

        return ActionForm(
            title=self._title,
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