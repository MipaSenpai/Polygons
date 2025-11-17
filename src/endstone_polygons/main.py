from endstone.plugin import Plugin
from endstone.event import BlockPlaceEvent, BlockBreakEvent, event_handler

from .commands import PolygonCommand

from .forms import CreatePolygonForm
from .tools import Command, CommandBuilder, Permission


class Polygons(Plugin):
    api_version = "0.10"

    commandBuilder = CommandBuilder()

    commandBuilder.add(
        Command(
            name="polygon",
            description="Polygon management",
            usages="/polygon",
            aliases="pg",
            permissions=Permission(
                name="polygon.command.polygon",
                description="Permission for polygon management",
                default=True
            )
        )
    )

    commands = commandBuilder.commands
    permissions = commandBuilder.permissions

    def on_load(self) -> None:
        self.logger.info("pg load")

    def on_enable(self) -> None:
        self.save_default_config()
        self.register_events(self)

        self.get_command("polygon").executor = PolygonCommand(self)

        self._createForm = CreatePolygonForm(self.config)

    def on_disable(self) -> None:
        self.logger.info("pg disable")
    
    @event_handler
    def placeBlock(self, event: BlockPlaceEvent):
        block = event.block_placed_state
        player = event.player
        print(block.type)
        print(player.name)

        player.send_form(self._createForm.form)

    @event_handler
    def breakBlock(self, event: BlockBreakEvent):
        block = event.block
        player = event.player
        print(block.type)
        print(player.name)