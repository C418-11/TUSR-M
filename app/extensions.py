# -*- coding: utf-8 -*-
# cython: language_level = 3


from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()

__all__ = (
    "db",
    "login_manager",
)
