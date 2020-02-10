import os

class ProductionConfig():
    DEBUG = os.getenv("DEBUG") in {"1", "yes", "true", "True"}
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


config = {
    "production": ProductionConfig,
}
