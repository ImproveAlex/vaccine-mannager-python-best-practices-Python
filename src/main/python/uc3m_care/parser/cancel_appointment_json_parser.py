"""Subclase de JsonParser para parsear los inputs en el metodo cancel_appointment"""
# pylint: disable=import-error,too-few-public-methods
from uc3m_care.parser.json_parser import JsonParser
from uc3m_care.exception.error_msg import ErrorMsg
from uc3m_care.data.key_lables import KeyLabel


class CancelAppointmentJsonParser(JsonParser):
    """Clase parser para cancel_appointment"""
    BAD_LABEL_DATE_SIGNATURE_ERROR = ErrorMsg.WRONG_LABLE_DATE_SIGNATURE.value
    BAD_LABEL_CANCELATION_TYPE_ERROR = ErrorMsg.WRONG_LABLE_CANCELATION_TYPE.value
    BAD_LABEL_REASON_ERROR = ErrorMsg.WRONG_LABLE_REASON.value
    DATE_SIGNATURE_KEY = KeyLabel.DATE_SIGNATURE.value
    CANCELATION_TYPE_KEY = KeyLabel.CANCELATION_TYPE.value
    REASON_KEY = KeyLabel.REASON.value

    _JSON_KEYS = [DATE_SIGNATURE_KEY, CANCELATION_TYPE_KEY, REASON_KEY]
    _ERROR_MESSAGES = [BAD_LABEL_DATE_SIGNATURE_ERROR,
                       BAD_LABEL_CANCELATION_TYPE_ERROR,
                       BAD_LABEL_REASON_ERROR]
