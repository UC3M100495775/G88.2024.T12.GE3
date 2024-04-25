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
        # leo los datos del fichero si existe , y si no existe creo una
        # lista vacía
        try:
            with open(file_store, "r", encoding="utf-8",
                      newline="") as file:
                list = json.load(file)
        except FileNotFoundError as file_not_found_error:
            list = []
        except json.JSONDecodeError as json_decode_error:
            raise HotelManagementException("JSON Decode Error - Wrong "
                                           "JSON Format") from json_decode_error
        return list

    @staticmethod
    def write_json(file, list):
        # Method for writing the data from the given
        # list in the given file
        try:
            with open(file, "w", encoding="utf-8",
                      newline="") as file:
                json.dump(list, file, indent=2)
        except FileNotFoundError as file_not_found_error:
            raise HotelManagementException("Wrong file  or file path") \
                from file_not_found_error

    def read_json_not_empty(self, file, prev_function):
        try:
            if prev_function == "read_data_from_json":
                with open(file, encoding='utf-8') as json_file:
                    list = json.load(json_file)
            else:
                with open(file, "r", encoding="utf-8",
                          newline="") as file:
                    list = json.load(file)
        except FileNotFoundError as file_not_found_error:
            self.read_json_raising_errors(file_not_found_error,
                                          prev_function)
        except json.JSONDecodeError as json_decode_error:
            raise HotelManagementException("JSON Decode Error - Wrong "
                                           "JSON Format") from json_decode_error
        return list

    def read_json_raising_errors(self, file_not_found_error,
                                 prev_function):
        if prev_function == "read_data_from_json":
            raise HotelManagementException("Wrong file or file "
                                           "path") from file_not_found_error
        elif prev_function == "guest_arrival":
            raise HotelManagementException("Error: store reservation not "
                                           "found") from file_not_found_error
        elif prev_function == "guest_checkout":
            raise HotelManagementException("Error: store checkin "
                                           "not found") from file_not_found_error
        elif prev_function == "guest_arrival":
            raise HotelManagementException("Error: file input not "
                                           "found") from file_not_found_error


    @staticmethod
    def validate_id_card(my_id_card):
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
