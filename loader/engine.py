import csv
from io import StringIO
import logging
import zipfile


from flask_sqlalchemy import SQLAlchemy


from .mapping import MAPPING


LOGGER = logging.getLogger(__name__)


class DataLoadEngine:
    @property
    def mapping(self) -> dict:
        """
        The mapping of the load engine.
        :return: dict
        """
        if self._mapping is None:
            self._mapping = MAPPING
        return self._mapping

    @property
    def db(self) -> SQLAlchemy:
        """
        Database connection of the load engine.
        :return: SQLAlchemy
        """
        if self._db is None:
            from .models import db
            self._db = db
        return self._db

    def __init__(self, db=None, mapping=None):
        self._mapping = mapping
        self._db = db

    @classmethod
    def prepare_mapping_rule(cls, rule: dict) -> bool:
        """
        Check and extend a mapping rule. One mapping rule should have:
            * file - the CSV file from which data is read.
            * model - the database model, which is loaded from the file.
            * rename_columns - pairs of (name in file, model field name)
            * transform_columns - pairs of (model field name, transformation function)
        :param rule: dict
        :return: bool - is the rule valid
        """
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
    def fp_to_reader(cls, fp: zipfile.ZipExtFile) -> csv.DictReader:
        """
        Prepare a file descriptor from zip archive to csv.DictReader
        :param fp: zipfile.ZipExtFile
        :return: csv.DictReader
        """
        content = fp.read().decode()
        data = StringIO(content)
        return csv.DictReader(data)

    @classmethod
    def read_row(cls, row: dict, rule: dict):
        """
        Run a mapping rule over a single row from the CSV file and receive a SQLAlchemy.Model object.
        :param row: dict
        :param rule: dict
        :return:
        """
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

    def run(self, archive_file: str) -> None:
        """
        Run the loader engine with a .zip archive containing csv files.
        :param archive_file: str
        :return: None
        """

        LOGGER.info("Reading archive file: {}".format(archive_file))
        with zipfile.ZipFile(archive_file) as zf:
            for rule in self.mapping:
                if not self.prepare_mapping_rule(rule):
                    continue

                with zf.open(rule["file"]) as fp:
                    LOGGER.info("Reading from '{}' ...".format(rule["file"]))
                    ctr = 0
                    for row in self.fp_to_reader(fp):
                        entry = self.read_row(row, rule)
                        self.db.session.add(entry)
                        try:
                            self.db.session.commit()
                        except Exception as err:
                            self.db.session.rollback()
                            LOGGER.error("Error: {}".format(err))
                        else:
                            ctr += 1
                    LOGGER.info("{} records found.".format(ctr))
