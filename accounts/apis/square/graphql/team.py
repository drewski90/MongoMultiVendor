from graphene import (
  ObjectType,
  List,
  String,
  Boolean,
  Field,
  Argument,
  InputObjectType,
  ID,
  Mutation,
  Int
)
from .money import (
  SquareMoneyType,
  SquareMoneyInput
)
from .enums import ENUMS
from ..client.merchant import square_merchant
from ....sessions import (
  current_account, 
  current_user,
  account_loaded
)

class TeamMember:

  class SquareAssignedLocationsType(ObjectType):
    assignment_type = String()
    location_ids = List(String)

  id = ID()
  reference_id = String()
  is_owner = Boolean()
  status = String()
  given_name = String()
  family_name = String()
  email_address = String()
  phone_number = String()
  assigned_locations = Field(SquareAssignedLocationsType)
  status = String()

class SquareWageSettingType(ObjectType):

  class SquareJobAssignmentType(ObjectType):

    job_title=String()
    pay_type=String()
    hourly_rate=Field(SquareMoneyType)
    annual_rate=Field(SquareMoneyType)
    weekly_hours=Int()

  team_member_id = ID()
  job_assignments=List(SquareJobAssignmentType)
  is_overtime_exempt = Boolean()
  created_at = String()
  updated_at = String()
  version = Int()

class SquareTeamMemberType(ObjectType, TeamMember):

  id = String()
  created_at = String()
  updated_at = String()
  wage_setting = Field(SquareWageSettingType)

  @account_loaded
  def resolve_wage_setting(root, ctx):
    if not root.email_address == current_user.email:
      current_account.assert_permission('square.read_team_member_wage_setting')
    return root.wage_setting()


class SquareTeamMemberInput(InputObjectType, TeamMember):
  class SquareAssignedLocationsInput(InputObjectType):
    assignment_type = String()
    location_ids = List(String)
  id = ID()
  status = Argument(ENUMS.SquareStatusEnum)
  assigned_locations = List(SquareAssignedLocationsInput)

class SquareTeamFilterInput(InputObjectType):
  status = String()
  location_ids = List(ID) 
  is_owner = Boolean()

class SquareCreateTeamMember(Mutation):
  
  team_member = Field(SquareTeamMemberType)

  class Arguments:
    idempotency_key = String()
    team_member = SquareTeamMemberInput(required=True)

  @classmethod
  @account_loaded
  def mutate(cls, root, ctx, team_member, idempotency_key):
    current_account.assert_permission('square.create_team_member')
    member = square_merchant.team.create(
      idempotency_key=idempotency_key,
      **team_member
    )
    return SquareCreateTeamMember(
      team_member=member
    )

class SquareUpdateTeamMember(Mutation):
  
  team_member = Field(SquareTeamMemberType)

  class Arguments:
    team_member = SquareTeamMemberInput(required=True)

  @classmethod
  @account_loaded
  def mutate(cls, root, ctx, team_member):
    current_account.assert_permission('square.update_team_member')
    member = square_merchant.team.update(
      **team_member
    )
    return SquareCreateTeamMember(
      team_member=member
    )

class SquareWageSettingInput(InputObjectType):

  class SquareJobAssignmentInput(InputObjectType):

    job_title=String()
    pay_type=String()
    hourly_rate=Field(SquareMoneyInput)
    annual_rate=Field(SquareMoneyInput)
    weekly_hours=Int()

  team_member_id = ID()
  job_assignments=List(SquareJobAssignmentInput)
  is_overtime_exempt = Boolean()

class SquareUpdateWageSetting(Mutation):

  wage_setting = Field(SquareWageSettingType)

  class Arguments:

    wage_setting = SquareWageSettingInput(required=True)

  @classmethod
  @account_loaded
  def mutate(cls, root, ctx, wage_setting):
    current_account.assert_permission('square.update_team_member_wage_setting')
    wage_setting = square_merchant.team.update_wage_setting(
      **wage_setting
    )
    return cls(wage_setting=wage_setting)