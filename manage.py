import os
import sys
import pytest
from flask.cli import FlaskGroup
from flask_migrate import Migrate
from app import flask_app
from app.plugins import db
# flake8: noqa
from app.seed.seed import seed


manager = FlaskGroup(flask_app)

migrate = Migrate()
migrate.init_app(flask_app, db)

@manager.command('formatter', with_appcontext=False)
def code_formatter():
    os.system("black app/ manage.py --skip-string-normalization --line-length 79")

@manager.command('test', with_appcontext=False)
def test():
    return pytest.main(['-v', './app/test'])

@manager.command('seed', with_appcontext=False)
def create_seed():
    seed()

@manager.command('run_docker', with_appcontext=False)
def create_docker_db_production():
    os.system(f"docker run --name {os.environ.get('PRODUCTION_DB_NAME')} -e POSTGRES_PASSWORD={os.environ.get('PRODUCTION_DB_PASSWORD')} -p 5432:5432 -d postgres")

if __name__ == '__main__':
        manager()
