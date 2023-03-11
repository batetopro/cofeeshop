import datetime
import unittest
from app.reader import DataReader


class ReaderTest(unittest.TestCase):
    def test_birthdates(self):
        reader = DataReader()
        birthdays = reader.read_birthdays(datetime.date.fromtimestamp(1678468782))
        self.assertEqual(birthdays[0]["customer_id"], 35)
        self.assertEqual(birthdays[1]["customer_id"], 5245)
        self.assertEqual(birthdays[2]["customer_id"], 5425)
        self.assertEqual(birthdays[3]["customer_id"], 5494)
        self.assertEqual(birthdays[4]["customer_id"], 5778)
        self.assertEqual(birthdays[5]["customer_id"], 8418)
        self.assertEqual(len(birthdays), 6)

    def test_top_selling_products(self):
        reader = DataReader()
        products = reader.read_top_selling_products(2019)
        self.assertEqual(products[0]["product_name"], 'Earl Grey Rg')
        self.assertEqual(products[1]["product_name"], 'Dark chocolate Lg')
        self.assertEqual(products[2]["product_name"], 'Latte')
        self.assertEqual(products[3]["product_name"], 'Morning Sunrise Chai Rg')
        self.assertEqual(len(products), 10)

    def test_last_order_per_customer(self):
        reader = DataReader()
        users = reader.read_last_order_per_customer()
        self.assertEqual(len(users), 2245)
        self.assertEqual(users[0]["customer_id"], 1)
        self.assertEqual(users[0]["customer_email"], "Venus@adipiscing.edu")
        self.assertEqual(users[0]["last_order_date"], "2019-04-29")


if __name__ == "__main__":
    unittest.main()
