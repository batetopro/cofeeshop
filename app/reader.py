





class SqliteReader:
    def read_birthdays(self, date):
        sql = """
        SELECT customer_id, name
        FROM customer
        WHERE strftime('%d %m', birthdate) = '? ?'
        """

