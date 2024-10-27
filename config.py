import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///sge_py.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'testandojwt'