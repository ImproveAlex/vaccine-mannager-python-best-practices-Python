"""Subclass of JsonStore for managing the Appointments"""
# pylint: disable=import-error,too-few-public-methods
from uc3m_care.storage.json_storage import JsonStore
from uc3m_care.singleton.singleton_metaclass import SingletonMetaclass
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.exception.error_msg import ErrorMsg
from uc3m_care.data.key_lables import KeyLabel


class AppointmentsJsonStore(JsonStore, metaclass=SingletonMetaclass):
    """Subclass of JsonStore for managing the Appointments"""
    _FILE_PATH = JSON_FILES_PATH + "store_date.json"
    _ID_FIELD = KeyLabel.VA_DATE_SIGNATURE.value
    ERROR_INVALID_APPOINTMENT_OBJECT = ErrorMsg.NOT_VALID_APPOINTMENT_OBJ.value

    def add_item(self, item):
        """Overrides the add_item method to verify the item to be stored"""
        # pylint: disable=import-outside-toplevel, cyclic-import
        from uc3m_care.data.vaccination_appointment import VaccinationAppointment
        if not isinstance(item, VaccinationAppointment):
            raise VaccineManagementException(self.ERROR_INVALID_APPOINTMENT_OBJECT)
        super().add_item(item)
