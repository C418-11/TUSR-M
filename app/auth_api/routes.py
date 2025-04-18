# -*- coding: utf-8 -*-


from flask import Blueprint
from flask import jsonify
from flask_login import login_user
from flask_login import logout_user

from .forms import LoginForm
from .models import User


def create_routes(bp: Blueprint):
    @bp.route("/login", methods=["POST"])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user: User = User.query.filter_by(username=form.username.data).first()
            if user and user.verify_password(form.password.data):
                login_user(user)
                return jsonify({"code": 200, "msg": "登录成功"})
            return jsonify({"code": 400, "msg": "用户名或密码错误"})
        return jsonify({"code": 400, "msg": "登录失败"})

    @bp.route("/logout")
    def logout():
        logout_user()
        return jsonify({"code": 200, "msg": "登出成功"})


__all__ = (
    "create_routes",
)
