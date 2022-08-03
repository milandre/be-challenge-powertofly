import os

import click
from flask_redoc import Redoc

from app import create_app
from app.api.models import User, db
from config import config

# Flask config setup and create app
flask_config = os.getenv('FLASK_CONFIG')
app = create_app(flask_config or 'default')

# ReDoc documentation for API
redoc = Redoc(app, '../redoc/bechallenge.yml')


@app.cli.command("test")
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Run the unit tests."""
    import unittest

    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command("recreate-db")
def recreate_db():
    """
    Recreates a local database.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


@app.cli.command("add-fake-data")
@click.option('-n', '--number-users', default=10, type=int, help='Number of each model type to create')
def add_fake_data(number_users):
    """
    Adds fake data to the database.
    """
    print(f'Add {number_users} testing users to the database')
    User.generate_fake_users(number_users)


@app.cli.command("setup-dev")
def setup_dev():
    """Runs the set-up needed for local development."""
    setup_general()


@app.cli.command("setup-prod")
def setup_prod():
    """Runs the set-up needed for production."""
    setup_general()


def setup_general():
    """Runs the set-up needed for both local development and production.
    Also sets up first user."""
    if User.query.filter_by(email=config[flask_config].EXAMPLE_EMAIL_USER).first() is None:
        user = User(email=config[flask_config].EXAMPLE_EMAIL_USER, first_name='Example', last_name='Account')
        db.session.add(user)
        db.session.commit()
        print(f'Added example user: {user.full_name()}')


if __name__ == "__main__":
    app.run(debug=os.getenv('DEBUG') or False, host="0.0.0.0")
