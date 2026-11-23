import os

from dotenv import load_dotenv


load_dotenv()


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "handwritten-notes-secret"
    )

    DB_HOST = os.getenv(
        "DB_HOST",
        "127.0.0.1"
    )

    DB_PORT = os.getenv(
        "DB_PORT",
        "3306"
    )

    DB_USER = os.getenv(
        "DB_USER",
        "root"
    )

    DB_PASSWORD = os.getenv(
        "DB_PASSWORD",
        ""
    )

    DB_NAME = os.getenv(
        "DB_NAME",
        "handwritten_notes"
    )

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://"
        f"{DB_USER}:{DB_PASSWORD}@"
        f"{DB_HOST}:{DB_PORT}/"
        f"{DB_NAME}"
        f"?charset=utf8"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)
        ),
        "uploads"
    )

    MAX_CONTENT_LENGTH = 20 * 1024 * 1024