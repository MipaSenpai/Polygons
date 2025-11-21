import json

from .base import BasePolygonForm

from endstone import Player

from endstone.form import ModalForm, Label, Toggle

from ..cache import PolygonCache
from ..database.models import Polygon
from ..database.engine import DatabaseEngine
from ..database.repository import PolygonRepository


class DeletePolygonForm(BasePolygonForm):
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
        confirmed = formData[1]
        
        if not confirmed:
            player.send_toast(
                self._messages.get("title"),
                self._messages.get("deleteCancelled")
            )
    
            from .control import ControlPolygonForm
            player.send_form(ControlPolygonForm(self._cache,self._dbEngine,self._config,self._player,self._polygon).buildForm())

            return
        
        with self._dbEngine as session:
            repo = PolygonRepository(session)
            repo.deletePolygon(self._polygon.id)
        
        self._cache.removePolygon(self._polygon.id)
        
        player.play_sound(player.location, "note.bass")
        player.send_toast(
            self._messages.get("title"),
            self._messages.get("deleteSuccess").format(name=self._polygon.name)
        )
        
        from .menu import MenuPolygonForm
        player.send_form(MenuPolygonForm(self._cache, self._dbEngine, self._config, self._player).buildForm())

    def _onClose(self, player: Player) -> None:
        from .control import ControlPolygonForm
        player.send_form(ControlPolygonForm(self._cache, self._dbEngine, self._config, self._player, self._polygon).buildForm())
        player.play_sound(player.location, "random.pop")

    def buildForm(self) -> ModalForm:
        members_count = len(self._polygon.members) if self._polygon.members else 0
        
        warning = self._textForms.get("delete").get("warning").format(
            name=self._polygon.name,
            world=self._polygon.world,
            membersCount=members_count
        )
        
        return ModalForm(
            title=self._textForms.get("delete").get("title").format(name=self._polygon.name),
            controls=[
                Label(warning),
                Toggle(self._textForms.get("delete").get("toggle"), False)
            ],
            on_submit=self._onSubmit,
            on_close=self._onClose
        )
