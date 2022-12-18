from graphene import (
  String,
  ObjectType,
  Int,
  ID,
  Boolean,
  List
)

class SquareSubscriptionPhaseType(ObjectType):

  id = ID()
  interval = String()
  price = Int()
  currency = String()
  ordinal = Int()

  def resolve_id(r, c): return r['uid']
  def resolve_interval(r, c): return r['cadence']
  def resolve_price(r, c): return r['recurring_price_money']['amount']
  def resolve_currency(r, c): return r['recurring_price_money']['currency']

class SquareSubcriptionPlanType(ObjectType):

  id = ID()
  updated = String()
  created = String()
  version = Int()
  deleted = Boolean()
  present_at_all_locations = Boolean()
  name = String()
  phases = List(SquareSubscriptionPhaseType)

  def resolve_updated(r, c): return r['updated_at']
  def resolve_created(r, c): return r['created_at']
  def resolve_version(r, c): return r['version']
  def resolve_deleted(r, c): return r['is_deleted']
  def resolve_name(r, c): return r['subscription_plan_data']['name']
  def resolve_phases(r, c): return r['subscription_plan_data']['phases']

