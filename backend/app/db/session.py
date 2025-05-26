from sqlmodel import Session, create_engine

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=False)


def get_db():
    with Session(engine) as session:
        yield session
