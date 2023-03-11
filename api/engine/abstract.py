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
