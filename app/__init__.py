from logging.config import dictConfig

from flask import Flask
import click
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.cli import with_appcontext


from .config import Config


dictConfig(Config.LOGGING)


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import routes, models


@click.command(name='load_data')
@with_appcontext
def load_data():
    from .loader import DataLoader
    loader = DataLoader()
    loader.run(Config.DATASET_ARCHIVE)


@click.command(name='tests')
@with_appcontext
def run_tests():
    import unittest
    tests = unittest.TestLoader().discover('tests')

    test_runner = unittest.TextTestRunner()
    test_runner.run(tests)


app.cli.add_command(load_data)
app.cli.add_command(run_tests)
