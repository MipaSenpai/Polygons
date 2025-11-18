from endstone.plugin import Plugin
from endstone.event import BlockPlaceEvent, BlockBreakEvent, event_handler, EventPriority

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
        self.logger.info("pg load")

    def on_enable(self) -> None:
        self.save_default_config()
        self.register_events(self)
        
        dbPath = str(self.data_folder / "polygons.db")
        self.dbEngine = DatabaseEngine(dbPath)
        self.dbEngine.createTables()
        self.logger.info(f"Database initialized at {dbPath}")
        
        self.cache = PolygonCache(self.logger)
        
        session = self.dbEngine.getSession()
        repository = PolygonRepository(session)
        self.cache.loadFromDatabase(repository)
        session.close()

        self.get_command("polygon").executor = PolygonCommand(self)

    def on_disable(self) -> None:
        if hasattr(self, 'dbEngine'):
            self.dbEngine.close()

        self.logger.info("pg disable")
    
    @event_handler(priority=EventPriority.HIGHEST)
    def placeBlock(self, event: BlockPlaceEvent):
        player = event.player
        block = event.block_placed_state
        location = block.location
        
        if block.type == "minecraft:diamond_block":
            existingPolygon = self.cache.findPolygonAtPosition(location.dimension.name, location.x, location.z)
            
            if existingPolygon:
                if not self.cache.canPlace(existingPolygon, player.name):
                    event.is_cancelled = True
                    player.send_error_message(f"§cВы не можете строить в полигоне '{existingPolygon.name}'")
                    return
            
            else:
                createForm = CreatePolygonForm(self.config,self.dbEngine,self.cache,location)
                player.send_form(createForm.form)
                return
        
        polygon = self.cache.findPolygonAtPosition(location.dimension.name, location.x, location.z)

        if polygon:
            if not self.cache.canPlace(polygon, player.name):
                event.is_cancelled = True
                player.send_error_message(f"§cВы не можете строить в полигоне '{polygon.name}'")
                return

    @event_handler(priority=EventPriority.HIGHEST)
    def breakBlock(self, event: BlockBreakEvent):
        block = event.block
        player = event.player
        location = block.location
        
        polygon = self.cache.findPolygonAtPosition(location.dimension.name, location.x, location.z)
        if polygon:
            if (polygon.coordinates and
                block.type == "minecraft:diamond_block" and
                int(location.x) == polygon.coordinates.centerX and
                int(location.y) == polygon.coordinates.centerY and
                int(location.z) == polygon.coordinates.centerZ):
                
                if not self.cache.isOwner(polygon.id, player.name):
                    event.is_cancelled = True
                    player.send_error_message(f"§cТолько владелец может удалить основной блок полигона '{polygon.name}'")
                    return
                
                session = self.dbEngine.getSession()
                repository = PolygonRepository(session)
                repository.deletePolygon(polygon.id)
                session.close()
                
                self.cache.removePolygon(polygon.id)
                player.send_message(f"§aПолигон '{polygon.name}' удален")
                return
            
            if not self.cache.canBreak(polygon, player.name):
                event.is_cancelled = True
                player.send_error_message(f"§cВы не можете ломать блоки в полигоне '{polygon.name}'")
                return
