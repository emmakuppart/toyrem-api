from enum import Enum

class SystemParameterKey(Enum):
    session_expiration_date_in_seconds = 'SESSION_EXPIRATION_DATE_IN_SECONDS'

class PaymentType(Enum):
    banklink = 'BANKLINK'
    card = 'CARD'
    cash = 'CASH'
    other = 'OTHER'

class Language(Enum):
    et = 'et'
    en = 'en'
    ru = 'ru'

class ShippingType(Enum):
    toyrem = 'TOYREM_OFFICE'
    itellaSmartpost = 'ITELLA_SMARTPOST'