from rtree import index
from typing import Optional

from endstone import Logger

from .database.models import Polygon
from .database.repository import PolygonRepository


class PolygonCache:
    def __init__(self, logger: Logger):
        self.logger = logger
        self.spatialIndex = index.Index()

        self.polygons = {}
        self.members = {}
        
        self.loaded = False
    
    def loadFromDatabase(self, repository: PolygonRepository):
        self.logger.info("Loading polygons into cache...")
        
        polygons = repository.getAllPolygons()
        for polygon in polygons:
            repository.session.expunge(polygon)
            
            self.polygons[polygon.id] = polygon
            
            if polygon.coordinates:
                self.spatialIndex.insert(
                    polygon.id,
                    (polygon.coordinates.minX, polygon.coordinates.minZ, 
                     polygon.coordinates.maxX, polygon.coordinates.maxZ)
                )
            
            for member in polygon.members:
                memberKey = (polygon.id, member.playerName)
                self.members[memberKey] = True
        
        self.logger.info(f"Loaded {len(self.polygons)} polygons")
        self.loaded = True
    
    def findPolygonAtPosition(self, world: str, x: float, z: float, y: float) -> Optional[Polygon]:
        candidates = list(self.spatialIndex.intersection((x, z, x, z)))
        for polygonId in candidates:
            polygon = self.polygons.get(polygonId)

            if polygon and polygon.world == world and polygon.coordinates:
                coords = polygon.coordinates

                if (coords.minX <= x <= coords.maxX and 
                    coords.minZ <= z <= coords.maxZ):
                    
                    if y is not None and (y < coords.minY or y > coords.maxY):
                        continue
                    
                    return polygon
        
        return None
    
    def addPolygon(self, polygon: Polygon, session=None):
        coords = polygon.coordinates
        membersList = list(polygon.members)
        
        if session:
            session.expunge(polygon)
        
        self.polygons[polygon.id] = polygon
        
        if coords:
            self.spatialIndex.insert(
                polygon.id,
                (coords.minX, coords.minZ,
                 coords.maxX, coords.maxZ)
            )
        
        for member in membersList:
            memberKey = (polygon.id, member.playerName)
            self.members[memberKey] = True
    
    def removePolygon(self, polygonId: int):
        polygon = self.polygons.get(polygonId)
        if not polygon:
            return
        
        if polygon.coordinates:
            self.spatialIndex.delete(
                polygon.id,
                (polygon.coordinates.minX, polygon.coordinates.minZ,
                 polygon.coordinates.maxX, polygon.coordinates.maxZ)
            )
        
        for member in polygon.members:
            memberKey = (polygonId, member.playerName)
            self.members.pop(memberKey, None)
        
        self.polygons.pop(polygonId, None)
    
    def updatePolygonFlags(self, polygonId: int, **kwargs):
        polygon = self.polygons.get(polygonId)
        if polygon and polygon.flags:
            for key, value in kwargs.items():
                if hasattr(polygon.flags, key):
                    setattr(polygon.flags, key, value)
    
    def addMember(self, polygonId: int, playerName: str):
        memberKey = (polygonId, playerName)
        self.members[memberKey] = True
    
    def removeMember(self, polygonId: int, playerName: str):
        memberKey = (polygonId, playerName)
        self.members.pop(memberKey, None)
    
    def isMember(self, polygonId: int, playerName: str) -> bool:
        memberKey = (polygonId, playerName)
        return memberKey in self.members
    
    def isOwner(self, polygonId: int, playerName: str) -> bool:
        polygon = self.polygons.get(polygonId)
        return polygon and polygon.owner == playerName
    
    def canBreak(self, polygon: Polygon, playerName: str) -> bool:
        if polygon.owner == playerName:
            return True
        
        if self.isMember(polygon.id, playerName):
            return True
        
        return polygon.flags.canBreak if polygon.flags else False
    
    def canPlace(self, polygon: Polygon, playerName: str) -> bool:
        if polygon.owner == playerName:
            return True
        
        if self.isMember(polygon.id, playerName):
            return True
        
        return polygon.flags.canPlace if polygon.flags else False
    
    def canOpenChests(self, polygon: Polygon, playerName: str) -> bool:
        if polygon.owner == playerName:
            return True
        
        if self.isMember(polygon.id, playerName):
            return True
        
        return polygon.flags.canOpenChests if polygon.flags else False
