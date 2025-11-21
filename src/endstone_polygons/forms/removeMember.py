from .base import BasePolygonForm

from endstone import Player

from endstone.form import ActionForm, Button, Divider

from ..cache import PolygonCache
from ..database.models import Polygon
from ..database.engine import DatabaseEngine
from ..database.repository import PolygonRepository


class RemoveMemberForm(BasePolygonForm):
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
        self._members = list(polygon.members) if polygon.members else []
    
    def _onSubmit(self, player: Player, data: str) -> None:
        memberIndex = int(data)
        
        if memberIndex != 0:
            member = self._members[memberIndex - 1]
            playerName = member.playerName
            
            with self._dbEngine as session:
                repo = PolygonRepository(session)
                repo.removeMember(self._polygon.id, playerName)
            
            self._cache.removeMember(self._polygon.id, playerName)

            player.send_message(f"§aИгрок §e{playerName}§a удален из полигона §e{self._polygon.name}")
        
        from .control import ControlPolygonForm
        player.send_form(ControlPolygonForm(self._cache, self._dbEngine, self._config, self._player, self._polygon).buildForm())

    def _onClose(self, player: Player) -> None: pass

    def buildForm(self) -> ActionForm:
        form = ActionForm(
            title=f"Удалить игрока: {self._polygon.name}",
            content=f"Выберите игрока для удаления из полигона {self._polygon.name}:" if self._members else "В полигоне нет добавленных игроков",
            buttons=[
                Button("Вернуться"),
                Divider()
            ],
            on_submit=self._onSubmit,
            on_close=self._onClose
        )
        
        for member in self._members:
            form.add_button(member.playerName)
        
        return form