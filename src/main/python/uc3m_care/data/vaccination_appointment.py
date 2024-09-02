"""Contains the class Vaccination Appointment"""
# pylint: disable=import-error,too-few-public-methods
from datetime import datetime
import hashlib
from freezegun import freeze_time
from uc3m_care.data.attribute.attribute_phone_number import PhoneNumber
from uc3m_care.data.attribute.attribute_patient_system_id import PatientSystemId
from uc3m_care.parser.cancel_appointment_json_parser import CancelAppointmentJsonParser
from uc3m_care.data.attribute.attribute_cancelation_type import CancelationType
from uc3m_care.data.attribute.attribute_cancelation_reason import CancelationReason
from uc3m_care.data.attribute.attribute_date_signature import DateSignature
from uc3m_care.data.vaccination_log import VaccinationLog
from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.data.key_lables import KeyLabel
from uc3m_care.exception.error_msg import ErrorMsg
from uc3m_care.storage.appointments_json_storage import AppointmentsJsonStore
from uc3m_care.parser.appointment_json_parser import AppointmentJsonParser
from uc3m_care.data.validate_dates import ValidateDates


# pylint: disable=too-many-instance-attributes, unused-private-member
class VaccinationAppointment:
    """Class representing an appointment  for the vaccination of a patient"""

    def __init__( self, patient_sys_id, patient_phone_number, date: float):
        self.__alg = KeyLabel.ALG.value
        self.__type = KeyLabel.ALG_TYPE.value
        self.__patient_sys_id = PatientSystemId(patient_sys_id).value
        patient = VaccinePatientRegister.create_patient_from_patient_system_id(
            self.__patient_sys_id)
        self.__patient_id = patient.patient_id
        self.__phone_number = PhoneNumber(patient_phone_number).value
        justnow = datetime.utcnow()
        self.__issued_at = datetime.timestamp(justnow)

        # Si se pasa directamente como timestamp, no hacemos ninguna conversion mas

        self.__appointment_date = date

        self.__date_signature = self.vaccination_signature

        self.__cancelled = False



    def __signature_string(self):
        """Composes the string to be used for generating the key for the date"""
        return "{alg:" + self.__alg +",typ:" + self.__type +",patient_sys_id:" + \
               self.__patient_sys_id + ",issuedate:" + self.__issued_at.__str__() + \
               ",vaccinationtiondate:" + self.__appointment_date.__str__() + "}"

    @property
    def patient_id( self ):
        """Property that represents the guid of the patient"""
        return self.__patient_id

    @patient_id.setter
    def patient_id( self, value ):
        self.__patient_id = value

    @property
    def patient_sys_id(self):
        """Property that represents the patient_sys_id of the patient"""
        return self.__patient_sys_id
    @patient_sys_id.setter
    def patient_sys_id(self, value):
        self.__patient_sys_id = value

    @property
    def phone_number( self ):
        """Property that represents the phone number of the patient"""
        return self.__phone_number

    @phone_number.setter
    def phone_number( self, value ):
        self.__phone_number = PhoneNumber(value).value

    @property
    def vaccination_signature( self ):
        """Returns the sha256 signature of the date"""
        return hashlib.sha256(self.__signature_string().encode()).hexdigest()

    @property
    def issued_at(self):
        """Returns the issued at value"""
        return self.__issued_at

    @issued_at.setter
    def issued_at( self, value ):
        self.__issued_at = value

    @property
    def appointment_date( self ):
        """Returns the vaccination date"""
        return self.__appointment_date

    @property
    def date_signature(self):
        """Returns the SHA256 """
        return self.__date_signature

    def save_appointment(self):
        """saves the appointment in the appointments store"""
        appointments_store = AppointmentsJsonStore()
        appointments_store.add_item(self)

    @classmethod
    def get_appointment_from_date_signature(cls, date_signature):
        """returns the vaccination appointment object for the date_signature received"""
        appointments_store = AppointmentsJsonStore()
        appointment_record = appointments_store.find_item(DateSignature(date_signature).value)
        if appointment_record is None:
            raise VaccineManagementException(ErrorMsg.NOT_FOUND_DATE_SIGNATURE.value)
        freezer = freeze_time(
            datetime.fromtimestamp(appointment_record[KeyLabel.VA_ISSUE_DATE.value]))
        freezer.start()

        appointment = cls(appointment_record[KeyLabel.VA_PATIENT_SYS_ID.value],
                          appointment_record[KeyLabel.VA_PHONE_NUMBER.value],
                          appointment_record[KeyLabel.VA_APPOINTMENT_DATE.value])
        appointment.__cancelled = appointment_record[KeyLabel.VA_CANCELLED.value]
        freezer.stop()
        return appointment

    @classmethod
    def create_appointment_from_json_file(cls, json_file, date):
        """returns the vaccination appointment for the received input json file"""
        # Validamos la fecha
        vac_date_timestamp = ValidateDates.check_iso_date(date)

        appointment_parser = AppointmentJsonParser(json_file)
        new_appointment = cls(
            appointment_parser.json_content[appointment_parser.PATIENT_SYSTEM_ID_KEY],
            appointment_parser.json_content[appointment_parser.CONTACT_PHONE_NUMBER_KEY],
            vac_date_timestamp)
        return new_appointment

    @classmethod
    def cancel_appointment_from_json_file(cls, json_file):
        """returns the date signature of the canceled appointment"""
        cancel_appointment_parser = CancelAppointmentJsonParser(json_file)
        content_cancelation_request = cancel_appointment_parser.json_content
        # Validamos datos: date_signature, cancelation_type y reason
        date_signature = DateSignature(
            content_cancelation_request[KeyLabel.DATE_SIGNATURE.value]).value
        CancelationType(content_cancelation_request[KeyLabel.CANCELATION_TYPE.value])
        CancelationReason(content_cancelation_request[KeyLabel.REASON.value])
        # Comprobamos que no se haya administrado ya la vacuna
        VaccinationLog.check_vaccine_in_log(date_signature)
        # Validamos la cita
        VaccinationAppointment.validate_appointment(date_signature)
        return date_signature

    @classmethod
    def validate_appointment(cls, date_signature):
        """returns true if the appointment exists and it's valid"""
        app_storage = AppointmentsJsonStore()
        app_storage.load()
        found = False
        for appointment in app_storage.data_list:
            # Si se encuentra la cita
            if appointment[KeyLabel.VA_DATE_SIGNATURE.value] == date_signature:
                found = True
                # Comprobamos que la fecha de la cita no haya pasado ya
                appoitment_date = appointment[KeyLabel.VA_APPOINTMENT_DATE.value]
                ValidateDates.validate_appointment_date(appoitment_date)
                if appointment[KeyLabel.VA_CANCELLED.value]:
                    raise VaccineManagementException(ErrorMsg.ALREADY_CANCELLED.value)
                # Marcamos la cita como cancelada
                appointment[KeyLabel.VA_CANCELLED.value] = True
                break
        if not found:
            raise VaccineManagementException(ErrorMsg.NOT_FOUND_APPOINTMENT.value)
        app_storage.save()

    def register_vaccination(self):
        """register the vaccine administration"""
        if ValidateDates.is_valid_today(self.appointment_date):
            vaccination_log_entry = VaccinationLog(self.date_signature)
            vaccination_log_entry.save_log_entry()
        return True
