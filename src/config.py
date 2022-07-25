import os

class DevelopmentConfig:
    DEBUG=True
    #SQLALCHEMY_DATABASE_URI='sqlite:///heatload.db'
    #SQLALCHEMY_DATABASE_URI='sqlite:///graphql.db'
    SQLALCHEMY_DATABASE_URI='sqlite:///construction.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

Config=DevelopmentConfig

