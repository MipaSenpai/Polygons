from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .models import Base


class DatabaseEngine:
    def __init__(self, config: dict, dbPath: str):
        dbConfig: dict = config.get("database")
        dbType = dbConfig.get("type")
        
        if dbType == "sqlite":
            sqliteConfig: dict = dbConfig.get("sqlite")

            filename = sqliteConfig.get("filename")
            self.dbPath = Path(dbPath) if dbPath else Path(filename)

            connection = f"sqlite:///{self.dbPath}"
            
        elif dbType == "mysql":
            mysqlConfig: dict = dbConfig.get("mysql")

            host = mysqlConfig.get("host")
            port = mysqlConfig.get("port")

            username = mysqlConfig.get("username")
            password = mysqlConfig.get("password")
            database = mysqlConfig.get("database")

            connection = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
            
        elif dbType == "postgresql":
            pgConfig: dict = dbConfig.get("postgresql")

            host = pgConfig.get("host")
            port = pgConfig.get("port", 5432)

            username = pgConfig.get("username")
            password = pgConfig.get("password")
            database = pgConfig.get("database")

            connection = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
                        
        self.engine = create_engine(connection, echo=False)
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
