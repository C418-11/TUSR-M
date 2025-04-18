# -*- coding: utf-8 -*-


from flask import Flask
from flask import render_template
from flask import redirect
from flask_login import login_required


def create_routes(app: Flask):
    @app.errorhandler(404)
    def handle(_):
        return render_template("http/404.html"), 404

    @app.errorhandler(405)
    def handle(_):
        return render_template("http/405.html"), 405

    @app.route("/")
    @app.route("/dashboard")
    @login_required
    def dashboard():
        return render_template("dashboard.html")

    @app.route("/login")
    def login():
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        return redirect("api/auth/logout")


__all__ = ("create_routes",)
