from .types import (
  UserType,
  UserRoleType,
  UserGroupType
)
from ..models import (
  User, 
  UserRole, 
  UserGroup, 
  PasswordResetCode
)
from ...sessions import current_user
from ...graphql import (
  GQLModelSchema, 
  ObjectId
)
from random import randint
from datetime import datetime
from graphene import (
  Field,
  String,
  Mutation,
  Boolean
)

class UserAccessMixin:

  def is_accessible(view, action):
    assert current_user != None, \
    "You are not logged in"
    return current_user.role.has_permission(
      view.model.__snakename__ + '.' + action
    )

class SignIn(Mutation):

  user = Field(UserType)

  class Arguments:
    email = String(required=True)
    password = String(required=True)
  
  def mutate(parent, ctx, email, password):
    user = User.authenticate(email, password)
    return SignIn(user=user)

class SignOut(Mutation):

  success = Boolean()
  
  def mutate(parent, ctx):
    if current_user:
      current_user.logout()
    return SignOut(success=True)

class ResetPassword(Mutation):
  "Creates password reset code"

  id = ObjectId()
  
  class Arguments:
    email = String(required=True)

  def mutate(root, ctx, email):
    user = User.search_by_identifier(email)
    pw_reset = None
    if user:
      reset_code = PasswordResetCode.objects(
        user=user
      ).modify(
        set__created=datetime.utcnow(),
        set__code=str(randint(10000, 99999)),
        set__user=user,
        upsert=True,
        new=True
      )
      pw_reset = reset_code.id
    return ResetPassword(id=pw_reset)


class ChangePassword(Mutation):
  "Use password reset code to change password"

  user = Field(UserType)

  class Arguments:
    code = String(required=True)
    id = ObjectId(required=True)
    password = String(required=True)
  
  def mutate(root, ctx, code, id, password):
    pw_reset = PasswordResetCode.objects.get(id=id, code=code)
    pw_reset.user.password = password
    pw_reset.user.save()
    pw_reset.delete()
    return ChangePassword(user=pw_reset.user)


class UserGQLSchema(GQLModelSchema, UserAccessMixin):

  model = User
  object_type = UserType
  me = Field(UserType)

  def resolve_me(root, ctx):
    return current_user

  sign_out = SignOut
  sign_in = SignIn
  reset_password = ResetPassword
  change_password = ChangePassword

  create_fields = [
    "*",
    "-created",
    "-email_verified",
    "!password",
    "!email",
    "-role",
    "-status",
    "-groups",
  ]

  update_fields = [
    "*",
    "-created",
    "-id",
    '-email_verified',
  ]

class UserRoleGQLSchema(GQLModelSchema, UserAccessMixin):

  model = UserRole
  object_type = UserRoleType

class UserGroupGQLSchema(GQLModelSchema, UserAccessMixin):

  model = UserGroup
  object_type = UserGroupType