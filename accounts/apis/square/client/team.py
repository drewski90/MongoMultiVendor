from typing import List, Any
from pydantic import constr, conint
from .error import request_wrapper
from .utils import APIModel, APIWrapper, Model
from uuid import uuid4
from .money import Money
from .patterns import (
  EMAIL_PATTERN,
  RFC_3339_PATTERN,
)
from .enums import (
  SquareStatusEnum, 
  SquareJobAssignmentPayTypeEnum,
  SquareJobAssignmentTypeEnum
)

class JobAssignment(Model):

  job_title:constr(
    strip_whitespace=True,
    strict=True
    )=None
  pay_type:SquareJobAssignmentPayTypeEnum=None
  hourly_rate:Money=None
  annual_rate:Money=None
  weekly_hours:int=None

class WageSetting(APIModel):

  team_member_id:str
  job_assignments:List[JobAssignment]=None
  is_overtime_exempt:bool=False
  created_at:str=None
  updated_at:str=None
  version:int=None

  def update(self):
    body = request_wrapper(
      self.api.update_wage_setting,
      team_member_id=self.team_member_id,
      body=dict(wage_setting=self.update_fields)
    )
    self.refresh(**body['wage_setting'])
    return self


class AssignedLocations(Model):

  assignment_type:SquareJobAssignmentTypeEnum=None
  location_ids:List[str]=[]

class TeamMember(APIModel):

  _edit_fields_ = {
    "status":True,
    "reference_id":True,
    "given_name":True,
    "family_name":True,
    "email_address":True,
    "phone_number":True,
    "assigned_locations":True,
  }

  id:str=None
  reference_id:constr(
    strip_whitespace=True,
    strict=True
    )=None
  is_owner:bool=False
  status:SquareStatusEnum=None
  given_name:constr(
    strip_whitespace=True,
    strict=True
    )=None
  family_name:constr(
    strip_whitespace=True,
    strict=True
    )=None
  email_address:constr(
    to_lower=True,
    regex=EMAIL_PATTERN,
    strip_whitespace=True,
    strict=True
    )=None
  phone_number:constr(
    strip_whitespace=True,
    max_length=17,
    )=None
  created_at:constr(
    strip_whitespace=True, 
    regex=RFC_3339_PATTERN
    )=None
  updated_at:constr(
    strip_whitespace=True, 
    regex=RFC_3339_PATTERN
    )=None
  assigned_locations:AssignedLocations=None

  def update(self):
    body = request_wrapper(
      self.api.update_team_member,
      team_member_id=self.id,
      body={"team_member": self.update_fields}
    )
    self.refresh(**body['team_member'])
    return self

  def save(self, idempotency_key:str=None):
    if self.id is not None:
      return self.update()
    assert idempotency_key is not None, \
      "idempotency_key cannot be none "
    body = request_wrapper(
      self.api.create_team_member,
      body={
        "idempotency_key": idempotency_key,
        "team_member": self.update_fields
      }
    )
    self.refresh(**body['team_member'])
    return self

  def update_wage_setting(
      self,
      job_assignments:List[JobAssignment]=None,
      is_overtime_exempt:bool=None
    ) -> WageSetting:
    setting = WageSetting(
      api_wrapper=self.api_wrapper,
      team_member_id=self.id,
      job_assignments=job_assignments,
      is_overtime_exempt=is_overtime_exempt
    )
    setting.save()
    return setting

  def wage_setting(self) -> WageSetting:
    body = request_wrapper(
      self.api.retrieve_wage_setting,
      team_member_id=self.id
    )
    return WageSetting(
      api_wrapper=self.api_wrapper,
      **body['wage_setting']
    )

class TeamMembers(APIWrapper):

  api_name = "team"

  def create(
    self, 
    idempotency_key:str,
    status:str=None,
    reference_id:str=None,
    given_name:str=None,
    family_name:str=None,
    email_address:str=None,
    phone_number:str=None,
    assigned_locations:str=None
    ) -> TeamMember:
    member = TeamMember(
      api_wrapper=self,
      status=status,
      reference_id=reference_id,
      given_name=given_name,
      family_name=family_name,
      email_address=email_address,
      phone_number=phone_number,
      assigned_locations=assigned_locations
    )
    member.save(idempotency_key=idempotency_key)
    return member

  def update(
    self,
    id,
    status:str=None,
    reference_id:str=None,
    given_name:str=None,
    family_name:str=None,
    email_address:str=None,
    phone_number:str=None,
    assigned_locations:str=None,
  ) -> TeamMember:
    member = TeamMember(
      api_wrapper=self,
      id=id, 
      status=status,
      reference_id=reference_id,
      given_name=given_name,
      family_name=family_name,
      email_address=email_address,
      phone_number=phone_number,
      assigned_locations=assigned_locations
    )
    member.update()
    return member

  def list(
      self, 
      status:str=None, 
      location_ids:List[str]=None, 
      is_owner:bool=None
    ) -> List[TeamMember]:
    body = {}
    body['query'] = {}
    body['query']['filter'] = {
      "location_ids": location_ids,
      "status": status,
      "is_owner": is_owner
    }
    body = request_wrapper(
      self.api.search_team_members,
      body=body
    )
    if 'team_members' in body:
      return [
        TeamMember(api_wrapper=self, **m) 
        for m in body['team_members']
      ]
    return []

  def retrieve(
    self, 
    team_member_id:str
    ) -> TeamMember:
    body = request_wrapper(
      self.api.retrieve_team_member,
      team_member_id=team_member_id
    )
    return TeamMember(
      api_wrapper=self,
      **body['team_member']
    )

  def update_wage_setting(
    self, 
    team_member_id:str, 
    job_assignments:List[JobAssignment]=None,
    is_overtime_exempt:bool=False
    ) -> WageSetting:
    setting = WageSetting(
      api_wrapper=self,
      team_member_id=team_member_id,
      job_assignments=job_assignments,
      is_overtime_exempt=is_overtime_exempt
    )
    setting.save()
    return setting
  
  def retrieve_wage_setting(
    self,
    team_member_id:str
  ):
    body = request_wrapper(
      self.api.retrieve_wage_setting,
      team_member_id=team_member_id
    )
    return WageSetting(
      api_wrapper=self.api_wrapper,
      **body['wage_setting']
    )

