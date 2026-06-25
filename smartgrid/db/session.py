from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from smartgrid.core.config import settings

print("DATABASE_URL =", settings.DATABASE_URL)

engine = create_engine(
    settings.DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()