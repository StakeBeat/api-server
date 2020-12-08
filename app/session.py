import logging
import os
from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.borg import Borg

DATABASE_URI = os.environ.get('DATABASE_URI')


class SessionManagerBorg(Borg):
    def __init__(self) -> None:
        super().__init__()

        if not hasattr(self, 'db_url'):
            self.db_url = ''
            self.engine = None
            self.maker = None

    @contextmanager
    def use_connection(self) -> Iterator:
        if self.engine is None:
            self.configure(DATABASE_URI)
        connection = self.engine.connect()  # type: ignore
        try:
            yield connection
        finally:
            connection.close()

    def configure(self, db_url: str) -> None:
        logging.info('Configuring database..')
        self.db_url = db_url
        self.engine = create_engine(
            db_url,
            echo=False,
            use_batch_mode=True,
            connect_args={'connect_timeout': 1},
        )
        self.maker = sessionmaker(bind=self.engine)

    @contextmanager
    def session(self) -> Iterator:
        if self.maker is None:
            self.configure(DATABASE_URI)

        db_session = self.maker and self.maker()
        try:
            yield db_session
            db_session and db_session.flush()
            db_session and db_session.expunge_all()
            db_session and db_session.commit()
        except Exception:
            db_session and db_session.rollback()
            raise
        finally:
            db_session and db_session.close()


SessionManager = SessionManagerBorg()
