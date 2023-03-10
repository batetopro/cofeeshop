import datetime
import unittest
from app.reader import DataReader
from app import db


class ReaderTest(unittest.TestCase):
    def test_birthdates(self):
        reader = DataReader(db=db)
        birthdays = reader.read_birthdays(datetime.date.fromtimestamp(1678468782))
        self.assertEqual(birthdays[0]["customer_id"], 35)
        self.assertEqual(birthdays[1]["customer_id"], 5245)
        self.assertEqual(birthdays[2]["customer_id"], 5425)
        self.assertEqual(birthdays[3]["customer_id"], 5494)
        self.assertEqual(birthdays[4]["customer_id"], 5778)
        self.assertEqual(birthdays[5]["customer_id"], 8418)
        self.assertEqual(len(birthdays), 6)



if __name__ == "__main__":
    unittest.main()
