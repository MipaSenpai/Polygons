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

            player.play_sound(player.location, "random.pop")
            player.send_toast(
                self._messages.get("title"),
                self._messages.get("memberRemoved").format(player=playerName, name=self._polygon.name)
            )

        else:
            player.play_sound(player.location, "note.bass")
        
        from .control import ControlPolygonForm
        player.send_form(ControlPolygonForm(self._cache, self._dbEngine, self._config, self._player, self._polygon).buildForm())

    def _onClose(self, player: Player) -> None:
        player.play_sound(player.location, "random.pop")

    def buildForm(self) -> ActionForm:
        content = self._textForms.get("removeMember").get("content").format(name=self._polygon.name) if self._members else self._textForms.get("removeMember").get("contentEmpty")
        
        form = ActionForm(
            title=self._textForms.get("removeMember").get("title").format(name=self._polygon.name),
            content=content,
            buttons=[
                Button(self._textForms.get("removeMember").get("buttonBack")),
                Divider()
            ],
            on_submit=self._onSubmit,
            on_close=self._onClose
        )
        
        for member in self._members:
            form.add_button(member.playerName)
        
        return form