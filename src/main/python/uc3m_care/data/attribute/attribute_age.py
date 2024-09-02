"""Classs for the attribute age"""
from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.exception.error_msg import ErrorMsg

#pylint: disable=too-few-public-methods
class Age(Attribute):
    """Classs for the attribute age"""
    _validation_error_message = ErrorMsg.NOT_VALID_AGE.value

    def _validate( self, attr_value: str ) -> str:
        """Validates the age according to the requirements"""
        if attr_value.isnumeric():
            if (int(attr_value) < 6 or int(attr_value) > 125):
                raise VaccineManagementException(self._validation_error_message)
        else:
            raise VaccineManagementException(self._validation_error_message)
        return attr_value
