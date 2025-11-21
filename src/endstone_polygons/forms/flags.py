import json

from .base import BasePolygonForm

from endstone import Player

from endstone.form import ModalForm, Toggle

from ..cache import PolygonCache
from ..database.models import Polygon
from ..database.engine import DatabaseEngine
from ..database.repository import PolygonRepository


class FlagsPolygonForm(BasePolygonForm):
    def __init__(
            self,
            cache: PolygonCache,
            dbEngine: DatabaseEngine,
            config: dict,
            player: Player,
            polygon: Polygon
        ):
        super().__init__(config)
        
        self._cache = cache
        self._dbEngine = dbEngine
        self._player = player
        self._polygon = polygon
    
    def _onSubmit(self, player: Player, data: str) -> None:
        formData = json.loads(data)
        
        canBreak = formData[0]
        canPlace = formData[1]
        canOpenChests = formData[2]
        
        with self._dbEngine as session:
            repo = PolygonRepository(session)
            repo.updatePolygonFlags(
                self._polygon.id,
                canBreak=canBreak,
                canPlace=canPlace,
                canOpenChests=canOpenChests
            )

        self._cache.updatePolygonFlags(
            self._polygon.id,
            canBreak=canBreak,
            canPlace=canPlace,
            canOpenChests=canOpenChests
        )
        
        player.send_message(f"§aФлаги полигона §e{self._polygon.name}§a обновлены")
        
        from .control import ControlPolygonForm
        player.send_form(ControlPolygonForm(self._cache, self._dbEngine, self._config, self._player, self._polygon).buildForm())

    def _onClose(self, player: Player) -> None:
        from .control import ControlPolygonForm
        player.send_form(ControlPolygonForm(self._cache, self._dbEngine, self._config, self._player, self._polygon).buildForm())

    def buildForm(self) -> ModalForm:
        flags = self._polygon.flags
        
        return ModalForm(
            title=f"Флаги: {self._polygon.name}",
            controls=[
                Toggle("Разрешить ломать блоки", flags.canBreak if flags else False),
                Toggle("Разрешить ставить блоки", flags.canPlace if flags else False),
                Toggle("Разрешить открывать сундуки", flags.canOpenChests if flags else False)
            ],
            on_submit=self._onSubmit,
            on_close=self._onClose
        )