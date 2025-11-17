from endstone.plugin import Plugin


class Polygons(Plugin):
    api_version = "0.10"

    def on_load(self) -> None:
        self.logger.info("pg load")

    def on_enable(self) -> None:
        self.logger.info("pg enable")

    def on_disable(self) -> None:
        self.logger.info("pg disable")