from pydantic import constr, conint, conlist
from .error import request_wrapper
from .utils import APIModel, APIWrapper, Model
from typing import List
from .money import Money
from .cards import Card
from .address import Address
from .patterns import (
  EMAIL_PATTERN,
  RFC_3339_PATTERN,
)
from .enums import (
  SquareProcessingFeeTypeEnum,
  SquarePaymentStatusEnum,
  SquarePaymentDelayActionEnum,
  SquarePaymentSourceTypeEnum,
  SquarePaymentCardStatusEnum,
  SquareCardEntryMethodEnum,
  SquareCardCVVStatusEnum,
  SquareCardAVSStatusEnum,
  SquareCardVerificationMethodEnum,
  SquareEVMPaymentResultEnum,
  SquareBankAccountOwnershipTypeEnum,
  SquareBankAccountTypeEnum,
  SquareExternalPaymentTypeEnum,
  SquareDigitalWalletStatusEnum,
  SquareDigitalWalletBrandEnum,
  SquareCardCoBrandEnum,
  SquareRiskEvaluationRiskLevelEnum,
  SquarePaymentCapabilitiesEnum,
  SquareApplicationDetailsExternalSquareProductEnum,
  SquareSortOrderEnum,
  SquareCardBrandEnum
)

class Error(Model):

  category:str=None
  code:str=None
  detail:str=None
  field:str=None

class Payment(APIModel):

  class ProcessingFee(Model):
    effective_at:constr(
      strip_whitespace=True,
      regex=RFC_3339_PATTERN
    )=None
    type:SquareProcessingFeeTypeEnum=None
    amount_money:Money=None

  class CardDetails(Model):

    class DeviceDetails(Model):

      device_id:constr(max_length=255)
      device_installation_id:constr(max_length=255)
      device_name:constr(max_length=255)

    class CardPaymentTimeline(Model):

      authorized_at:constr(
        strip_whitespace=True,
        regex=RFC_3339_PATTERN
      )=None
      captured_at:constr(
        strip_whitespace=True,
        regex=RFC_3339_PATTERN
      )=None
      voided_at:constr(
        strip_whitespace=True,
        regex=RFC_3339_PATTERN
      )=None

    status:SquarePaymentCardStatusEnum=None
    card:Card=None
    entry_method:SquareCardEntryMethodEnum=None
    cvv_status:SquareCardCVVStatusEnum=None
    avs_status:SquareCardAVSStatusEnum=None
    auth_result_code:constr(max_length=10)=None
    application_identifier:constr(max_length=32)=None
    application_name:constr(max_length=16)=None
    application_cryptogram:constr(max_length=16)=None
    verification_method:SquareCardVerificationMethodEnum=None
    verification_results:SquareEVMPaymentResultEnum=None
    statement_description:constr(max_length=50)=None
    device_details:DeviceDetails=None
    card_payment_timeline:CardPaymentTimeline=None
    refund_requires_timeline:bool=None
    errors:List[Error]=None

  class CashPaymentDetails(Model):

    buyer_supplied_money:Money=None
    change_back_money:Money=None

  class BankAccountDetails(Model):

    class ACHDetails(Model):

      routing_number:constr(
        strip_whitespace=True,
        max_length=50
      )=None
      account_suffix:constr(
        strip_whitespace=True,
        max_length=4,
        min_length=1
      )=None
      account_type:SquareBankAccountTypeEnum=None
      errors:List[Error]=None

    bank_name:constr(max_length=100)=None
    transfer_type:constr(max_length=50)=None
    account_ownership_type:SquareBankAccountOwnershipTypeEnum=None
    fingerprint:constr(max_length=255)=None
    country:constr(max_length=2, min_length=2)=None
    statement_description:constr(max_length=1000)
    ach_details:ACHDetails=None

  class ExternalPaymentDetails(Model):

    type:SquareExternalPaymentTypeEnum
    source:constr(max_length=255)
    source_id:constr(max_length=255)=None
    source_fee_money:Money=None

  class DigitalWalletDetails(Model):

    class CashAppDetails(Model):
      buyer_full_name:constr(max_length=255)=None
      buyer_country_code:constr(max_length=2, min_length=2)=None
      buyer_cashtag:constr(min_length=1, max_length=21)

    status:SquareDigitalWalletStatusEnum=None
    brand:SquareDigitalWalletBrandEnum=None
    cash_app_details:CashAppDetails=None

  class BuyNowPayLaterDetails(Model):

    class AfterpayDetails(Model):

      email_address:constr(
        strip_whitespace=True,
        regex=EMAIL_PATTERN
      )=None
    
    class ClearpayDetails(Model):

      email_address:constr(
        strip_whitespace=True,
        regex=EMAIL_PATTERN
      )=None
    
    brand:SquareCardCoBrandEnum=None
    afterpay_details:AfterpayDetails=None
    clearpay_details:ClearpayDetails=None

  class RiskEvaluation(Model):

    created_at:constr(
        strip_whitespace=True,
        regex=RFC_3339_PATTERN
      )=None
    risk_level:SquareRiskEvaluationRiskLevelEnum=None

  class DeviceDetails(Model):

    device_id:str=None
    device_installation_id:str=None
    device_name:str=None

  class ApplicationDetails(Model):

    square_product:SquareApplicationDetailsExternalSquareProductEnum=None
    application_id:str=None

  id:constr(
    strip_whitespace=True,
    min_length=1,
    max_length=192
  )=None
  created_at:constr(
    strip_whitespace=True,
    min_length=1,
    max_length=32,
    regex=RFC_3339_PATTERN
  )=None
  updated_at:constr(
    strip_whitespace=True,
    min_length=1,
    max_length=32,
    regex=RFC_3339_PATTERN
  )=None
  amount_money:Money=None
  tip_money:Money=None
  total_money:Money=None
  app_fee_money:Money=None
  approved_money:Money=None
  processing_fee:List[ProcessingFee]=None
  refunded_money:Money=None
  status:SquarePaymentStatusEnum=None
  delay_duration:str=None
  delay_action:SquarePaymentDelayActionEnum=None
  delayed_until:str=None
  source_type:SquarePaymentSourceTypeEnum=None
  card_details:CardDetails=None
  cash_details:CashPaymentDetails=None
  bank_account_details:BankAccountDetails=None
  external_details:ExternalPaymentDetails=None
  wallet_details:DigitalWalletDetails=None
  buy_now_pay_later_details:BuyNowPayLaterDetails=None
  location_id:constr(
    strip_whitespace=True,
    max_length=50
  )=None
  order_id:constr(
    strip_whitespace=True,
    max_length=192
  )=None
  reference_id:constr(
    strip_whitespace=True,
    max_length=40
  )=None
  customer_id:constr(
    strip_whitespace=True,
    max_length=191
  )=None
  team_member_id:constr(
    strip_whitespace=True,
    max_length=192
  )=None
  refund_ids:List[str]=None
  risk_evaluation:RiskEvaluation=None
  buyer_email_address:constr(
    strip_whitespace=True,
    max_length=255
  )=None
  billing_address:Address=None
  shipping_address:Address=None
  note:constr(
    strip_whitespace=True,
    max_length=500
  )
  statement_description_identifier:str=None
  capabilities:List[SquarePaymentCapabilitiesEnum]=None
  receipt_number:constr(max_length=4)=None
  receipt_url:constr(max_length=255)=None
  device_details:DeviceDetails=None
  application_details:ApplicationDetails=None
  version_token:str=None

class Payments(APIWrapper):

  api_name = "payments"

  class CreatePaymentInput(Model):

    source_id:constr(
      strip_whitespace=True,
      min_length=1
    )
    idempotency_key:constr(
      strip_whitespace=True,
      min_length=1, 
      max_length=45
    )
    amount_money:Money
    tip_money:Money=None
    app_fee_money:Money=None
    delay_duration:constr()=None
    delay_action:SquarePaymentDelayActionEnum=None
    autocomplete:bool=True,
    order_id:str=None
    customer_id:str=None
    location_id:str=None
    team_member_id:str=None
    reference_id:constr(max_length=40)=None
    verification_token:str=None
    accept_partial_authorization:bool=False
    buyer_email_address:str=None
    billing_address:Address=None
    shipping_address:Address=None
    note:constr(
      strip_whitespace=True,
      max_length=500
    )=None
    statement_description_identifier:constr(
      strip_whitespace=True,
      max_length=20
    )
    cash_details:Payment.CashPaymentDetails=None
    external_details:Payment.ExternalPaymentDetails=None

  def create(
    self,
    idempotency_key:str,
    source_id:str=None,
    amount_money:Money=None,
    tip_money:Money=None,
    app_fee_money:Money=None,
    delay_duration:str=None,
    delay_action:SquarePaymentDelayActionEnum=None,
    autocomplete:bool=True,
    order_id:str=None,
    customer_id:str=None,
    location_id:str=None,
    team_member_id:str=None,
    reference_id:str=None,
    verification_token:str=None,
    accept_partial_authorization:bool=None,
    buyer_email_address:str=None,
    billing_address:Address=None,
    shipping_address:Address=None,
    note:str=None,
    statement_description_identifier:str=None,
    cash_details:Payment.CashPaymentDetails=None,
    external_details:Payment.ExternalPaymentDetails=None
  ):
    body = request_wrapper(
      self.api.create_payment,
      body=dict(
        source_id=source_id,
        idempotency_key=idempotency_key,
        amount_money=amount_money,
        tip_money=tip_money,
        app_fee_money=app_fee_money,
        delay_duration=delay_duration,
        delay_action=delay_action,
        autocomplete=autocomplete,
        order_id=order_id,
        customer_id=customer_id,
        location_id=location_id,
        team_member_id=team_member_id,
        reference_id=reference_id,
        verification_token=verification_token,
        accept_partial_authorization=accept_partial_authorization,
        buyer_email_address=buyer_email_address,
        billing_address=billing_address,
        shipping_address=shipping_address,
        note=note,
        statement_description_identifier=statement_description_identifier,
        cash_details=cash_details,
        external_details=external_details
      )
    )
    if 'payment' in body:
      return Payment(
        api_wrapper=self,
        **body['payment']
      )

  def update(
    self,
    idempotency_key:str,
    id:str,
    amount_money:str=None,
    tip_money:Money=None,
    total_money:Money=None,
    app_fee_money:Money=None,
    approved_money:Money=None,
    processing_fee:List[Payment.ProcessingFee]=None,
    refunded_money:Money=None,
    status:SquarePaymentStatusEnum=None,
    delay_duration:str=None,
    delay_action:SquarePaymentDelayActionEnum=None,
    delayed_until:str=None,
    source_type:SquarePaymentSourceTypeEnum=None,
    card_details:Payment.CardDetails=None,
    cash_details:Payment.CashPaymentDetails=None,
    bank_account_details:Payment.BankAccountDetails=None,
    external_details:Payment.ExternalPaymentDetails=None,
    wallet_details:Payment.DigitalWalletDetails=None,
    buy_now_pay_later_details:Payment.BuyNowPayLaterDetails=None,
    location_id:str=None,
    order_id:str=None,
    reference_id:str=None,
    customer_id:str=None,
    team_member_id:str=None,
    refund_ids:List[str]=None,
    risk_evaluation:Payment.RiskEvaluation=None,
    buyer_email_address:str=None,
    billing_address:Address=None,
    shipping_address:Address=None,
    note:str=None,
    statement_description_identifier:str=None,
    capabilities:List[SquarePaymentCapabilitiesEnum]=None,
    receipt_number:str=None,
    receipt_url:str=None,
    device_details:Payment.DeviceDetails=None,
    application_details:Payment.ApplicationDetails=None,
    version_token:str=None
  ):
    payment = Payment(
      api_wrapper=self,
      id=id,
      amount_money=amount_money,
      tip_money=tip_money,
      total_money=total_money,
      app_fee_money=app_fee_money,
      approved_money=approved_money,
      processing_fee=processing_fee,
      refunded_money=refunded_money,
      status=status,
      delay_duration=delay_duration,
      delay_action=delay_action,
      delayed_until=delayed_until,
      source_type=source_type,
      card_details=card_details,
      cash_details=cash_details,
      bank_account_details=bank_account_details,
      external_details=external_details,
      wallet_details=wallet_details,
      buy_now_pay_later_details=buy_now_pay_later_details,
      location_id=location_id,
      order_id=order_id,
      reference_id=reference_id,
      customer_id=customer_id,
      team_member_id=team_member_id,
      refund_ids=refund_ids,
      risk_evaluation=risk_evaluation,
      buyer_email_address=buyer_email_address,
      billing_address=billing_address,
      shipping_address=shipping_address,
      note=note,
      statement_description_identifier=statement_description_identifier,
      capabilities=capabilities,
      receipt_number=receipt_number,
      receipt_url=receipt_url,
      device_details=device_details,
      application_details=application_details,
      version_token=version_token
    ).dict(
      exclude_none=True,
      exclude_unset=True
    )
    body = request_wrapper(
      self.api.update_payment,
      payment_id=id,
      body=dict(
        payment=payment,
        idempotency_key=idempotency_key
      )
    )
    if 'payment' in body:
      return Payment(
        api_wrapper=self,
        **body['payment']
      )

  class ListPaymentsInput(Model):
    begin_time:constr(
      strip_whitespace=True,
      regex=RFC_3339_PATTERN,
    )=None
    end_time:constr(
      strip_whitespace=True,
      regex=RFC_3339_PATTERN,
    )=None
    sort_order:SquareSortOrderEnum=None
    cursor:str=None
    location_id:str=None
    total:int=None
    last_4:constr(
      max_length=4,
      min_length=4
    )=None
    card_brand:SquareCardBrandEnum=None
    limit:conint(
      lt=101,
      gt=0
    )=None

  def list(
    self,
    begin_time=None,
    end_time=None,
    sort_order=None,
    cursor=None,
    location_id=None,
    total=None,
    last_4=None,
    card_brand=None,
    limit=None
  ):
    input = self.ListPaymentsInput(
      begin_time=begin_time,
      end_time=end_time,
      sort_order=sort_order,
      cursor=cursor,
      location_id=location_id,
      total=total,
      last_4=last_4,
      card_brand=card_brand,
      limit=limit
    ).dict(
      exclude_none=True,
      exclude_unset=True
    )
    body = request_wrapper(
      self.api.list_payments,
      **input
    )
    if 'payments' in body:
      body['payments'] = Payment(
        api_wrapper=self,
        **body['payments']
      )
    else:
      body['payments'] = []
    return body

  def retrieve(self, payment_id:str):
    body = request_wrapper(
      self.api.get_payment,
      payment_id=payment_id
    )
    if 'payment' in body:
      body['payment'] = Payment(
        api_wrapper=self,
        **body['payment']
      )
    return body

  def cancel(self, payment_id:str):
    body = request_wrapper(
      self.api.cancel_payment,
      payment_id=payment_id
    )
    if 'payment' in body:
      body['payment'] = Payment(
        api_wrapper=self,
        **body['payment']
      )
    return body

  def complete(
    self,
    payment_id:str,
    version_token:str
  ):
    body = request_wrapper(
      self.api.complete_payment,
      payment_id=payment_id,
      body=dict(version_token=version_token)
    )
    if 'payment' in body:
      body['payment'] = Payment(
        api_wrapper=self,
        **body['payment']
      )
    return body