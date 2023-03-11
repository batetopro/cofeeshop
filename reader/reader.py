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

    def read_top_selling_products(self, year):
        sql = """
        SELECT p.product, SUM(r.quantity)
        FROM receipt r
        JOIN product p ON p.product_id = r.product_id
        JOIN date d ON d.transaction_date = r.transaction_date
        WHERE d.year_id = {}
        GROUP BY p.product_id
        ORDER BY SUM(quantity) DESC
        LIMIT 10
        """.format(year)

        rows = self.reader.db.session.execute(self.reader.db.text(sql))

        result = []
        for row in rows:
            result.append({
                "product_name": row[0],
                "total_sales": row[1],
            })
        return result

    def read_last_order_per_customer(self):
        sql = """
        SELECT c.customer_id, c.email, T.last_order_date
        FROM (
            SELECT 
                customer_id,
                MAX(transaction_date) AS last_order_date
            FROM receipt r
            WHERE r.customer_id IS NOT NULL
            GROUP BY customer_id
        ) T 
        JOIN customer c ON T.customer_id = c.customer_id
        ORDER BY c.customer_id ASC
        """

        rows = self.reader.db.session.execute(self.reader.db.text(sql))

        result = []
        for row in rows:
            result.append({
                "customer_id": row[0],
                "customer_email": row[1],
                "last_order_date": row[2],
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

    def read_top_selling_products(self, year):
        sql = """
        SELECT p.product, SUM(r.quantity)
        FROM receipt r
        JOIN product p ON p.product_id = r.product_id
        JOIN date d ON d.transaction_date = r.transaction_date
        WHERE d.year_id = :year
        GROUP BY p.product_id
        ORDER BY SUM(quantity) DESC
        LIMIT 10
        """

        params = dict(year=year)

        rows = self.reader.db.session.execute(self.reader.db.text(sql), params)

        result = []
        for row in rows:
            result.append({
                "product_name": row[0],
                "total_sales": row[1],
            })
        return result

    def read_last_order_per_customer(self):
        sql = """
        SELECT c.customer_id, c.email, T.last_order_date
        FROM (
            SELECT 
                customer_id,
                MAX(transaction_date) AS last_order_date
            FROM receipt r
            WHERE r.customer_id IS NOT NULL
            GROUP BY customer_id
        ) T 
        JOIN customer c ON T.customer_id = c.customer_id
        ORDER BY c.customer_id ASC
        """

        rows = self.reader.db.session.execute(self.reader.db.text(sql))

        result = []
        for row in rows:
            result.append({
                "customer_id": row[0],
                "customer_email": row[1],
                "last_order_date": row[2].strftime('%Y-%m-%d'),
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

    def read_top_selling_products(self, year):
        sql = """
        SELECT p.product, SUM(r.quantity)
        FROM receipt r
        JOIN product p ON p.product_id = r.product_id
        JOIN date d ON d.transaction_date = r.transaction_date
        WHERE d.year_id = :year
        GROUP BY p.product_id
        ORDER BY SUM(quantity) DESC
        LIMIT 10
        """

        params = dict(year=year)

        rows = self.reader.db.session.execute(self.reader.db.text(sql), params)

        result = []
        for row in rows:
            result.append({
                "product_name": row[0],
                "total_sales": row[1],
            })
        return result

    def read_last_order_per_customer(self):
        sql = """
        SELECT c.customer_id, c.email, T.last_order_date
        FROM (
            SELECT 
                customer_id,
                MAX(transaction_date) AS last_order_date
            FROM receipt r
            WHERE r.customer_id IS NOT NULL
            GROUP BY customer_id
        ) T 
        JOIN customer c ON T.customer_id = c.customer_id
        ORDER BY c.customer_id ASC
        """

        rows = self.reader.db.session.execute(self.reader.db.text(sql))

        result = []
        for row in rows:
            result.append({
                "customer_id": row[0],
                "customer_email": row[1],
                "last_order_date": row[2].strftime('%Y-%m-%d'),
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
        LOGGER.info("Reading top selling products on '{}'".format(year))
        result = self.engine.read_top_selling_products(year)
        LOGGER.info("{} records found.".format(len(result)))
        return result

    def read_last_order_per_customer(self):
        LOGGER.info("Reading last order per customer.")
        result = self.engine.read_last_order_per_customer()
        LOGGER.info("{} records found.".format(len(result)))
        return result
