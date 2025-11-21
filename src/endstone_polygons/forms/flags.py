import json

from .base import BasePolygonForm

from endstone import Player

from endstone.form import ModalForm, Toggle, Label

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
        
        canBreak = formData[1]
        canPlace = formData[2]
        canOpenChests = formData[3]
        
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
        
        player.play_sound(player.location, "block.enchanting_table.use")
        player.send_toast(
            self._messages.get("title"),
            self._messages.get("flagsUpdated").format(name=self._polygon.name)
        )
        
        from .control import ControlPolygonForm
        player.send_form(ControlPolygonForm(self._cache, self._dbEngine, self._config, self._player, self._polygon).buildForm())

    def _onClose(self, player: Player) -> None:
        from .control import ControlPolygonForm
        player.send_form(ControlPolygonForm(self._cache, self._dbEngine, self._config, self._player, self._polygon).buildForm())
        player.play_sound(player.location, "random.pop")

    def buildForm(self) -> ModalForm:
        flags = self._polygon.flags
        
        return ModalForm(
            title=self._textForms.get("flags").get("title").format(name=self._polygon.name),
            controls=[
                Label(self._textForms.get("flags").get("label").format(name=self._polygon.name)),
                Toggle(self._textForms.get("flags").get("toggleBreak"), flags.canBreak if flags else False),
                Toggle(self._textForms.get("flags").get("togglePlace"), flags.canPlace if flags else False),
                Toggle(self._textForms.get("flags").get("toggleChests"), flags.canOpenChests if flags else False)
            ],
            on_submit=self._onSubmit,
            on_close=self._onClose
        )