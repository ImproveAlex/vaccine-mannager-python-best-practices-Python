"""Class representing an entry of the vaccine administration log"""
from datetime import datetime
from uc3m_care.storage.vaccination_json_storage import VaccinationJsonStore
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.data.key_lables import KeyLabel
from uc3m_care.exception.error_msg import ErrorMsg

#pylint: disable=too-few-public-methods
class VaccinationLog():
    """Class representing an entry of the Vaccine administration log"""

    def __init__(self, date_signature):
        self.__date_signature = date_signature
        self.__timestamp = datetime.timestamp(datetime.utcnow())

    def save_log_entry( self ):
        """saves the entry in the vaccine administration log"""
        vaccination_log = VaccinationJsonStore()
        vaccination_log.add_item(self)

    @property
    def date_signature( self ):
        """returns the value of the date_signature"""
        return self.__date_signature

    @property
    def vaccination_date( self ):
        """returns the timestamp corresponding to the date of administration """
        return self.__timestamp

    @classmethod
    def check_vaccine_in_log(cls, date_signature):
        """Checks if the date signatur is already in log"""
        vacc_storage = VaccinationJsonStore()
        vacc_storage.load()
        if vacc_storage.find_item(date_signature, KeyLabel.LOG_DATE_SIGNATURE.value) is not None:
            raise VaccineManagementException(ErrorMsg.ALREADY_VACCINATED.value)
