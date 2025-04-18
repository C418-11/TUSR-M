# -*- coding: utf-8 -*-


from typing import Never, Optional
from typing import Self

from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from ..extensions import db

# 用户-角色关联表（多对多）
user_roles = db.Table(
    "user_roles",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id"))
)

# 角色-权限关联表（多对多）
role_permissions = db.Table(
    "role_permissions",
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id")),
    db.Column("permission_id", db.Integer, db.ForeignKey("permissions.id"))
)


class User(db.Model, UserMixin):
    """
    用户模型
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    active = db.Column(db.Boolean, default=True)

    # 关联角色（多对多）
    roles = db.relationship("Role",
                            secondary=user_roles,
                            backref=db.backref("users", lazy="dynamic"))

    @classmethod
    def create(cls, username: str, password: str, roles: Optional[list[str]] = None) -> Self:
        """
        创建用户

        :param username: 用户名
        :type username: str
        :param password: 密码
        :type password: str
        :param roles: 角色
        :type roles: list[str]

        :return: 用户对象
        :rtype: Self
        """
        user = cls()
        user.username = username
        user.password = password
        if roles:
            user.roles = [Role.query.filter_by(name=name).first() for name in roles]
        return user

    @property
    def password(self) -> Never:
        """
        密码字段，只写
        """
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password: str) -> None:
        """
        设置密码

        :param password: 密码
        :type password: str
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        """
        验证密码

        :param password: 密码
        :type password: str

        :return: 密码是否正确
        :rtype: bool
        """
        return check_password_hash(self.password_hash, password)

    def has_permission(self, permission_name) -> bool:
        """
        检查用户是否拥有某个权限

        :param permission_name: 权限名称
        :type permission_name: str

        :return: 是否拥有权限
        :rtype: bool
        """
        return any(role.has_permission(permission_name) for role in self.roles)


class Role(db.Model):
    """
    角色模型
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(256))

    # 关联权限（多对多）
    permissions = db.relationship("Permission",
                                  secondary=role_permissions,
                                  backref=db.backref("roles", lazy="dynamic"))

    def has_permission(self, permission_name: str):
        """
        检查角色是否拥有某个权限

        :param permission_name: 权限名称
        :type permission_name: str

        :return: 是否拥有权限
        :rtype: bool
        """
        return any(perm.name == permission_name for perm in self.permissions)


class Permission(db.Model):
    """
    权限模型
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "permissions"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(256))


__all__ = (
    "user_roles",
    "role_permissions",
    "User",
    "Role",
    "Permission",
)
