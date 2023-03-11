import datetime
import logging


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from config import Config
from .engine import ReaderEngine, SqliteEngine, MySQLEngine, PostgreSQLEngine


LOGGER = logging.getLogger(__name__)


class DataReader:
    @property
    def connection_string(self):
        if self._connection_string is None:
            self._connection_string = Config.SQLALCHEMY_DATABASE_URI
        return self._connection_string

    @property
    def db_type(self):
        if self.connection_string.startswith("sqlite"):
            return "sqlite"
        elif self.connection_string.startswith("mysql"):
            return "mysql"
        elif self.connection_string.startswith("postgresql"):
            return "postgresql"
        else:
            return None

    @property
    def engine(self) -> ReaderEngine:
        if self._engine is None:
            if self.db_type == "sqlite":
                self._engine = SqliteEngine(self)
            elif self.db_type == "mysql":
                self._engine = MySQLEngine(self)
            elif self.db_type == "postgresql":
                self._engine = PostgreSQLEngine(self)
            else:
                raise NotImplementedError
        return self._engine

    @property
    def session(self):
        if self._session is None:
            if self.db_type == "sqlite":
                connect_args = {"check_same_thread": False}
            else:
                connect_args = {}
            engine = create_engine(self.connection_string, connect_args=connect_args)
            self._session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()

        return self._session

    def __init__(self, connection_string=None):
        self._connection_string = connection_string
        self._engine = None
        self._session = None

    def read_birthdays(self, date=None):
        if date is None:
            date = datetime.date.today()
        LOGGER.info("Reading birthdays on '{}'".format(date))
        result = self.engine.read_birthdays(date)
        LOGGER.info("{} records found.".format(len(result)))
        return result

    def read_top_selling_products(self, year):
        LOGGER.info("Reading top selling products on '{}'".format(year))
        result = self.engine.read_top_selling_products(year)
        LOGGER.info("{} records found.".format(len(result)))
        return result

    def read_last_order_per_customer(self):
        LOGGER.info("Reading last order per customer.")
        result = self.engine.read_last_order_per_customer()
        LOGGER.info("{} records found.".format(len(result)))
        return result
