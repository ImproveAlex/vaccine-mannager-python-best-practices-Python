"""Subclass of JsonStore for managing the Patients store"""
# pylint: disable=import-error,too-few-public-methods
from uc3m_care.storage.json_storage import JsonStore
from uc3m_care.singleton.singleton_metaclass import SingletonMetaclass
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.data.key_lables import KeyLabel
from uc3m_care.exception.error_msg import ErrorMsg


class PatientsJsonStore(JsonStore, metaclass=SingletonMetaclass):
    """Subclass of JsonStore for managing the VaccinationLog"""
    _FILE_PATH = JSON_FILES_PATH + "store_patient.json"
    _ID_FIELD = KeyLabel.VPR_PATIENT_SYS_ID.value

    def add_item( self, item ):
        """Overrides the add_item to verify the item to be stored"""
        # pylint: disable=import-outside-toplevel, cyclic-import
        from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
        if not isinstance(item,VaccinePatientRegister):
            raise VaccineManagementException(ErrorMsg.NOT_VALID_PATIENT_OBJ.value)

        patient_found = False
        patient_records = self.find_items_list\
            (item.patient_id,KeyLabel.VPR_PATIENT_ID.value)
        for patient_recorded in patient_records:
            if (patient_recorded[KeyLabel.VPR_REGISTRATION_TYPE.value]
                == item.vaccine_type) \
                    and \
                    (patient_recorded[KeyLabel.VPR_FULL_NAME.value]
                     == item.full_name):
                raise VaccineManagementException(ErrorMsg.ALREADY_REGISTERED_PATIENT.value)

        if not patient_found:
            super().add_item(item)
