from datetime import datetime

from sqlalchemy import String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Polygon(Base):
    __tablename__ = "polygons"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    owner: Mapped[str] = mapped_column(String, nullable=False)
    world: Mapped[str] = mapped_column(String, nullable=False)
    
    createdAt: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updatedAt: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    coordinates: Mapped["PolygonCoordinates"] = relationship(
        "PolygonCoordinates", back_populates="polygon", uselist=False, cascade="all, delete-orphan"
    )
    flags: Mapped["PolygonFlags"] = relationship(
        "PolygonFlags", back_populates="polygon", uselist=False, cascade="all, delete-orphan"
    )
    members: Mapped[list["PolygonMember"]] = relationship(
        "PolygonMember", back_populates="polygon", cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Polygon(id={self.id}, name='{self.name}', owner='{self.owner}')>"


class PolygonCoordinates(Base):
    __tablename__ = "polygonCoordinates"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    polygonId: Mapped[int] = mapped_column(
        Integer, ForeignKey("polygons.id"), nullable=False, unique=True
    )
    
    minX: Mapped[int] = mapped_column(Integer, nullable=False)
    minY: Mapped[int] = mapped_column(Integer, nullable=False)
    minZ: Mapped[int] = mapped_column(Integer, nullable=False)
    maxX: Mapped[int] = mapped_column(Integer, nullable=False)
    maxY: Mapped[int] = mapped_column(Integer, nullable=False)
    maxZ: Mapped[int] = mapped_column(Integer, nullable=False)
    
    centerX: Mapped[int] = mapped_column(Integer, nullable=False)
    centerY: Mapped[int] = mapped_column(Integer, nullable=False)
    centerZ: Mapped[int] = mapped_column(Integer, nullable=False)
    
    polygon: Mapped["Polygon"] = relationship("Polygon", back_populates="coordinates")
    
    def __repr__(self) -> str:
        return f"<PolygonCoordinates(polygonId={self.polygonId}, center=({self.centerX}, {self.centerY}, {self.centerZ}))>"


class PolygonFlags(Base):
    __tablename__ = "polygonFlags"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    polygonId: Mapped[int] = mapped_column(
        Integer, ForeignKey("polygons.id"), nullable=False, unique=True
    )
    
    canBreak: Mapped[bool] = mapped_column(Boolean, default=False)
    canPlace: Mapped[bool] = mapped_column(Boolean, default=False)
    canOpenChests: Mapped[bool] = mapped_column(Boolean, default=False)
    
    pvpEnabled: Mapped[bool] = mapped_column(Boolean, default=True)
    mobSpawning: Mapped[bool] = mapped_column(Boolean, default=True)
    fireSpread: Mapped[bool] = mapped_column(Boolean, default=False)
    explosions: Mapped[bool] = mapped_column(Boolean, default=False)

    polygon: Mapped["Polygon"] = relationship("Polygon", back_populates="flags")
    
    def __repr__(self) -> str:
        return f"<PolygonFlags(polygonId={self.polygonId})>"


class PolygonMember(Base):
    __tablename__ = "polygonMembers"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    polygonId: Mapped[int] = mapped_column(Integer, ForeignKey("polygons.id"), nullable=False)
    playerName: Mapped[str] = mapped_column(String, nullable=False)
    
    addedAt: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    polygon: Mapped["Polygon"] = relationship("Polygon", back_populates="members")
    
    def __repr__(self) -> str:
        return f"<PolygonMember(id={self.id}, player='{self.playerName}', polygonId={self.polygonId})>"
