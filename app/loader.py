import csv
import datetime
import logging
from zipfile import ZipFile
from app.models import db, Customer, Staff, SalesOutlet
from io import StringIO



LOGGER = logging.getLogger(__name__)
MAPPING = [
    {
        "file": "staff.csv",
        "model": Staff,
        "rename_columns": [],
        "transform_columns": [
            ("start_date", lambda x: datetime.datetime.strptime(x, "%m/%d/%Y").date()),
        ],
    },
    {
        "file": "sales_outlet.csv",
        "model": SalesOutlet,
        "rename_columns": [
            ("Neighorhood", "neighborhood"),
        ],
        "transform_columns": [
            ("manager", lambda x: None if not x else int(x)),
        ],
    },


    {
        "file": "customer.csv",
        "model": Customer,
        "rename_columns": [
            ("customer_first-name", "name"),
            ("customer_email", "email"),
        ],
        "transform_columns": [
            ("customer_since", lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").date()),
            ("birthdate", lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").date()),
        ],
    },
]


class DataLoader:
    @property
    def mapping(self):
        if self._mapping is None:
            self._mapping = MAPPING
        return self._mapping

    def __init__(self, mapping=None):
        self._mapping = mapping

    @classmethod
    def prepare_mapping_rule(cls, rule):
        if "file" not in rule:
            LOGGER.error("Missing `file` in mapping rule.")
            return False

        if "model" not in rule:
            LOGGER.error("Missing `model` in mapping rule.")
            return False

        if "rename_columns" not in rule:
            rule["rename_columns"] = []

        for pair in rule["rename_columns"]:
            if len(pair) != 2:
                LOGGER.error("Pair in 'rename_columns' should have two elements.")
                return False

        if "transform_columns" not in rule:
            rule["transform_columns"] = []

        for pair in rule["transform_columns"]:
            if len(pair) != 2:
                LOGGER.error("Pair in 'transform_columns' should have two elements.")
                return False

        rule["rename_columns"] = {c[0]: c[1] for c in rule["rename_columns"]}
        rule["transform_columns"] = {c[0]: c[1] for c in rule["transform_columns"]}

        return True

    @classmethod
    def fp_to_reader(cls, fp):
        content = fp.read().decode()
        data = StringIO(content)
        return csv.DictReader(data)

    @classmethod
    def read_row(cls, row, rule):
        kwargs = dict()
        for key, value in row.items():
            if not key:
                continue

            if key in rule["rename_columns"]:
                key = rule["rename_columns"][key]

            if key in rule["transform_columns"]:
                value = rule["transform_columns"][key](value)

            kwargs[key] = value

        return rule["model"](**kwargs)

    def run(self, archive_file):
        LOGGER.info("Reading archive file: {}".format(archive_file))
        with ZipFile(archive_file) as zf:
            for rule in self.mapping:
                if not self.prepare_mapping_rule(rule):
                    continue

                with zf.open(rule["file"]) as fp:
                    LOGGER.info("Reading from '{}' ...".format(rule["file"]))
                    for row in self.fp_to_reader(fp):
                        entry = self.read_row(row, rule)
                        db.session.add(entry)
                        try:
                            db.session.commit()
                        except Exception as err:
                            db.session.rollback()
                            LOGGER.error("Error: {}".format(err))
