from ..admin import Admin
from .models import (
  BaseUser,
  User,
  BaseGroup,
  UserGroup,
  BaseRole,
  UserRole,
  UserPermission,
  Permission,
  Address
)
from .admin import (
  UserAuthView,
  UserView,
  RoleView,
  UserGroupView,
  UserPermissionView,
  UserModelView
)
from . import graphql

ADMIN_CATEGORY = "Users"

Admin.add_views(
  UserAuthView(
    category=ADMIN_CATEGORY,
    name="My Account"
  ),
  UserView(
    User,
    category=ADMIN_CATEGORY,
    name="Users"
  ),
  RoleView(
    UserRole,
    category=ADMIN_CATEGORY,
    name="Roles"
  ),
  UserGroupView(
    UserGroup,
    category=ADMIN_CATEGORY,
    name="Groups"
  ),
  UserPermissionView(
    UserPermission,
    category=ADMIN_CATEGORY,
    name="Permissions"
  )
)


__all__ = [
  "UserModelView",
  "User",
  "UserAddress",
  "Address",
  "BaseGroup",
  "UserGroup",
  "BaseRole",
  "UserRole",
  "BaseUser",
  "Permission",
]