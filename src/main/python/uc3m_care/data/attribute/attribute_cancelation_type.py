"""Classs for the attribute Cancelation Type"""
from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.exception.error_msg import ErrorMsg


#pylint: disable=too-few-public-methods
class CancelationType(Attribute):
    """Classs for the attribute PhoneNumber"""
    _validation_pattern = r"(Final|Temporal)"
    _validation_error_message = ErrorMsg.NOT_VALID_CANCELLATION_TYPE.value
