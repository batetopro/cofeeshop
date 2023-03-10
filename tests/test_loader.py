import os
import unittest
from app.loader import DataLoader
from app.models import Test, db


class LoaderTest(unittest.TestCase):
    def test_simple(self):
        mapping = [
            {
                "file": "test.csv",
                "model": Test,
                "rename_columns": [
                    ("id_2", "square"),
                ],
                "transform_columns": [
                    ("square", lambda x: int(x) * int(x)),
                ],
            },
        ]
        loader = DataLoader(mapping=mapping, db=db)

        archive = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "test.zip")
        loader.run(archive)

        ctr = 0
        for item in Test.query.all():
            ctr += 1
            self.assertEqual(item.id * item.id, item.square)
            db.session.delete(item)

        db.session.commit()
        self.assertEqual(ctr, 5)


if __name__ == "__main__":
    unittest.main()
