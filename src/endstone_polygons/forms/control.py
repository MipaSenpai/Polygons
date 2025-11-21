from .base import BasePolygonForm

from endstone import Player
from endstone.form import ActionForm, Divider, Button

from ..cache import PolygonCache
from ..database.models import Polygon
from ..database.engine import DatabaseEngine


class ControlPolygonForm(BasePolygonForm):
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
        formData = int(data)

        match formData:
            case 0:
                from .menu import MenuPolygonForm
                player.send_form(MenuPolygonForm(self._cache, self._dbEngine, self._config, self._player).buildForm())

            case 1:
                from .flags import FlagsPolygonForm
                player.send_form(FlagsPolygonForm(self._cache, self._dbEngine, self._config, self._player, self._polygon).buildForm())

            case 2:
                from .addMember import AddMemberForm
                player.send_form(AddMemberForm(self._cache, self._dbEngine, self._config, self._player, self._polygon).buildForm())

            case 3:
                from .removeMember import RemoveMemberForm
                player.send_form(RemoveMemberForm(self._cache, self._dbEngine, self._config, self._player, self._polygon).buildForm())

            case 4:
                from .delete import DeletePolygonForm
                player.send_form(DeletePolygonForm(self._cache, self._dbEngine, self._config, self._player, self._polygon).buildForm())

    def _onClose(self, player: Player) -> None: pass

    def buildForm(self) -> ActionForm:
        flags = self._polygon.flags
        members_count = len(self._polygon.members) if self._polygon.members else 0
        
        content = f"Полигон: §e{self._polygon.name}§r\n"
        content += f"Владелец: §e{self._polygon.owner}§r\n"
        content += f"Мир: {self._polygon.world}\n"
        content += f"Участников: {members_count}\n"
        
        if self._polygon.members and members_count > 0:
            content += "\nУчастники:\n"
            for member in self._polygon.members:
                content += f"  §7• §f{member.playerName}§r\n"
        
        content += "\nФлаги:\n"
        content += f"  §7• §fЛомать: {'§aДа§r' if flags and flags.canBreak else '§cНет§r'}\n"
        content += f"  §7• §fСтроить: {'§aДа§r' if flags and flags.canPlace else '§cНет§r'}\n"
        content += f"  §7• §fСундуки: {'§aДа§r' if flags and flags.canOpenChests else '§cНет§r'}"

        return ActionForm(
            title=f"Управление: {self._polygon.name}",
            content=content,
            buttons=[
                Button("Вернуться"),
                Divider(),
                Button("Управление флагами"),
                Button("Добавить игрока"),
                Button("Удалить игрока"),
                Button("Удалить полигон")
            ],
            on_submit=self._onSubmit,
            on_close=self._onClose
        )