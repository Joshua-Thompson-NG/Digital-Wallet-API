from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

database_url = "sqlite:///./wallet.db"

engine = create_engine(database_url,
                       connect_args={"check_same_thread": False},
                       echo=True)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

class Base(DeclarativeBase):
    pass