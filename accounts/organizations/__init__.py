from ..users import ADMIN_CATEGORY
from ..admin import Admin
from ..sessions import (
  account_loader,
  organization_loader,
  user_loader,
  Accounts,
  current_user
)
from .admin import (
  OrganizationView,
  BusinessAddressView,
  AccountView,
  AccountRoleView,
  AccountGroupView,
  AccountPermissionView
)

from .models import (
  Organization,
  Account,
  AccountGroup, 
  AccountRole,
  AccountPermission,
  BusinessAddress
)
from . import graphql
from flask import session, request

@organization_loader
def load_organization():
  org_id = request.view_args.get('organization_id')
  if org_id:
    return Organization.objects(id=org_id).first()

@account_loader
def load_account_from_session():
  organization_id = request.view_args.get('organization_id')
  if organization_id and current_user != None: 
    return Account.objects(
      user=current_user.id, 
      organization=organization_id
    ).first()

ADMIN_CATEGORY = "Organizations"

Admin.add_views(
  OrganizationView(
    Organization,
    category=ADMIN_CATEGORY,
    name="Organizations"
  ),
  BusinessAddressView(
    BusinessAddress,
    category=ADMIN_CATEGORY,
    name="Addresss"
  ),
  AccountView(
    Account,
    category=ADMIN_CATEGORY,
    name="Accounts"
  ),
  AccountGroupView(
    AccountGroup,
    category=ADMIN_CATEGORY,
    name="Groups"
  ),
  AccountRoleView(
    AccountRole,
    category=ADMIN_CATEGORY,
    name="Roles"
  ),
  AccountPermissionView(
    AccountPermission,
    category=ADMIN_CATEGORY,
    name="Permissions"
  )
)

__all__ = [
  "Organization",
  "Account",
  "AccountGroup", 
  "OrganizationAccountGroup",
  "AccountRole", 
  "OrganizationAccountRole",
  "current_organization"
]