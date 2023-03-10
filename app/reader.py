import datetime
import logging
from app.config import Config


LOGGER = logging.getLogger(__name__)


class ReaderEngine:
    @property
    def reader(self):
        return self._reader

    def __init__(self, reader):
        self._reader = reader

    def read_birthdays(self, date):
        raise NotImplementedError

    def read_top_selling_products(self, year):
        raise NotImplementedError

    def read_last_order_per_customer(self):
        raise NotImplementedError


class SqliteEngine(ReaderEngine):
    def read_birthdays(self, date):
        sql = """
        SELECT customer_id, name
        FROM customer
        WHERE strftime('%d %m', birthdate) = '{}'
        ORDER BY customer_id ASC
        """.format(date.strftime('%d %m'))

        rows = self.reader.db.session.execute(self.reader.db.text(sql))

        result = []
        for row in rows:
            result.append({
                "customer_id": row[0],
                "customer_first_name": row[1],
            })
        return result


class MySQLEngine(ReaderEngine):
    def read_birthdays(self, date):
        sql = """
        SELECT customer_id, name
        FROM customer
        WHERE MONTH(birthdate) = :month
            AND DAYOFMONTH(birthdate) = :day
        ORDER BY customer_id ASC 
        """
        params = dict(day=date.day, month=date.month)

        rows = self.reader.db.session.execute(self.reader.db.text(sql), params)

        result = []
        for row in rows:
            result.append({
                "customer_id": row[0],
                "customer_first_name": row[1],
            })
        return result


class PostgreSQLEngine(ReaderEngine):
    def read_birthdays(self, date):
        sql = """
        SELECT customer_id, name
        FROM customer
        WHERE extract(month from birthdate) = :month
            AND extract(day from birthdate) = :day  
        ORDER BY customer_id ASC 
        """
        params = dict(day=date.day, month=date.month)

        rows = self.reader.db.session.execute(self.reader.db.text(sql), params)

        result = []
        for row in rows:
            result.append({
                "customer_id": row[0],
                "customer_first_name": row[1],
            })
        return result


class DataReader:
    @property
    def db(self):
        if self._db is None:
            from app.models import db
            self._db = db
        return self._db

    @property
    def engine(self) -> ReaderEngine:
        if self._engine is None:
            if Config.SQLALCHEMY_DATABASE_URI.startswith("sqlite"):
                self._engine = SqliteEngine(self)
            elif Config.SQLALCHEMY_DATABASE_URI.startswith("mysql"):
                self._engine = MySQLEngine(self)
            elif Config.SQLALCHEMY_DATABASE_URI.startswith("postgresql"):
                self._engine = PostgreSQLEngine(self)
            else:
                raise NotImplementedError
        return self._engine

    def __init__(self, db=None, engine=None):
        self._db = db
        self._engine = engine

    def read_birthdays(self, date=None):
        if date is None:
            date = datetime.date.today()
        LOGGER.info("Reading birthdays on '{}'".format(date))
        result = self.engine.read_birthdays(date)
        LOGGER.info("{} records found.".format(len(result)))
        return result

    def read_top_selling_products(self, year):
        return self.engine.read_top_selling_products(year)

    def read_last_order_per_customer(self):
        return self.engine.read_last_order_per_customer()
