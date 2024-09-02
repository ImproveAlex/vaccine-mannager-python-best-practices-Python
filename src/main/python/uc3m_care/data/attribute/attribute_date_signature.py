"""Classs for the attribute DateSignature"""
from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.exception.error_msg import ErrorMsg

#pylint: disable=too-few-public-methods
class DateSignature(Attribute):
    """Classs for the attribute DateSignature"""
    _validation_pattern = r"[0-9a-fA-F]{64}$"
    _validation_error_message = ErrorMsg.NOT_VALID_DATE_SIGNATURE.value
