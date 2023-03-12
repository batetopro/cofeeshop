import datetime
from typing import List


from sqlalchemy import text


from .abstract import ReaderEngine
from ..schemas import Birthday, TopSellingProduct, LastOrderPerCustomer


class MySQLEngine(ReaderEngine):
    def read_birthdays(self, date:datetime.date) -> List[Birthday]:
        """
        Get list of customers, which have birthday on the given date.
        :param date: datetime.date
        :return: List[Birthday]
        """

        sql = """
        SELECT customer_id, name
        FROM customer
        WHERE MONTH(birthdate) = :month
            AND DAYOFMONTH(birthdate) = :day
        ORDER BY customer_id ASC 
        """
        params = dict(day=date.day, month=date.month)

        rows = self.reader.session.execute(text(sql), params)

        result = []
        for row in rows:
            result.append(Birthday(
                customer_id=row[0],
                customer_first_name=row[1]
            ))
        return result

    def read_top_selling_products(self, year:int) -> List[TopSellingProduct]:
        """
        The top 10 selling products for a specific year.
        :param year: int
        :return: List[TopSellingProduct]
        """

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

        rows = self.reader.session.execute(text(sql), params)

        result = []
        for row in rows:
            result.append(TopSellingProduct(
                product_name=row[0],
                total_sales=row[1]
            ))
        return result

    def read_last_order_per_customer(self) -> List[LastOrderPerCustomer]:
        """
        The last order per customer with their email.
        :return: List[LastOrderPerCustomer]
        """
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

        rows = self.reader.session.execute(text(sql))

        result = []
        for row in rows:
            result.append(LastOrderPerCustomer(
                customer_id=row[0],
                customer_email=row[1],
                last_order_date=row[2].strftime('%Y-%m-%d')
            ))
        return result
