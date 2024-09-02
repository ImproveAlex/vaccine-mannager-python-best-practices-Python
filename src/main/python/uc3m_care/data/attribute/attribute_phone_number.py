"""Classs for the attribute PhoneNumber"""
from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.exception.error_msg import ErrorMsg

#pylint: disable=too-few-public-methods
class PhoneNumber(Attribute):
    """Classs for the attribute PhoneNumber"""
    _validation_pattern = r"^(\+)[0-9]{11}"
    _validation_error_message = ErrorMsg.NOT_VALID_PHONE_NUMBER.value
