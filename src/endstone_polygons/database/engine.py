"""Database engine and session management."""

from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Base


class DatabaseEngine:
    def __init__(self, dbPath: str = "polygons.db"):
        self.dbPath = Path(dbPath)
        self.engine = create_engine(f"sqlite:///{self.dbPath}", echo=False)
        self.sessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)
        
    def createTables(self):
        Base.metadata.create_all(self.engine)
        
    def getSession(self) -> Session:
        return self.sessionLocal()
    
    def __enter__(self) -> Session:
        self._session = self.sessionLocal()
        return self._session
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, '_session'):
            self._session.close()
        return False
    
    def close(self):
        self.engine.dispose()
