"""Clase para metodos relacionados con la validacion de las fechas"""
from datetime import datetime
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.exception.error_msg import ErrorMsg


class ValidateDates:
    """Clase para validar fechas"""

    def __init__(self):
        pass

    @classmethod
    def validate_appointment_date (cls, date):
        """returns true if the appointment date is correct"""
        justnow = datetime.utcnow()
        time = datetime.timestamp(justnow)
        if date < time:
            raise VaccineManagementException(ErrorMsg.NOT_VALID_APPOINTMENT.value)
        return True

    @classmethod
    def check_iso_date(cls, date):
        """Comprueba que la fecha este en formato ISO y que no sea
        previa a la fecha actual"""
        try:
            vac_date = datetime.fromisoformat(date)
        except:
            # pylint: disable=raise-missing-from
            raise VaccineManagementException(ErrorMsg.NOT_VALID_DATE_FORMAT.value)
        today = datetime.utcnow()
        if vac_date <= today:
            raise VaccineManagementException(ErrorMsg.NOT_VALID_VACC_DATE.value)
        vac_date_timestamp = datetime.timestamp(vac_date)
        return vac_date_timestamp

    @classmethod
    def is_valid_today(cls, appointment_date):
        """returns true if today is the appointment's date"""
        today = datetime.today().date()
        date_patient = datetime.fromtimestamp(appointment_date).date()
        if date_patient != today:
            raise VaccineManagementException(ErrorMsg.INCORRECT_DATE.value)
        return True
