import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


# Loading variables from .env
load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_HOSTNAME = os.getenv('DB_HOSTNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DSN = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}/{DB_NAME}'


def destruct_sqlalchemy_session(session: Session) -> None:
    session.close()


def create_sqlalchemy_session() -> Session:
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=create_engine(
            DSN,
            isolation_level='AUTOCOMMIT',
            pool_pre_ping=True,
        ),
        expire_on_commit=False,
    )()
