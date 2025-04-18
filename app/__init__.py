# -*- coding: utf-8 -*-


from flask import Flask

from .auth_api import create_blueprint as create_auth_blueprint
from .auth_api.models import Permission
from .auth_api.models import Role
from .auth_api.models import User
from .routes import create_routes
from .extensions import db
from .extensions import login_manager


def create_app():
    app = Flask(__name__)
    app.secret_key = r"dev"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"

    create_routes(app)
    # 注册蓝图
    app.register_blueprint(create_auth_blueprint(), url_prefix="/api/auth")

    # 添加初始化命令
    @app.cli.command("init")
    def init() -> None:
        """初始化应用程序"""
        db.create_all()
        print("数据库表已创建")

        # 创建权限
        for name, desc in {
            "auth/account/create": "创建账户",
        }.items():
            print(f"创建权限：{name}")
            db.session.add(Permission(name=f"tusr-m:{name}", description=desc))
        # 创建角色
        for name, (desc, permissions) in {
            "admin": ("管理员", [
                "auth/account/create",
            ]),
        }.items():
            print(f"创建角色：{name}")
            db.session.add(Role(name=name, description=desc, permissions=permissions))
        # 创建用户
        db.session.add(User.create(username="admin", password="admin", roles=["admin"]))
        db.session.commit()
        print("管理员用户已创建")

    return app
