"""Subclass of JsonStore for managing the VaccinationLog"""
# pylint: disable=import-error,too-few-public-methods
from uc3m_care.storage.json_storage import JsonStore
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.singleton.singleton_metaclass import SingletonMetaclass
from uc3m_care.exception.error_msg import ErrorMsg
from uc3m_care.data.key_lables import KeyLabel


class VaccinationJsonStore(JsonStore, metaclass=SingletonMetaclass):
    """Subclass of JsonStore for managing the VaccinationLog"""
    _FILE_PATH = JSON_FILES_PATH + "store_vaccine.json"
    _ID_FIELD = KeyLabel.LOG_DATE_SIGNATURE.value

    def add_item( self, item ):
        """Overrides the add_item to verify the item to be stored"""
        # pylint: disable=import-outside-toplevel, cyclic-import
        from uc3m_care.data.vaccination_log import VaccinationLog
        if not isinstance(item, VaccinationLog):
            raise VaccineManagementException(ErrorMsg.NOT_VALID_LOG_OBJ.value)
        super().add_item(item)
