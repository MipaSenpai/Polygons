from .base import BasePolygonForm

from endstone import Player
from endstone.form import ActionForm, Button

from ..cache import PolygonCache
from ..database.engine import DatabaseEngine


class InfoPolygonForm(BasePolygonForm):
    def __init__(
            self,
            cache: PolygonCache,
            dbEngine: DatabaseEngine,
            config: dict,
            player: Player
        ):
        super().__init__(config)

        self._cache = cache
        self._dbEngine = dbEngine
        self._player = player

    def _onSubmit(self, player: Player, data: str) -> None:
        from .menu import MenuPolygonForm

        menu = MenuPolygonForm(self._cache, self._dbEngine, self._config, self._player).buildForm()
        player.send_form(menu)

    def _onClose(self, player: Player) -> None:
        print(player.name, "закрыл меню")

    def buildForm(self) -> ActionForm:
        return ActionForm(
            title=self._title,
            content="test", # TODO
            buttons=[Button("Вернуться")],
            on_submit=self._onSubmit,
            on_close=self._onClose
        )