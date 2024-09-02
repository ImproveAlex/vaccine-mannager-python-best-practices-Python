"""Subclass of JsonParer for parsing inputs of get_vaccine_date"""
# pylint: disable=import-error,too-few-public-methods
from uc3m_care.parser.json_parser import JsonParser
from uc3m_care.exception.error_msg import ErrorMsg
from uc3m_care.data.key_lables import KeyLabel

class AppointmentJsonParser(JsonParser):
    """Subclass of JsonPasrer for parsing inputs of get_vaccine_date"""
    BAD_PHONE_NUMBER_LABEL_ERROR = ErrorMsg.WRONG_LABEL_PHONE.value
    BAD_PATIENT_SYS_ID_LABEL_ERROR = ErrorMsg.WRONG_LABEL_PATIENT_ID.value
    PATIENT_SYSTEM_ID_KEY = KeyLabel.PATIENT_SYSTEM_ID.value
    CONTACT_PHONE_NUMBER_KEY = KeyLabel.PHONE.value

    _JSON_KEYS = [ PATIENT_SYSTEM_ID_KEY, CONTACT_PHONE_NUMBER_KEY ]
    _ERROR_MESSAGES = [ BAD_PATIENT_SYS_ID_LABEL_ERROR, BAD_PHONE_NUMBER_LABEL_ERROR ]
