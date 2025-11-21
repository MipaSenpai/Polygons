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
            player.send_message("§eУдаление полигона отменено")
    
            from .control import ControlPolygonForm
            player.send_form(ControlPolygonForm(self._cache,self._dbEngine,self._config,self._player,self._polygon).buildForm())

            return
        
        with self._dbEngine as session:
            repo = PolygonRepository(session)
            repo.deletePolygon(self._polygon.id)
        
        self._cache.removePolygon(self._polygon.id)
        
        player.send_message(f"§aПолигон §e{self._polygon.name}§a успешно удален")
        
        from .menu import MenuPolygonForm
        player.send_form(MenuPolygonForm(self._cache, self._dbEngine, self._config, self._player).buildForm())

    def _onClose(self, player: Player) -> None:
        from .control import ControlPolygonForm
        player.send_form(ControlPolygonForm(self._cache, self._dbEngine, self._config, self._player, self._polygon).buildForm())

    def buildForm(self) -> ModalForm:
        members_count = len(self._polygon.members) if self._polygon.members else 0
        
        warning = f"ВНИМАНИЕ!§r\n\n"
        warning += f"Вы собираетесь удалить полигон {self._polygon.name}\n"
        warning += f"Мир: {self._polygon.world}\n"
        warning += f"Участников: {members_count}\n\n"
        warning += "Это действие необратимо!"
        
        return ModalForm(
            title=f"Удалить полигон: {self._polygon.name}",
            controls=[
                Label(warning),
                Toggle("Я подтверждаю удаление полигона", False)
            ],
            on_submit=self._onSubmit,
            on_close=self._onClose
        )
