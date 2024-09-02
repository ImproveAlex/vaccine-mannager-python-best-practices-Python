"""Test"""
# pylint: disable=import-error, ungrouped-imports
import unittest
from datetime import datetime
from os import listdir
from freezegun import freeze_time
from uc3m_care.vaccine_manager import VaccineManager
from test_utils import TestUtils
from uc3m_care import JSON_FILES_RF4_PATH


class TestGetVaccineDate(unittest.TestCase):
    """Clase para probar el metodo cancel_appointment"""

    # Hemos decidido insertar directamente en los jsons
    # las citas y las vacunaciones en vez de utilizar
    # get_vaccine_date y vaccine_patient ya que estas funciones ya
    # se prueban en otros tests. Ademas al insertar directamente creemos que queda mas claro
    # lo que se esta haciendo.

    @freeze_time("2022-05-20")
    def setUp(self) -> None:
        """Reinicia los storages al principio de cada test"""
        justnow = datetime.utcnow()
        issued_time = datetime.timestamp(justnow)
        date_signature = "f2d18b9007cd19dbc83bd7c1da35a45de2e55f2565347b36e8c794b1642cb61a"
        date_signature_vac = "3a7d3ef6f4febd261d2719f173eddc79e67a5c00a4077c39d2f64d5555e569a4"
        # La fecha de la cita se ha elegido para dentro de 10 dias,
        # es decir, 2022-05-30
        # El date_signature de la cita coincide con el date_signature de los ficheros
        # ALL_OK_1.json y ALL_OK_2.json
        self.test_appointment = {
            "_VaccinationAppointment__alg": "SHA-256",
            "_VaccinationAppointment__type": "DS",
            "_VaccinationAppointment__patient_sys_id": "72b72255619afeed8bd26861a2bc2caf",
            "_VaccinationAppointment__patient_id": "78924cb0-075a-4099-a3ee-f3b562e805b9",
            "_VaccinationAppointment__phone_number": "+34123456789",
            "_VaccinationAppointment__issued_at": issued_time,
            "_VaccinationAppointment__appointment_date": issued_time + (10 * 24 * 60 * 60),
            "_VaccinationAppointment__date_signature": date_signature,
            "_VaccinationAppointment__cancelled": False
        }

        self.test_vaccine = {
            "_VaccinationLog__date_signature": date_signature_vac,
            "_VaccinationLog__timestamp": issued_time + (10 * 24 * 60 * 60)
        }

        TestUtils.clear_all_storages()

    # TESTS CLASES DE EQUIVALENCIA

    @freeze_time("2022-05-21")
    def test_all_ok_ec(self):
        """Tests ALL_OK_1 y ALL_OK_2 obtenidos mediante EC"""
        my_manager = VaccineManager()
        directory_path = JSON_FILES_RF4_PATH + "all_ok/"
        test_names = list(listdir(directory_path))
        # Añadimos la cita de prueba al storage correspondiente
        TestUtils.add_store_date(self.test_appointment)
        for file_name in test_names:
            # Añadimos la cita
            TestUtils.add_store_date(self.test_appointment)
            file_path = directory_path + file_name
            # Ejecutamos la funcion
            my_manager.cancel_appointment(file_path)
            # Comprobamos que la cita este cancelada
            appointment = TestUtils.read_store_date()[0]
            self.assertTrue(appointment["_VaccinationAppointment__cancelled"])
            # Limpiamos el storage para la siguiente entrada
            TestUtils.clear_store_date()

    def test_wrong_date_signature(self):
        """Tests para los casos donde date signature sea invalido
            TEST_DATE_SIGNATURE_INVAL1 y TEST_DATE_SIGNATURE_INVAL_2
            obtenidos mediante EC"""
        my_manager = VaccineManager()
        directory_path = JSON_FILES_RF4_PATH + "wrong_date_signature/"
        test_names = list(listdir(directory_path))
        exception_message = ""
        # Ejecutamos el test para cada json en el directorio y comprobamos el resultado
        for file_name in test_names:
            file_path = directory_path + file_name
            try:
                my_manager.cancel_appointment(file_path)
            # pylint: disable=broad-except
            except Exception as exception_raised:
                exception_message = exception_raised.__str__()
            self.assertEqual(exception_message, "date_signature format is not valid")

    def test_wrong_cancellation_type(self):
        """Tests para los casos en los que el tipo de cancelacion sea invalido
        TEST_CANCEL_TYPE_INVAL_1 y TEST_CANCEL_TYPE_INVAL_2 obtenidos mediante EC"""
        my_manager = VaccineManager()
        directory_path = JSON_FILES_RF4_PATH + "wrong_cancellation_type/"
        test_names = list(listdir(directory_path))
        exception_message = ""
        # Ejecutamos el test para cada json en el directorio y comprobamos el resultado
        for file_name in test_names:
            file_path = directory_path + file_name
            try:
                my_manager.cancel_appointment(file_path)
            # pylint: disable=broad-except
            except Exception as exception_raised:
                exception_message = exception_raised.__str__()
            self.assertEqual(exception_message, "Invalid cancelation type")

    def test_wrong_reason(self):
        """Tests para los casos en los que la razon de cancelacion sea invalida
        TEST_REASON_INVAL_1, TEST_REASON_INVAL_2 y TEST_REASON_INVAL_3 obtenidos mediante EC"""
        my_manager = VaccineManager()
        directory_path = JSON_FILES_RF4_PATH + "wrong_reason/"
        test_names = list(listdir(directory_path))
        exception_message = ""
        # Ejecutamos el test para cada json en el directorio y comprobamos el resultado
        for file_name in test_names:
            file_path = directory_path + file_name
            try:
                my_manager.cancel_appointment(file_path)
            # pylint: disable=broad-except
            except Exception as exception_raised:
                exception_message = exception_raised.__str__()
            self.assertEqual(exception_message, "Invalid cancelation reason")

    # TESTS GRAMATICA

    def test_wrong_json_structure(self):
        """Tests para los casos en los que la estructura del JSON sea incorrecta
        Incluye la mayoria de tests obtenidos mediante la gramatica"""
        my_manager = VaccineManager()
        directory_path = JSON_FILES_RF4_PATH + "wrong_json_format/"
        test_names = list(listdir(directory_path))
        exception_message = ""
        for file_name in test_names:
            file_path = directory_path + file_name
            try:
                my_manager.cancel_appointment(file_path)
            # pylint: disable=broad-except
            except Exception as exception_raised:
                exception_message = exception_raised.__str__()
            self.assertEqual(exception_message, "JSON Decode Error - Wrong JSON Format")

    def test_bad_labels(self):
        """Test para los mensajes de error del parser al haber una label incorrecta, obtenidos
        mediante la gramatica"""
        my_manager = VaccineManager()
        directory_paths = [(JSON_FILES_RF4_PATH + "bad_label_cancellation_type/",
                            "Bad label cancelation type"),
                           (JSON_FILES_RF4_PATH + "bad_label_date_signature/",
                            "Bad label date signature"),
                           (JSON_FILES_RF4_PATH + "bad_label_reason/",
                            "Bad label reason")]
        exception_message = ""
        for directory in directory_paths:
            test_names = list(listdir(directory[0]))
            for file_name in test_names:
                file_path = directory[0] + file_name
                try:
                    my_manager.cancel_appointment(file_path)
                # pylint: disable=broad-except
                except Exception as exception_raised:
                    exception_message = exception_raised.__str__()
                self.assertEqual(exception_message, directory[1])

    # TESTS ANALISIS ESTRUCTURAL

    @freeze_time("2022-05-21")
    def test_all_ok_estructural_analysis(self):
        """Tests ALL_OK_3 y ALL_OK_4 obtenidos mediante analisis estructural"""
        my_manager = VaccineManager()
        file_path = JSON_FILES_RF4_PATH + "all_ok/ALL_OK_1.json"

        # ALL_OK_3
        # Se recorre el bucle al buscar las vacunaciones mas de una vez
        # Almacenamos varias vacunas (asegurandonos de que el date_signature no coincida
        # con el de la cita que queremos cancelar)

        TestUtils.add_store_date(self.test_appointment)
        TestUtils.add_store_vaccine(self.test_vaccine)
        test_vaccine_2 = self.test_vaccine.copy()
        TestUtils.add_store_vaccine(test_vaccine_2)

        my_manager.cancel_appointment(file_path)
        appointment = TestUtils.read_store_date()[0]
        # Comprobamos que se ha cancelado la cita (cogemos la primera cita porque solo hay una)
        self.assertTrue(appointment["_VaccinationAppointment__cancelled"])

        # ALL_OK_4
        # Se recorre el bucle al buscar las citas mas de una vez, almacenamos 2 citas
        # almacenando la que buscamos la ultima

        TestUtils.clear_all_storages()
        test_app_2 = self.test_appointment.copy()
        key = "_VaccinationAppointment__date_signature"
        fake_date_signature = "fd8b79030d29b4ac6aa1ad630530992903fadd3f7796aeb31b15145a7c0fac27"
        test_app_2[key] = fake_date_signature
        TestUtils.add_store_date(test_app_2)
        TestUtils.add_store_date(self.test_appointment)
        # Comprobamos que se ha cancelado la cita
        my_manager.cancel_appointment(file_path)
        for appointment in TestUtils.read_store_date():
            if appointment[key] == self.test_appointment[key]: # Misma key que hay en ALL_OK_1.json
                self.assertTrue(appointment["_VaccinationAppointment__cancelled"])

    def test_vaccine_already_administrated(self):
        """Test en el que la vacuna cuya cita se quiere cancelar ya ha sido administrada
        test VACCINE_ALREADY_ADMINISTRATED obtenido mediante analisis estructural"""
        my_manager = VaccineManager()
        file_path = JSON_FILES_RF4_PATH + "all_ok/ALL_OK_1.json"
        exception_message = ""

        # Añadimos una vacuna al log de vacunas con el mismo date_signature de la cita
        # que queremos cancelar
        vaccine = self.test_vaccine.copy()
        vaccine["_VaccinationLog__date_signature"] = \
            self.test_appointment["_VaccinationAppointment__date_signature"]
        TestUtils.add_store_date(self.test_appointment)
        TestUtils.add_store_vaccine(vaccine)
        try:
            my_manager.cancel_appointment(file_path)
        # pylint: disable=broad-except
        except Exception as exception_raised:
            exception_message = exception_raised.__str__()
        self.assertEqual(exception_message, "Vaccination has already been administered")

    @freeze_time("2022-06-30")
    def test_appointment_expired(self):
        """Test en el que la cita que se intenta cancelar ya ha expirado.
        test APPOINTMENT_EXPIRED obtenido mediante analisis estructural"""
        my_manager = VaccineManager()
        file_path = JSON_FILES_RF4_PATH + "all_ok/ALL_OK_1.json"
        exception_message = ""

        # La cita que insertamos tiene como fecha 2022-05-30
        # Ponemos como fecha actual el 2022-06-30 por ejemplo
        TestUtils.add_store_date(self.test_appointment)
        try:
            my_manager.cancel_appointment(file_path)
            # pylint: disable=broad-except
        except Exception as exception_raised:
            exception_message = exception_raised.__str__()
        self.assertEqual(exception_message, "Appointment has expired")

    def test_appointment_already_cancelled(self):
        """Test en el que la cita ya fue cancelada previamente.
        test APPOINTMENT_ALREADY_CANCELLED obtenido mediante analisis estructural"""
        my_manager = VaccineManager()
        file_path = JSON_FILES_RF4_PATH + "all_ok/ALL_OK_1.json"
        exception_message = ""

        # Añadimos una cita ya cancelada
        appointment = self.test_appointment.copy()
        appointment["_VaccinationAppointment__cancelled"] = True
        TestUtils.add_store_date(appointment)
        try:
            my_manager.cancel_appointment(file_path)
        # pylint: disable=broad-except
        except Exception as exception_raised:
            exception_message = exception_raised.__str__()
        self.assertEqual(exception_message, "Appointment is already cancelled")

    def test_appointment_not_found(self):
        """Test en el que la cita que se intenta cancelar no existe
        test APPOINTMENT_NOT_FOUND obtenido mediante analisis estructural"""
        my_manager = VaccineManager()
        file_path = JSON_FILES_RF4_PATH + "all_ok/ALL_OK_1.json"
        exception_message = ""

        # Añadimos una cita cuyo date_signature no coincide con el de nuestro fichero
        appointment = self.test_appointment.copy()
        fake_date_signature = "9859dba7ea9a8e59d7f6f78165bba989b2618f584f9d97452beab11d0595d4a6"
        appointment["_VaccinationAppointment__date_signature"] = fake_date_signature
        try:
            my_manager.cancel_appointment(file_path)
        # pylint: disable=broad-except
        except Exception as exception_raised:
            exception_message = exception_raised.__str__()
        self.assertEqual(exception_message, "Appointment does not exist")






if __name__ == '__main__':
    unittest.main()
