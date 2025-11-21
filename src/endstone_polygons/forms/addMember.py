from .base import BasePolygonForm

from endstone import Player

from endstone.form import ActionForm, Button, Divider

from ..cache import PolygonCache
from ..database.models import Polygon
from ..database.engine import DatabaseEngine
from ..database.repository import PolygonRepository


class AddMemberForm(BasePolygonForm):
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
    
    def _onSubmit(self, player: Player, buttonIndex: int) -> None:
        onlinePlayers = [p for p in player.server.online_players 
                        if not self._cache.isMember(self._polygon.id, p.name)]
        
        if buttonIndex != 0:
            selectedPlayer = onlinePlayers[buttonIndex - 1]
            playerName = selectedPlayer.name
            
            with self._dbEngine as session:
                repo = PolygonRepository(session)
                repo.addMember(self._polygon.id, playerName)
            
            self._cache.addMember(self._polygon.id, playerName)
            
            player.send_message(f"§aИгрок §e{playerName}§a добавлен в полигон §e{self._polygon.name}")
        
        from .control import ControlPolygonForm
        player.send_form(ControlPolygonForm(self._cache, self._dbEngine, self._config, self._player, self._polygon).buildForm())

    def _onClose(self, player: Player) -> None: pass

    def buildForm(self) -> ActionForm:
        onlinePlayers = [p for p in self._player.server.online_players 
                        if not self._cache.isMember(self._polygon.id, p.name)]
    
        form = ActionForm(
            title=f"Добавить игрока: {self._polygon.name}",
            content="Выберите игрока для добавления в полигон:" if onlinePlayers else "§cНет доступных игроков для добавления",
            buttons=[
                Button("Вернуться"),
                Divider()
            ],
            on_submit=self._onSubmit,
            on_close=self._onClose
        )
        
        for onlinePlayer in onlinePlayers:
            form.add_button(onlinePlayer.name)
        
        return form
