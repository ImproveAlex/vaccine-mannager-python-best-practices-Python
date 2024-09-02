"""Modulo con metodos que hemos utilizado para ayudarnos en la creacion de tests para el metodo
cancel_appointment"""
# pylint: disable=import-error
import json
from uc3m_care import JSON_FILES_PATH

class TestUtils:
    """Test setup for the Python unittest module."""

    store_patient = JSON_FILES_PATH + "store_patient.json"
    store_date = JSON_FILES_PATH + "store_date.json"
    store_vaccine = JSON_FILES_PATH + "store_vaccine.json"

    @classmethod
    def add_element_to_json_file(cls, path, new_elem: dict):
        """Add element to a json file"""
        with open(path, "r+", encoding="utf-8") as file:
            data = json.load(file)
            data.append(new_elem)
            file.seek(0)
            json.dump(data, file, indent=2)

    @classmethod
    def read_json_file(cls, path):
        """Read a json file"""
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    @classmethod
    def clear_json_file(cls, path):
        """Clear a json file"""
        with open(path, "w", encoding="utf-8") as file:
            json.dump([], file)

    @classmethod
    def clear_all_storages(cls):
        """Vacia todas las storages"""
        cls.clear_json_file(cls.store_date)
        cls.clear_json_file(cls.store_patient)
        cls.clear_json_file(cls.store_vaccine)

    @classmethod
    def clear_store_date(cls):
        """Vacia store date"""
        cls.clear_json_file(cls.store_date)

    # Metodos para introducir datos en los jsons individuales
    @classmethod
    def add_store_date(cls, content):
        """Adds element to vaccination appointments"""
        cls.add_element_to_json_file(cls.store_date, content)

    @classmethod
    def add_store_vaccine(cls, content):
        """Adds element to vaccination appointments"""
        cls.add_element_to_json_file(cls.store_vaccine, content)

    @classmethod
    def read_store_date(cls):
        """Lee store_date.json"""
        data = cls.read_json_file(cls.store_date)
        return data
