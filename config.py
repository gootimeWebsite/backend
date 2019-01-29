from datetime import timedelta

CSRF_ENABLED = True
SECRET_KEY = "I_LOVE_PYTHON_NMSL"

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root12345@localhost:3306/gooTimeWebsite?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_POOL_RECYCLE = 3600
