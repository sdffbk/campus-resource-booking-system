import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me-for-prototype")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///booksystem.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_BOOKING_HOURS = 4
