"""Modulo para los enum de las claves"""
from enum import Enum

class KeyLabel(Enum):
    """Clase con las key labels"""
    ALG = "SHA-256"
    ALG_TYPE = "DS"
    PATIENT_SYSTEM_ID = "PatientSystemID"
    PHONE = "ContactPhoneNumber"
    DATE_SIGNATURE = 'date_signature'
    CANCELATION_TYPE = 'cancelation_type'
    REASON = 'reason'
    LOG_DATE_SIGNATURE = '_VaccinationLog__date_signature'

    # VPR es Vaccine Patient Register
    VPR_PATIENT_ID = "_VaccinePatientRegister__patient_id"
    VPR_REGISTRATION_TYPE = "_VaccinePatientRegister__registration_type"
    VPR_FULL_NAME = "_VaccinePatientRegister__full_name"
    VPR_PHONE_NUMBER = "_VaccinePatientRegister__phone_number"
    VPR_TIME_STAMP = "_VaccinePatientRegister__time_stamp"
    VPR_AGE = "_VaccinePatientRegister__age"
    VPR_PATIENT_SYS_ID = "_VaccinePatientRegister__patient_sys_id"

    # VA es Vaccination Appointment
    VA_ISSUE_DATE = "_VaccinationAppointment__issued_at"
    VA_PATIENT_SYS_ID = "_VaccinationAppointment__patient_sys_id"
    VA_PHONE_NUMBER = "_VaccinationAppointment__phone_number"
    VA_DATE_SIGNATURE = '_VaccinationAppointment__date_signature'
    VA_APPOINTMENT_DATE = '_VaccinationAppointment__appointment_date'
    VA_CANCELLED = '_VaccinationAppointment__cancelled'
