from .base import BasePolygonForm

from endstone import Player
from endstone.form import ActionForm, Divider, Button

from ..cache import PolygonCache
from ..database.engine import DatabaseEngine


class MenuPolygonForm(BasePolygonForm):
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
        
        self._polygons = self._cache.getPolygonsByOwner(player.name)
    
    def _onSubmit(self, player: Player, data: str) -> None:
        formData = int(data)

        if formData == 0:
            from .info import InfoPolygonForm

            infoForm = InfoPolygonForm(self._cache, self._dbEngine, self._config, self._player).buildForm()
            player.send_form(infoForm)

            return
        
        selectedPolygon = self._polygons[formData - 1]
            
        from .control import ControlPolygonForm

        player.send_form(
            ControlPolygonForm(
                self._cache,
                self._dbEngine,
                self._config,
                self._player,
                selectedPolygon
            ).buildForm()
        )

    def _onClose(self, player: Player) -> None:
        print(player.name, "закрыл меню")

    def buildForm(self) -> ActionForm:
        buttons = [Button("Информация")]
        
        if self._polygons:
            buttons.append(Divider())
        
        for polygon in self._polygons:
            buttons.append(Button(polygon.name))
        
        return ActionForm(
            title=self._title,
            content=f"Количество полигонов: {len(self._polygons)}",
            buttons=buttons,
            on_submit=self._onSubmit,
            on_close=self._onClose
        )