from endstone.plugin import Plugin

from endstone.event import (
    BlockPlaceEvent,
    BlockBreakEvent,
    EventPriority,
    PlayerInteractEvent,
    event_handler
)

from .cache import PolygonCache

from .database.engine import DatabaseEngine
from .database.repository import PolygonRepository

from .forms import CreatePolygonForm
from .commands import PolygonCommand

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
        self.logger.info("Polygons load")

    def on_enable(self) -> None:
        self.save_default_config()
        self.register_events(self)
        
        self._messages: dict = self.config.get("messages")
        self._polygonTypes: dict = self.config.get("polygonTypes")
        
        dbPath = str(self.data_folder / "polygons.db")
        self._dbEngine = DatabaseEngine(self.config, dbPath)
        self._dbEngine.createTables()
        
        dbType = self.config.get("database").get("type")
        if dbType == "sqlite":
            self.logger.info(f"Database initialized (SQLite) at {dbPath}")
        else:
            self.logger.info(f"Database initialized ({dbType.upper()})")
        
        self._cache = PolygonCache(self.logger)
        
        session = self._dbEngine.getSession()
        repository = PolygonRepository(session)

        self._cache.loadFromDatabase(repository)
        session.close()

        self.get_command("polygon").executor = PolygonCommand(self)

    def on_disable(self) -> None:
        if hasattr(self, 'dbEngine'):
            self._dbEngine.close()

        self.logger.info("Polygons disabled")
    
    @event_handler(priority=EventPriority.HIGHEST)
    def placeBlock(self, event: BlockPlaceEvent):
        player = event.player
        block = event.block_placed_state
        location = block.location
        
        if block.type in self._polygonTypes.keys():
            existingPolygon = self._cache.findPolygonAtPosition(location.dimension.name, location.x, location.z, location.y)
            if existingPolygon:
                if not self._cache.canPlace(existingPolygon, player.name):
                    event.is_cancelled = True
                    player.send_popup(self._messages.get("cannotBuild").format(name=existingPolygon.name))
                    return
            
            else:
                size = self._polygonTypes.get(block.type)
                _, _, _, minX, minY, minZ, maxX, maxY, maxZ = self._cache.calculatePolygonBounds(
                    location.x, location.y, location.z, size
                )
                
                intersecting = self._cache.checkIntersection(
                    location.dimension.name, minX, minY, minZ, maxX, maxY, maxZ
                )
                
                if intersecting:
                    event.is_cancelled = True
                    player.send_message(self._messages.get("cannotCreateIntersection").format(name=intersecting.name))
                    return
                
                createForm = CreatePolygonForm(self, self._dbEngine, self._cache, self.config, location, size)
                player.send_form(createForm.form)
                
                return
        
        polygon = self._cache.findPolygonAtPosition(location.dimension.name, location.x, location.z, location.y)
        if polygon:
            if not self._cache.canPlace(polygon, player.name):
                event.is_cancelled = True
                player.send_popup(self._messages.get("cannotBuild").format(name=polygon.name))
                return

    @event_handler(priority=EventPriority.HIGHEST)
    def breakBlock(self, event: BlockBreakEvent):
        block = event.block
        player = event.player
        location = block.location
        
        polygon = self._cache.findPolygonAtPosition(location.dimension.name, location.x, location.z, location.y)
        if polygon:
            if (polygon.coordinates and
                block.type in self._polygonTypes.keys() and
                int(location.x) == polygon.coordinates.centerX and
                int(location.y) == polygon.coordinates.centerY and
                int(location.z) == polygon.coordinates.centerZ):
                
                if not self._cache.isOwner(polygon.id, player.name):
                    event.is_cancelled = True
                    player.send_message(self._messages.get("onlyOwnerCanDelete").format(name=polygon.name))
                    return
                
                session = self._dbEngine.getSession()
                repository = PolygonRepository(session)
                repository.deletePolygon(polygon.id)
                session.close()
                
                self._cache.removePolygon(polygon.id)
                player.send_message(self._messages.get("polygonDeleted").format(name=polygon.name))
                player.play_sound(player.location, "random.anvil_break")
                return
            
            if not self._cache.canBreak(polygon, player.name):
                event.is_cancelled = True
                player.send_popup(self._messages.get("cannotBreak").format(name=polygon.name))
                return
            
    @event_handler()
    def openContainers(self, event: PlayerInteractEvent):
        try:
            player = event.player
            block = event.block
            location = block.location

            containers = [
                "chest", "trapped_chest", "barrel", "ender_chest", 
                "furnace", "lit_furnace", "blast_furnace", "lit_blast_furnace", "smoker", "lit_smoker", 
                "copper_chest", "exposed_copper_chest", "weathered_copper_chest", "oxidized_copper_chest", 
                "waxed_copper_chest", "waxed_exposed_copper_chest", "waxed_weathered_copper_chest", "waxed_oxidized_copper_chest", 
                "brewing_stand", "chiseled_bookshelf", "decorated_pot", "frame", "glow_frame",
                "dispenser", "dropper", "hopper", "jukebox", "lectern",
                "undyed_shulker_box", "white_shulker_box", "orange_shulker_box", "magenta_shulker_box", "light_blue_shulker_box", 
                "yellow_shulker_box", "lime_shulker_box", "pink_shulker_box", "gray_shulker_box", "light_gray_shulker_box", "red_shulker_box", 
                "cyan_shulker_box", "purple_shulker_box", "blue_shulker_box", "brown_shulker_box", "green_shulker_box", "black_shulker_box"
                ]
            for container in containers:
                if container in block.type:
                    polygon = self._cache.findPolygonAtPosition(
                        location.dimension.name, location.x, location.z, location.y
                    )
                    
                    if polygon:
                        if not self._cache.canOpenChests(polygon, player.name):
                            event.is_cancelled = True
                            player.send_popup(
                                self._messages.get("cannotOpenChests").format(name=polygon.name)
                            )
                            return
                        
        except:
            return
