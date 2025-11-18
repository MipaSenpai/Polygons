from typing import List

from endstone import Player
from endstone.plugin import Plugin
from endstone.command import Command, CommandSender, CommandExecutor

from ..forms import MenuPolygonForm


class PolygonCommand(CommandExecutor):
    def __init__(self, plugin: Plugin):
        super().__init__()
        self.plugin = plugin
        self.config = plugin.config
        self.menuForm = MenuPolygonForm(self.config)

    def on_command(self, sender: CommandSender, command: Command, args: List[str]) -> bool:
        if not isinstance(sender, Player):
            sender.send_message("§cЭта команда доступна только игрокам")
            return

        player: Player = sender
        player.send_form(self.menuForm.form)
