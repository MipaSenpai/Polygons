from typing import Optional

from sqlalchemy.orm import Session, joinedload

from .models import Polygon, PolygonCoordinates, PolygonFlags, PolygonMember


class PolygonRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def createPolygon(self, name: str, owner: str, world: str,
                      centerX: int, centerY: int, centerZ: int,
                      minX: float, minY: float, minZ: float, 
                      maxX: float, maxY: float, maxZ: float,
                      canBreak: bool = False, canPlace: bool = False, 
                      canOpenChests: bool = False) -> Polygon:
        polygon = Polygon(
            name=name,
            owner=owner,
            world=world
        )
        self.session.add(polygon)
        self.session.flush()
        
        coordinates = PolygonCoordinates(
            polygonId=polygon.id,
            centerX=centerX,
            centerY=centerY,
            centerZ=centerZ,
            minX=minX,
            minY=minY,
            minZ=minZ,
            maxX=maxX,
            maxY=maxY,
            maxZ=maxZ
        )
        self.session.add(coordinates)
        
        flags = PolygonFlags(
            polygonId=polygon.id,
            canBreak=canBreak,
            canPlace=canPlace,
            canOpenChests=canOpenChests
        )
        self.session.add(flags)
        
        self.session.commit()
        
        self.session.refresh(polygon)
        return polygon
    
    def getPolygonByName(self, name: str) -> Optional[Polygon]:
        return self.session.query(Polygon).options(
            joinedload(Polygon.coordinates),
            joinedload(Polygon.flags),
            joinedload(Polygon.members)
        ).filter(Polygon.name == name).first()
    
    def getPolygonById(self, polygonId: int) -> Optional[Polygon]:
        return self.session.query(Polygon).options(
            joinedload(Polygon.coordinates),
            joinedload(Polygon.flags),
            joinedload(Polygon.members)
        ).filter(Polygon.id == polygonId).first()
    
    def getPolygonAtPosition(self, world: str, x: float, z: float) -> Optional[Polygon]:
        return self.session.query(Polygon).join(PolygonCoordinates).options(
            joinedload(Polygon.coordinates),
            joinedload(Polygon.flags),
            joinedload(Polygon.members)
        ).filter(
            Polygon.world == world,
            PolygonCoordinates.minX <= x,
            PolygonCoordinates.maxX >= x,
            PolygonCoordinates.minZ <= z,
            PolygonCoordinates.maxZ >= z
        ).first()
    
    def getPolygonsByOwner(self, owner: str) -> list[Polygon]:
        return self.session.query(Polygon).options(
            joinedload(Polygon.coordinates),
            joinedload(Polygon.flags),
            joinedload(Polygon.members)
        ).filter(Polygon.owner == owner).all()
    
    def getAllPolygons(self) -> list[Polygon]:
        return self.session.query(Polygon).options(
            joinedload(Polygon.coordinates),
            joinedload(Polygon.flags),
            joinedload(Polygon.members)
        ).all()
    
    def deletePolygon(self, polygonId: int) -> bool:
        polygon = self.getPolygonById(polygonId)
        if polygon:
            self.session.delete(polygon)
            self.session.commit()
            return True
        return False
    
    def updatePolygonFlags(self, polygonId: int, **kwargs) -> bool:
        flags = self.session.query(PolygonFlags).filter(PolygonFlags.polygonId == polygonId).first()
        
        if not flags:
            return False
        
        for key, value in kwargs.items():
            if hasattr(flags, key):
                setattr(flags, key, value)
        
        self.session.commit()
        return True
    
    def updatePolygonCoordinates(self, polygonId: int, 
                                 minX: float = None, minY: float = None, minZ: float = None,
                                 maxX: float = None, maxY: float = None, maxZ: float = None) -> bool:
        coords = self.session.query(PolygonCoordinates).filter(PolygonCoordinates.polygonId == polygonId).first()
        
        if not coords:
            return False
        
        if minX is not None:
            coords.minX = minX
        if minY is not None:
            coords.minY = minY
        if minZ is not None:
            coords.minZ = minZ
        if maxX is not None:
            coords.maxX = maxX
        if maxY is not None:
            coords.maxY = maxY
        if maxZ is not None:
            coords.maxZ = maxZ
        
        self.session.commit()
        return True
    
    def addMember(self, polygonId: int, playerName: str) -> Optional[PolygonMember]:
        existing = self.session.query(PolygonMember).filter(
            PolygonMember.polygonId == polygonId,
            PolygonMember.playerName == playerName
        ).first()
        
        if existing:
            return existing
        
        member = PolygonMember(
            polygonId=polygonId,
            playerName=playerName
        )
        
        self.session.add(member)
        self.session.commit()
        return member
    
    def removeMember(self, polygonId: int, playerName: str) -> bool:
        member = self.session.query(PolygonMember).filter(
            PolygonMember.polygonId == polygonId,
            PolygonMember.playerName == playerName
        ).first()
        
        if member:
            self.session.delete(member)
            self.session.commit()
            return True
        return False
    
    def getPolygonMembers(self, polygonId: int) -> list[PolygonMember]:
        return self.session.query(PolygonMember).filter(PolygonMember.polygonId == polygonId).all()
