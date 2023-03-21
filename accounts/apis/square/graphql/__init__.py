from .customers import (
  SquareCustomerResultsType,
  SquareCustomerType,
  SquareCustomerFilterInput,
  SquareCustomersPaginationInput,
  SquareCreateCustomer,
  SquareUpdateCustomer,
  SquareDeleteCustomer,
  SquareRemoveGroupFromCustomer,
  SquareAddGroupToCustomer
)
from .locations import (
  SquareLocationType,
  SquareCreateLocation,
  SquareUpdateLocation
)
from .cards import (
  SquareCardResultsType,
  SquareCardType,
  SquareCardsPaginationInput,
  SquareCreateCard,
  SquareDisableCard,
  SquareCardFilterInput
)
from .team import (
  SquareTeamMemberType,
  SquareCreateTeamMember,
  SquareUpdateTeamMember,
  SquareUpdateWageSetting,
  SquareTeamFilterInput,
  SquareWageSettingType
)
from .bookings import (
  SquareAvailableBookingType,
  SquareBookingResultsType,
  SquareBookingType,
  SquareAppointmentSearchFilterInput,
  SquareBookingsPaginationInput,
  SquareBookingsFilterInput,
  SquareCreateBooking,
  SquareUpdateBooking,
  SquareCancelBooking
)
from .catalog import (
  SquareCatalogObjectsFilterInput,
  SquareCatalogItemsFilterInput,
  SquareCatalogItemsPaginationInput,
  SquareCatalogObjectsPaginationInput,
  SquareCatalogObjectsResultsType,
  SquareCatalogResultType,
  SquareCatalogItemsResultsType,
  SquareCatalogInfoType,
  SquareCatalogBatchUpsert,
  SquareCatalogBatchDelete,
  SquareCatalogUpdateItemModifierLists,
  SquareCatalogUpdateItemTaxes,
  OBJECT_TYPES
)
from .payments import (
  SquarePaymentType,
  SquareCreatePayment,
  SquareUpdatePayment,
  SquareCancelPayment,
  SquareCompletePayment,
  SquarePaymentsFilterInput,
  SquarePaymentsPaginationInput,
  SquarePaymentResultsType
)
from .groups import (
  SquareCustomerGroupResults,
  SquareCustomerGroupPaginationInput,
  SquareCustomerGroupType,
  SquareCreateCustomerGroup,
  SquareUpdateCustomerGroup,
  SquareDeleteCustomerGroup
)
from ..client import test_client
from ....sessions import (
  current_org,
  current_account,
  current_user,
  account_loaded
)
from ....graphql import Graph
from graphene import (
  ObjectType, 
  Field,
  List,
  String,
  ID,
  Boolean,
  Int
)

class SquareQueries(ObjectType):
  application_id = String()
  oauth = String()
  customers = Field(
    SquareCustomerResultsType, 
    filter=SquareCustomerFilterInput(),
    pagination=SquareCustomersPaginationInput()
  )
  customer = Field(
    SquareCustomerType,
    customer_id = ID(required=True)
  )
  customer_groups = Field(
    SquareCustomerGroupResults,
    pagination=SquareCustomerGroupPaginationInput()
  )
  customer_group = Field(
    SquareCustomerGroupType,
    group_id=ID(required=True)
  )
  cards = Field(
    SquareCardResultsType,
    filter=SquareCardFilterInput(),
    pagination=SquareCardsPaginationInput()
  )
  card = Field(
    SquareCardType,
    card_id = ID(required=True)
  )
  team = List(
    SquareTeamMemberType,
    filter=SquareTeamFilterInput()
  )
  wage_setting = Field(
    SquareWageSettingType
  )
  team_member = Field(
    SquareTeamMemberType, 
    team_member_id=ID(required=True)
  )
  locations = List(
    SquareLocationType
  )
  location = Field(
    SquareLocationType, 
    location_id=ID(required=True)
  )
  availability = List(
    SquareAvailableBookingType,
    filter=SquareAppointmentSearchFilterInput()
  )
  bookings = Field(
    SquareBookingResultsType,
    filter=SquareBookingsFilterInput(),
    pagination=SquareBookingsPaginationInput()
  )
  booking = Field(
    SquareBookingType,
    booking_id=ID(required=True)
  )
  catalog_objects = Field(
    SquareCatalogObjectsResultsType,
    filter=SquareCatalogObjectsFilterInput(),
    pagination=SquareCatalogObjectsPaginationInput()
  )
  catalog_info = Field(SquareCatalogInfoType)
  catalog_items = Field(
    SquareCatalogItemsResultsType,
    filter=SquareCatalogItemsFilterInput(),
    pagination=SquareCatalogItemsPaginationInput()
  )
  catalog_object = Field(
    SquareCatalogResultType,
    object_id=String(required=True),
    include_related_objects=Boolean(),
    catalog_version=Int()
    )
  payments = Field(
    SquarePaymentResultsType,
    filter=SquarePaymentsFilterInput(),
    pagination=SquarePaymentsPaginationInput()
  )
  payment = Field(
    SquarePaymentType,
    payment_id=ID(required=True)
  )

  @account_loaded
  def resolve_oauth(root, ctx):
    current_account.assert_permission('square.oauth_authorize')
    if current_org != None:
      return root.oauth.oauth_uri(
        str(current_org.id), 
        "http://something.com"
      )

  def resolve_application_id(root, ctx):
    return root.application_id

  @account_loaded
  def resolve_cards(root, ctx, filter={}, pagination={}):
    current_account.assert_permission('square.read_cards')
    return root.cards.list(**filter, **pagination)

  @account_loaded
  def resolve_card(root, ctx, card_id):
    current_account.assert_permission('square.read_cards')
    return root.cards.retrive(card_id)

  @account_loaded
  def resolve_customers(root, ctx, filter={}, pagination={}):
    current_account.assert_permission('square.read_customers')
    return root.customers.list(**filter, **pagination)
  
  @account_loaded
  def resolve_customer(root, ctx, customer_id):
    current_account.assert_permission('square.read_customers')
    return root.customers.retrieve(customer_id)

  @account_loaded
  def resolve_customer_groups(root, ctx, pagination={}):
    current_account.assert_permission('square.read_customer_groups')
    return root.customer_groups.list(**pagination)

  @account_loaded
  def resolve_customer_group(root, ctx, group_id):
    current_account.assert_permission('square.read_customer_groups')
    return root.customer_groups.retrieve(group_id)

  def resolve_team(root, ctx, filter={}):
    print(filter)
    return root.team.list(**filter)

  def resolve_team_member(root, ctx, team_member_id):
    return root.team.retrieve(team_member_id)

  def resolve_locations(root, ctx):
    return root.locations.list()

  def resolve_location(root, ctx, location_id):
    return root.locations.retrieve(location_id)

  def resolve_availability(root, ctx, filter={}):
    return root.bookings.search_availability(**filter)

  @account_loaded
  def resolve_bookings(root, ctx, filter={}, pagination={}):
    current_account.assert_permission('square.read_bookings')
    return root.bookings.list(**filter, **pagination)

  @account_loaded
  def resolve_booking(root, ctx, booking_id):
    return root.bookings.retrieve(booking_id)

  def resolve_catalog_objects(root, ctx, filter={}, pagination={}):
    return root.catalog.objects_search(**filter, **pagination)
  
  def resolve_catalog_object(root, ctx, **kwargs):
    return root.catalog.retrieve(**kwargs)
  
  def resolve_catalog_items(root, ctx, filter={}, pagination={}):
    return root.catalog.items_search(**filter, **pagination)
  
  def resolve_catalog_info(root, ctx):
    return root.catalog.catalog_info()

  @account_loaded
  def resolve_payments(root, ctx, filter={}, pagination={}):
    current_account.assert_permission('square.read_payments')
    return root.payments.list(
      **filter,
      **pagination
    )

  def resolve_payment(root, ctx, payment_id):
    return root.payments.retrieve(payment_id)

class SquareOneMutations(ObjectType):
  # Customers
  square_create_customer = SquareCreateCustomer.Field()
  square_update_customer = SquareUpdateCustomer.Field()
  square_delete_customer = SquareDeleteCustomer.Field()
  square_remove_group_from_customer = SquareRemoveGroupFromCustomer.Field()
  square_add_group_to_customer = SquareAddGroupToCustomer.Field()
  # CustomerGroups
  square_create_customer_group = SquareCreateCustomerGroup.Field()
  square_update_customer_group = SquareUpdateCustomerGroup.Field()
  square_delete_customer_group = SquareDeleteCustomerGroup.Field()
  # Locations
  square_create_location = SquareCreateLocation.Field()
  square_update_location = SquareUpdateLocation.Field()
  # Team
  square_create_team_member = SquareCreateTeamMember.Field()
  square_update_team_member = SquareUpdateTeamMember.Field()
  square_update_wage_setting = SquareUpdateWageSetting.Field()
  # Cards
  square_create_card = SquareCreateCard.Field()
  square_disable_card = SquareDisableCard.Field()
  # Bookings
  square_create_booking = SquareCreateBooking.Field()
  square_update_booking = SquareUpdateBooking.Field()
  square_cancel_booking = SquareCancelBooking.Field()
  # Catalog
  square_catalog_batch_upsert = SquareCatalogBatchUpsert.Field()
  square_catalog_batch_delete = SquareCatalogBatchDelete.Field()
  square_catalog_update_item_modifier_lists = SquareCatalogUpdateItemModifierLists.Field()
  square_catalog_update_item_taxes = SquareCatalogUpdateItemTaxes.Field()
  # Payments
  square_create_payment = SquareCreatePayment.Field()
  square_update_payment = SquareUpdatePayment.Field()
  square_cancel_payment = SquareCancelPayment.Field()
  square_complete_payment = SquareCompletePayment.Field()

class SquareQueries(ObjectType):
  square = Field(SquareQueries)

  def resolve_square(root, ctx):
    return test_client

Graph.add(
  query=SquareQueries,
  mutation=SquareOneMutations,
  types=list(OBJECT_TYPES.values())
)