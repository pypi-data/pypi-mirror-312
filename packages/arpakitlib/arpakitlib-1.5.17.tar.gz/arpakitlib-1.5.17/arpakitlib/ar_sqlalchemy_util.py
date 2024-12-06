import logging
from datetime import timedelta, datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import create_engine, QueuePool, text, func, inspect, INTEGER, TEXT, TIMESTAMP
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm.session import Session

from arpakitlib.ar_datetime_util import now_utc_dt
from arpakitlib.ar_json_util import safely_transfer_to_json_str

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


class BaseDBM(DeclarativeBase):
    __abstract__ = True
    _bus_data: dict[str, Any] | None = None

    @property
    def bus_data(self) -> dict[str, Any]:
        if self._bus_data is None:
            self._bus_data = {}
        return self._bus_data

    def simple_dict(self) -> dict[str, Any]:
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def simple_json(self) -> str:
        return safely_transfer_to_json_str(self.simple_dict())


class SimpleDBM(BaseDBM):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        INTEGER, primary_key=True, autoincrement=True, nullable=False
    )
    long_id: Mapped[str] = mapped_column(
        TEXT, insert_default=uuid4, unique=True, nullable=False
    )
    creation_dt: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), insert_default=now_utc_dt, index=True, nullable=False
    )


class EasySQLAlchemyDB:
    def __init__(self, *, db_url: str, echo: bool = False):
        self._logger = logging.getLogger(self.__class__.__name__)
        self.engine = create_engine(
            url=db_url,
            echo=echo,
            pool_size=5,
            max_overflow=10,
            poolclass=QueuePool,
            pool_timeout=timedelta(seconds=30).total_seconds()
        )
        self.sessionmaker = sessionmaker(bind=self.engine)
        self.func_new_session_counter = 0

    def drop_celery_tables(self):
        with self.engine.connect() as connection:
            connection.execute(text("DROP TABLE IF EXISTS celery_tasksetmeta CASCADE;"))
            connection.execute(text("DROP TABLE IF EXISTS celery_taskmeta CASCADE;"))
            connection.commit()
            self._logger.info("celery tables were dropped")

    def remove_celery_tables_data(self):
        with self.engine.connect() as connection:
            connection.execute(text("DELETE FROM celery_tasksetmeta;"))
            connection.execute(text("DELETE FROM celery_taskmeta;"))
            connection.commit()
            self._logger.info("celery tables data were removed")

    def init(self):
        BaseDBM.metadata.create_all(bind=self.engine, checkfirst=True)
        self._logger.info("db was inited")

    def drop(self):
        BaseDBM.metadata.drop_all(bind=self.engine, checkfirst=True)
        self._logger.info("db was dropped")

    def reinit(self):
        BaseDBM.metadata.drop_all(bind=self.engine, checkfirst=True)
        BaseDBM.metadata.create_all(bind=self.engine, checkfirst=True)
        self._logger.info("db was reinited")

    def check_conn(self):
        self.engine.connect()
        self._logger.info("db conn is good")

    def new_session(self) -> Session:
        self.func_new_session_counter += 1
        return self.sessionmaker(bind=self.engine)

    def is_conn_good(self) -> bool:
        try:
            self.check_conn()
        except Exception as e:
            self._logger.error(e)
            return False
        return True

    def generate_unique_id(self, *, class_dbm: type[SimpleDBM]):
        with self.new_session() as session:
            res: int = session.query(func.max(class_dbm.id)).scalar()
            while session.query(class_dbm).filter(class_dbm.id == res).first() is not None:
                res += 1
        return res

    def generate_unique_long_id(self, *, class_dbm: type[SimpleDBM]):
        with self.new_session() as session:
            res: str = str(uuid4())
            while session.query(class_dbm).filter(class_dbm.long_id == res).first() is not None:
                res = str(uuid4())
        return res


def __example():
    pass


if __name__ == '__main__':
    __example()
