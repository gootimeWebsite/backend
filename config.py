from datetime import timedelta
SECRET_KEY = "I_LOVE_PYTHON_NMSL"
PERMANENT_SESSION_LIFETIME = timedelta(days=7)

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root12345@localhost:3306/gooTimeWebsite?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_POOL_RECYCLE = 3600
