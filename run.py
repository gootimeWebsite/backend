# -*- coding: UTF-8 -*-
from flask import current_app
from flask.cli import FlaskGroup, run_command
from flask_sqlalchemy import SQLAlchemy
from werkzeug.contrib.fixers import ProxyFix
from code import interact
from getpass import getpass

from app import app, db
from app.models import User, Messages
from app.article.models import Article, ArticleRole
from app.forum.models import Forum, ForumRole
import config

import click
import os
import sys

app.wsgi_app = ProxyFix(app.wsgi_app)

cli = FlaskGroup(add_default_commands=False, create_app=lambda r: app)
cli.add_command(run_command)

try:
    from flask_migrate import Migrate
    migrate = Migrate(app, db)
except ImportError:
    pass


@cli.command('shell', short_help='Starts an interactive shell.')
def shell_command():
    ctx = dict(
        app=app, db=db, User=User, Messages=Messages, Article=Article, Forum=Forum,
        run=run, test=test
    )
    banner = 'Python %s on %s\n%s' % (
        sys.version,
        sys.platform,
        app.config['SHELL_BANNER'],
    )
    interact(banner=banner, local=ctx, exitmsg=app.config['SHELL_EXITMSG'])


def run(host="0.0.0.0", port=80):
    app.run(host=host, port=port)


@cli.command()
@click.option('-d', '--debug', default=True, type=bool, help='If open debug mode?')
@click.option('-h', '--host', default='0.0.0.0', type=str, help='The host?')
@click.option('-p', '--port', default=80, type=int, help='The port?')
def runserver(debug, host, port):
    app.run(debug = debug, host = host, port = port)


@cli.command()
@click.option('-u', '--username', type=str, help='The database username?')
@click.option('-p', '--password', type=str, help='The database password?')
def connectdb(username, password):
    with open('config.py', 'r') as f:
        lines = f.readlines()
    f.close()
    conf = []
    for line in lines:
        if line.find("SQL_USERNAME =") != -1 and username:
            line = "SQL_USERNAME = \"" + username + "\"\n"
        elif line.find("SQL_PASSWORD =") != -1 and password:
            line = "SQL_PASSWORD = \"" + password + "\"\n"
        conf.append(line)
    with open('config.py', 'w') as f:
        f.writelines(conf)
    f.close()


@cli.command()
def initdb():
    app.config.from_pyfile('config.py', silent=True)
    db.init_app(app)
    db.drop_all()
    db.create_all()
    init_perm()
    init_admin()
    init_user()


def init_perm():
    ForumRole.insert_roles()
    ArticleRole.insert_roles()


def init_admin():
    admin = User(username="admin", phonenumber="12345678910", forum_roleID=2, article_roleID=2)
    db.session.add(admin)
    db.session.commit()


def init_user():
    user = User(username="Tel72250567", phonenumber="17799163760", forum_roleID=1, article_roleID=1)
    db.session.add(user)
    db.session.commit()


@cli.command()
@click.option('-c', '--coverage', default='False', type=bool, help='If use coverage tool and make report?')
def test(coverage):
    os.system("coverage run test.py")
    if coverage:
        os.system("coverage report")
        os.system("coverage html")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        app.run(debug = True, host = "0.0.0.0", port = 80)
    else:
        cli.main()
