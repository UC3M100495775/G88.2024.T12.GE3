"""JsonStore module"""
import json
from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.attributes.attribute_localizer import Localizer
from uc3m_travel.attributes.attribute_id_card import IdCard
from uc3m_travel.attributes.attribute_roomkey import RoomKey

class JsonStore():
    """JsonStore class"""
    _data_list = []
    _file_name = ""

    def __init__(self):
        pass

    @staticmethod
    def load_json_store(file_store):
        """Method for loading the data from the given file"""
        # leo los datos del fichero si existe , y si no existe creo una
        # lista vacía
        try:
            with open(file_store, "r", encoding="utf-8",
                      newline="") as file:
                json_list = json.load(file)
        # pylint: disable=unused-variable
        except FileNotFoundError as file_not_found_error:
            json_list = []
        except json.JSONDecodeError as json_decode_error:
            raise HotelManagementException("JSON Decode Error - Wrong "
                                           "JSON Format") from json_decode_error
        return json_list

    @staticmethod
    def write_json(file, json_list):
        """"Method for writing the data from the given list in the given file"""
        # Method for writing the data from the given
        # list in the given file
        try:
            with open(file, "w", encoding="utf-8",
                      newline="") as json_file:
                json.dump(json_list, json_file, indent=2)
        except FileNotFoundError as file_not_found_error:
            raise HotelManagementException("Wrong file  or file path") \
                from file_not_found_error

    def read_json_not_empty(self, file, prev_function):
        """Method for reading the data from the given file, assuming the file is not empty"""
        try:
            if prev_function == "read_data_from_json":
                with open(file, encoding='utf-8') as json_file:
                    json_list = json.load(json_file)
            else:
                with open(file, "r", encoding="utf-8",
                          newline="") as json_file:
                    json_list = json.load(json_file)
        except FileNotFoundError as file_not_found_error:
            self.read_json_raising_errors(file_not_found_error,
                                          prev_function)
        except json.JSONDecodeError as json_decode_error:
            raise HotelManagementException("JSON Decode Error - Wrong "
                                           "JSON Format") from json_decode_error
        return json_list

    def read_json_raising_errors(self, file_not_found_error,
                                 prev_function):
        """Method for raising errors when reading the data from the given file"""
        if prev_function == "read_data_from_json":
            raise HotelManagementException("Wrong file or file "
                                           "path") from file_not_found_error
        if prev_function == "guest_arrival":
            raise HotelManagementException("Error: store reservation not "
                                           "found") from file_not_found_error
        if prev_function == "guest_checkout":
            raise HotelManagementException("Error: store checkin "
                                           "not found") from file_not_found_error
        if prev_function == "guest_arrival":
            raise HotelManagementException("Error: file input not "
                                           "found") from file_not_found_error


    @staticmethod
    def validate_id_card(my_id_card):
        """validates the id card format using a regex"""
        id_card = IdCard(my_id_card)
        return id_card.value

    @staticmethod
    def validate_localizer(localizer_value):
        """validates the localizer format using a regex"""
        localizer = Localizer(localizer_value)
        return localizer.value

    @staticmethod
    def validate_roomkey(roomkey_value):
        """validates the roomkey format using a regex"""
        room_key = RoomKey(roomkey_value)
        return room_key.value
