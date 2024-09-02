"""Classs for the attribute PatientId"""
import uuid
from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.exception.error_msg import ErrorMsg

#pylint: disable=too-few-public-methods
class PatientId(Attribute):
    """Classs for the attribute PatientId"""
    _validation_pattern = r"^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]{3}" \
                          r"-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$"
    _validation_error_message = ErrorMsg.NOT_VALID_UUID.value

    def _validate( self, attr_value ):
        """overrides the validate method to include the valiation of  UUID values"""
        try:
            patient_uuid = uuid.UUID(attr_value)
        except ValueError as val_er:
            raise VaccineManagementException(ErrorMsg.NOT_VALID_ID.value) from val_er
        return super()._validate(patient_uuid.__str__())
