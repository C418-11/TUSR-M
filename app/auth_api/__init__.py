# -*- coding: utf-8 -*-


from flask import Blueprint

from .models import User
from .routes import create_routes
from ..extensions import login_manager


def create_blueprint():
    blueprint = Blueprint("auth-api", __name__, template_folder="templates")

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    create_routes(blueprint)
    return blueprint


__all__ = (
    "create_blueprint",
)
