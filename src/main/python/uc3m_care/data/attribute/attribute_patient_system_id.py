"""Classs for the attribute PatientSystemId"""
from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.exception.error_msg import ErrorMsg

#pylint: disable=too-few-public-methods
class PatientSystemId(Attribute):
    """Classs for the attribute PatientSystemId"""
    _validation_pattern = r"[0-9a-fA-F]{32}$"
    _validation_error_message = ErrorMsg.NOT_VALID_PATIENT_SYSTEM_ID.value
