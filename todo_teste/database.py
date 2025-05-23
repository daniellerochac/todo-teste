from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from todo_teste.settings import Settings

settings = Settings()

engine = create_engine(settings.DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session
