"""Classs for the attribute Cancelation Reason"""
from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.exception.error_msg import ErrorMsg


#pylint: disable=too-few-public-methods
class CancelationReason(Attribute):
    """Classs for the attribute PhoneNumber"""
    _validation_pattern = r"^[A-Za-z0-9_-]{2,100}$"
    _validation_error_message = ErrorMsg.NOT_VALID_CANCELATION_REASON.value
