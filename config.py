from datetime import timedelta

CSRF_ENABLED = True
SECRET_KEY = "I_LOVE_PYTHON_NMSL"
LIFE_TIME = 7200
LONG_LIFE_TIME = 2592000

SQL_HOSTNAME = "localhost"
SQL_PORT = "3306"
SQL_DATABASE = "gooTimeWebsite"
SQL_USERNAME = "root"
SQL_PASSWORD = "root12345"

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8mb4'.\
    format(username=SQL_USERNAME, password=SQL_PASSWORD, host=SQL_HOSTNAME, port=SQL_PORT, db=SQL_DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_POOL_RECYCLE = 3600

SHELL_BANNER = """===================================================
Welcome to gooTime Interactive Shell!
Here, you can explore and manage with gooTime backend :)
---------------------------------------------------
Enjoy!"""

SHELL_EXITMSG = """Thank you for using!
Have a good day!
==================================================="""
