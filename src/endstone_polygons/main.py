from endstone.plugin import Plugin

from .tools import Command, CommandBuilder, Permission


class Polygons(Plugin):
    api_version = "0.10"

    registry = CommandBuilder()

    pgPermission = Permission(
        name="polygon.command.polygon",
        description="pg",
        default=True
    )

    registry.add(Command(
        name="pg",
        description="Полигоны",
        usages="/pg",
        permissions=pgPermission
    ))

    commands = registry.commands
    permissions = registry.permissions

    def on_load(self) -> None:
        self.logger.info("pg load")

    def on_enable(self) -> None:
        self.logger.info("pg enable")

    def on_disable(self) -> None:
        self.logger.info("pg disable")