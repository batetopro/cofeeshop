import datetime
import logging
from typing import Union, List


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from config import Config
from .engine import ReaderEngine, SqliteEngine, MySQLEngine, PostgreSQLEngine
from .schemas import Birthday, TopSellingProduct, LastOrderPerCustomer


LOGGER = logging.getLogger(__name__)


class DataReader:
    @property
    def connection_string(self) -> str:
        """
        Connection string used to connect to the database.
        :return: str
        """
        if self._connection_string is None:
            self._connection_string = Config.SQLALCHEMY_DATABASE_URI
        return self._connection_string

    @property
    def db_type(self) -> Union[str, None]:
        """
        What database is used with the connection string.
        :return: str | None
        """
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
        """
        The engine that is used to make queries to the database.
        :return: ReaderEngine
        """
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
        """
        Initialize the data reader with connection string, which is used to connect to the database.
        If None is given, then it uses the config.
        :param connection_string: str
        """
        self._connection_string = connection_string
        self._engine = None
        self._session = None

    def read_birthdays(self, date:datetime.date = None) -> List[Birthday]:
        """
        Get list of customers, which have birthday on the given date.
        :param date: datetime.date | None
        :return: List[Birthday]
        """
        if date is None:
            date = datetime.date.today()
        LOGGER.info("Reading birthdays on '{}'".format(date))
        result = self.engine.read_birthdays(date)
        LOGGER.info("{} records found.".format(len(result)))
        return result

    def read_top_selling_products(self, year: int) -> List[TopSellingProduct]:
        """
        The top 10 selling products for a specific year.
        :param year: int
        :return: List[TopSellingProduct]
        """
        LOGGER.info("Reading top selling products on '{}'".format(year))
        result = self.engine.read_top_selling_products(year)
        LOGGER.info("{} records found.".format(len(result)))
        return result

    def read_last_order_per_customer(self) -> List[LastOrderPerCustomer]:
        """
        The last order per customer with their email.
        :return: List[LastOrderPerCustomer]
        """
        LOGGER.info("Reading last order per customer.")
        result = self.engine.read_last_order_per_customer()
        LOGGER.info("{} records found.".format(len(result)))
        return result
