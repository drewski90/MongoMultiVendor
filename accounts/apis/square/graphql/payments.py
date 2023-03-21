from graphene import (
  ObjectType, 
  InputObjectType,
  String,
  Int,
  Boolean,
  List,
  Mutation,
  Field,
  ID,
  Argument
)
from .cards import (
  SquareCardType,
  SquareCardInput
)
from .money import (
  SquareMoneyType, 
  SquareMoneyInput
)
from .address import (
  SquareAddressInput,
  SquareAddressType
)
from .enums import ENUMS
from ..client.merchant import square_merchant

class SquareErrorType(ObjectType):

  category=String()
  code=String()
  detail=String()
  field=String()

class SquareDeviceDetailsType(ObjectType):

  device_id=ID()
  device_installation_id=String()
  device_name=String()

class SquarePaymentType(ObjectType):

  class SquareProcessingFeeType(ObjectType):
    effective_at=String()
    type=String()
    amount_money=Field(SquareMoneyType)

  class SquareCardDetailsType(ObjectType):

    class SquareCardPaymentTimelineType(ObjectType):

      authorized_at=String()
      captured_at=String()
      voided_at=String()

    status=String()
    card=Field(SquareCardType)
    entry_method=String()
    cvv_status=String()
    avs_status=String()
    auth_result_code=String()
    application_identifier=String()
    application_name=String()
    application_cryptogram=String()
    verification_method=String()
    verification_results=String()
    statement_description=String()
    device_details=Field(SquareDeviceDetailsType)
    card_payment_timeline=Field(SquareCardPaymentTimelineType)
    refund_requires_timeline=Boolean()
    errors=List(SquareErrorType)

  class SquareCashPaymentDetailsType(ObjectType):

    buyer_supplied_money=Field(SquareMoneyType)
    change_back_money=Field(SquareMoneyType)

  class SquareBankAccountDetailsType(ObjectType):

    class SquareACHDetailsType(ObjectType):

      routing_number=String()
      account_suffix=String()
      account_type=String()
      errors=List(SquareErrorType)

    bank_name=String()
    transfer_type=String()
    account_ownership_type=String()
    fingerprint=String()
    country=String
    statement_description=String()
    ach_details=Field(SquareACHDetailsType)

  class SquareExternalPaymentDetailsType(ObjectType):

    type=String()
    source=String()
    source_id=ID()
    source_fee_money=Field(SquareMoneyType)

  class SquareDigitalWalletDetailsType(ObjectType):

    class SquareCashAppDetailsType(ObjectType):
      buyer_full_name=String()
      buyer_country_code=String()
      buyer_cashtag=String()

    status=String()
    brand=String()
    cash_app_details=Field(SquareCashAppDetailsType)

  class SquareBuyNowPayLaterDetailsType(ObjectType):

    class SquareAfterpayDetailsType(ObjectType):

      email_address=String()
    
    class SquareClearpayDetailsType(ObjectType):

      email_address=String()
    
    brand=String()
    afterpay_details=Field(SquareAfterpayDetailsType)
    clearpay_details=Field(SquareClearpayDetailsType)

  class SquareRiskEvaluationType(ObjectType):

    created_at=String()
    risk_level=String()

  class SquareApplicationDetailsType(ObjectType):

    square_product=String()
    application_id=ID()

  id=ID()
  created_at=String()
  updated_at=String()
  amount_money=Field(SquareMoneyType)
  tip_money=Field(SquareMoneyType)
  total_money=Field(SquareMoneyType)
  app_fee_money=Field(SquareMoneyType)
  approved_money=Field(SquareMoneyType)
  processing_fee=List(SquareProcessingFeeType)
  refunded_money=Field(SquareMoneyType)
  status=String()
  delay_duration=String()
  delay_action=String()
  delayed_until=String()
  source_type=String()
  card_details=Field(SquareCardDetailsType)
  cash_details=Field(SquareCashPaymentDetailsType)
  bank_account_details=Field(SquareBankAccountDetailsType)
  external_details=Field(SquareExternalPaymentDetailsType)
  wallet_details=Field(SquareDigitalWalletDetailsType)
  buy_now_pay_later_details=Field(SquareBuyNowPayLaterDetailsType)
  location_id=ID()
  order_id=ID()
  reference_id=ID()
  customer_id=ID()
  team_member_id=ID()
  refund_ids=List(ID)
  risk_evaluation=Field(SquareRiskEvaluationType)
  buyer_email_address=String()
  billing_address=Field(SquareAddressType)
  shipping_address=Field(SquareAddressType)
  note=String()
  statement_description_identifier=String()
  capabilities=List(String)
  receipt_number=String()
  receipt_url=String()
  device_details=Field(SquareDeviceDetailsType)
  application_details=Field(SquareApplicationDetailsType)
  version_token=String()

class SquarePaymentResultsType(ObjectType):

  payments = List(SquarePaymentType)
  cursor = String()

class SquarePaymentInput(InputObjectType):

  class SquareProcessingFeeInput(InputObjectType):
    effective_at=String()
    type=Argument(ENUMS.SquareProcessingFeeTypeEnum)
    amount_money=SquareMoneyInput()

  class SquareCardDetailsInput(InputObjectType):

    class SquareDeviceDetailsInput(InputObjectType):

      device_id=ID()
      device_installation_id=ID()
      device_name=String()

    class SquareCardPaymentTimelineInput(InputObjectType):

      authorized_at=String()
      captured_at=String()
      voided_at=String()

    status=Argument(ENUMS.SquarePaymentCardStatusEnum)
    card=SquareCardInput()
    entry_method=Argument(ENUMS.SquareCardEntryMethodEnum)
    cvv_status=Argument(ENUMS.SquareCardCVVStatusEnum)
    avs_status=Argument(ENUMS.SquareCardAVSStatusEnum)
    auth_result_code=String()
    application_identifier=String()
    application_name=String()
    application_cryptogram=String()
    verification_method=Argument(ENUMS.SquareCardVerificationMethodEnum)
    verification_results=Argument(ENUMS.SquareEVMPaymentResultEnum)
    statement_description=String()
    device_details=SquareDeviceDetails=None
    card_payment_timeline=SquareCardPaymentTimelineInput()
    refund_requires_timeline=Boolean()

  class SquareCashPaymentDetailsInput(InputObjectType):

    buyer_supplied_money=SquareMoneyInput()
    change_back_money=SquareMoneyInput()

  class SquareBankAccountDetailsInput(InputObjectType):

    class SquareACHDetailsInput(InputObjectType):

      routing_number=String()
      account_suffix=String()
      account_type=Argument(
        ENUMS.SquareBankAccountTypeEnum
      )

    bank_name=String()
    transfer_type=String()
    account_ownership_type=Argument(
      ENUMS.SquareBankAccountOwnershipTypeEnum
    )
    fingerprint=String()
    country=String()
    statement_description=String()
    ach_details=Argument(
      ENUMS.SquareBankAccountTypeEnum
    )

  class SquareExternalPaymentDetailsInput(InputObjectType):

    type=Argument(ENUMS.SquareExternalPaymentTypeEnum)
    source=String()
    source_id=String()
    source_fee_money=SquareMoneyInput()

  class SquareDigitalWalletDetailsInput(InputObjectType):

    class SquareCashAppDetailsInput(InputObjectType):
      buyer_full_name=String()
      buyer_country_code=String()
      buyer_cashtag=String()

    status=Argument(ENUMS.SquareDigitalWalletStatusEnum)
    brand=Argument(ENUMS.SquareDigitalWalletBrandEnum)
    cash_app_details=SquareCashAppDetailsInput()

  class SquareBuyNowPayLaterDetailsInput(InputObjectType):

    class SquareAfterpayDetailsInput(InputObjectType):

      email_address=String()
  
    class SquareClearpayDetailsInput(InputObjectType):

      email_address=String()
    
    brand=Argument(ENUMS.SquareCardCoBrandEnum)
    afterpay_details=SquareAfterpayDetailsInput()
    clearpay_details=SquareClearpayDetailsInput()

  class SquareRiskEvaluationInput(InputObjectType):

    created_at=String()
    risk_level=Argument(
      ENUMS.SquareRiskEvaluationRiskLevelEnum
    )

  class SquareDeviceDetailsInput(InputObjectType):

    device_id=ID()
    device_installation_id=ID()
    device_name=String()

  class SquareApplicationDetailsInput(InputObjectType):

    square_product=Argument(
      ENUMS.SquareApplicationDetailsExternalSquareProductEnum
    )
    application_id=String()

  id=ID()
  created_at=String()
  updated_at=String()
  amount_money=SquareMoneyInput()
  tip_money=SquareMoneyInput()
  total_money=SquareMoneyInput()
  app_fee_money=SquareMoneyInput()
  approved_money=SquareMoneyInput()
  processing_fee=List(SquareProcessingFeeInput)
  refunded_money=SquareMoneyInput()
  status=Argument(ENUMS.SquarePaymentStatusEnum)
  delay_duration=String()
  delay_action=Argument(ENUMS.SquarePaymentDelayActionEnum)
  delayed_until=String()
  source_type=Argument(ENUMS.SquarePaymentSourceTypeEnum)
  card_details=SquareCardDetailsInput
  cash_details=SquareCashPaymentDetailsInput
  bank_account_details=SquareBankAccountDetailsInput()
  external_details=SquareExternalPaymentDetailsInput()
  wallet_details=SquareDigitalWalletDetailsInput()
  buy_now_pay_later_details=SquareBuyNowPayLaterDetailsInput()
  location_id=ID()
  order_id=ID()
  reference_id=ID()
  customer_id=ID()
  team_member_id=ID()
  refund_ids=List(ID)
  risk_evaluation=SquareRiskEvaluationInput()
  buyer_email_address=String()
  billing_address=SquareAddressInput()
  shipping_address=SquareAddressInput()
  note=String()
  statement_description_identifier=String()
  capabilities=List(ENUMS.SquarePaymentCapabilitiesEnum)
  receipt_number=String()
  receipt_url=String()
  device_details=SquareDeviceDetailsInput()
  application_details=SquareApplicationDetailsInput()
  version_token=String()

class SquarePaymentsFilterInput(InputObjectType):
  begin_time=String()
  end_time=String()
  sort_order=Argument(
    ENUMS.SquareSortOrderEnum
  )
  cursor=String()
  location_id=ID()
  total=Int()
  last_4=String()
  card_brand=Argument(
    ENUMS.SquareCardBrandEnum
  )
  limit=Int()

class SquarePaymentsPaginationInput(InputObjectType):
  cursor=String()
  limit=Int()

class SquareCreatePayment(Mutation):

  payment = Field(SquarePaymentType)

  class Arguments:

    idempotency_key = String(required=True)
    payment = SquarePaymentInput(required=True)

  @classmethod
  def mutate(cls, root, ctx, idempotency_key, payment):
    resp = square_merchant.payments.create(
      idempotency_key=idempotency_key,
      **payment
    )
    return cls(**resp)

class SquareUpdatePayment(Mutation):

  payment = Field(SquarePaymentType)

  class Arguments:

    idempotency_key = String(required=True)
    payment = SquarePaymentInput(required=True)

  @classmethod
  def mutate(cls, root, ctx, idempotency_key, **payment):
    resp = square_merchant.payments.create(
      idempotency_key=idempotency_key,
      **payment
    )
    return cls(**resp)

class SquareCancelPayment(Mutation):

  payment = Field(SquarePaymentType)

  class Arguments:
    payment_id = ID(required=True)

  @classmethod
  def mutate(cls, root, ctx, payment_id):
    resp = square_merchant.payments.cancel(
      payment_id
    )
    return cls(**resp)

class SquareCompletePayment(Mutation):

  payment = Field(SquarePaymentType)

  class Arguments:

    payment_id = ID(required=True)
    version_token = String()
  
  @classmethod
  def mutate(cls, root, ctx, **kwargs):
    resp = square_merchant.payments.complete(
      **kwargs
    )
    return cls(**resp)