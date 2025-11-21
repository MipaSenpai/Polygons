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
        player.play_sound(player.location, "random.pop")

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

    def _onClose(self, player: Player) -> None:
        player.play_sound(player.location, "random.pop")

    def buildForm(self) -> ActionForm:
        flags = self._polygon.flags
        members_count = len(self._polygon.members) if self._polygon.members else 0
        
        membersList = ""
        if self._polygon.members and members_count > 0:
            membersList = "\nMembers:\n"

            for member in self._polygon.members:
                membersList += f"  • {member.playerName}\n"

            membersList += "\n"
        
        content = self._textForms.get("control").get("content").format(
            name=self._polygon.name,
            owner=self._polygon.owner,
            world=self._polygon.world,
            membersCount=members_count,
            members_list=membersList,
            canBreak="Yes" if flags and flags.canBreak else "No",
            canPlace="Yes" if flags and flags.canPlace else "No",
            canOpenChests="Yes" if flags and flags.canOpenChests else "No"
        )

        return ActionForm(
            title=self._textForms.get("control").get("title").format(name=self._polygon.name),
            content=content,
            buttons=[
                Button(self._textForms.get("control").get("buttonBack")),
                Divider(),
                Button(self._textForms.get("control").get("buttonFlags")),
                Button(self._textForms.get("control").get("buttonAddMember")),
                Button(self._textForms.get("control").get("buttonRemoveMember")),
                Button(self._textForms.get("control").get("buttonDelete"))
            ],
            on_submit=self._onSubmit,
            on_close=self._onClose
        )