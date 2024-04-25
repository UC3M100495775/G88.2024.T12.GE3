import json
from datetime import datetime
from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.hotel_reservation import HotelReservation
from uc3m_travel.hotel_stay import HotelStay
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from uc3m_travel.attributes.attribute_localizer import Localizer
from uc3m_travel.attributes.attribute_id_card import IdCard
from uc3m_travel.attributes.attribute_roomkey import RoomKey
from freezegun import freeze_time

class JsonStore():
    """JsonStore class"""
    _data_list = []
    _file_name = ""

    def __init__(self):
        pass

    def save_reservation(self, reservation_data):
        # I write the Json file with all the data
        file_store = JSON_FILES_PATH + "store_reservation.json"

        data_list = self.load_json_store(file_store)

        # compruebo que esta reserva no esta en la lista
        for item in data_list:
            if reservation_data.localizer == item[
                "_HotelReservation__localizer"]:
                raise HotelManagementException("Reservation already exists")
            if reservation_data.id_card == item["_HotelReservation__id_card"]:
                raise HotelManagementException(
                    "This ID card has another reservation")
        # añado los datos de mi reserva a la lista , a lo que hubiera
        data_list.append(reservation_data.__dict__)

        # escribo la lista en el fichero
        self.write_json(file_store, data_list)

        return reservation_data.localizer

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

    def save_chekin(self, checkin_data):
        """manages the arrival of a guest with a reservation"""
        input_list = self.read_json_not_empty(checkin_data, "guest_arrival")

        # comprobar valores del fichero
        try:
            my_localizer = input_list["Localizer"]
            my_id_card = input_list["IdCard"]
        except KeyError as key_error:
            raise HotelManagementException("Error - Invalid Key in "
                                               "JSON") from key_error

        # This will have to be changed when the JSON store classes are
        # implemented
        # new_reservation = HotelReservation.create_reservation_from_arrival(my_id_card,my_localizer)
        new_reservation = self.create_reservation_from_arrival(my_id_card, my_localizer)

        # compruebo si hoy es la fecha de checkin
        reservation_format = "%d/%m/%Y"
        date_obj = datetime.strptime(new_reservation.arrival,
                                         reservation_format)
        if date_obj.date() != datetime.date(datetime.utcnow()):
            raise HotelManagementException("Error: today is not reservation date")

        # genero la room key para ello llamo a Hotel Stay
        my_checkin = HotelStay(idcard=my_id_card, numdays=int(
            new_reservation.num_days),
                                localizer=my_localizer,
                                roomtype=new_reservation.room_type)

        #Ahora lo guardo en el almacen nuevo de checkin
        # escribo el fichero Json con todos los datos
        file_store = JSON_FILES_PATH + "store_check_in.json"

        room_key_list = self.load_json_store(file_store)

        # comprobar que no he hecho otro ckeckin antes
        for item in room_key_list:
            if my_checkin.room_key == item["_HotelStay__room_key"]:
                raise HotelManagementException ("ckeckin  ya realizado")

        #añado los datos de mi reserva a la lista , a lo que hubiera
        room_key_list.append(my_checkin.__dict__)

        self.write_json(file_store, room_key_list)

        return my_checkin.room_key

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

    def create_reservation_from_arrival(self, my_id_card, my_localizer):
        self.validate_id_card(my_id_card)
        self.validate_localizer(my_localizer)

        # self.validate_localizer() hay que validar
        # buscar en almacen
        file_store = JSON_FILES_PATH + "store_reservation.json"
        # leo los datos del fichero , si no existe deber dar error porque el almacen de reserva
        # debe existir para hacer el checkin
        store_list = self.read_json_not_empty(file_store, "guest_arrival")
        # compruebo si esa reserva esta en el almacen
        reservation = self.find_reservation(my_localizer, store_list)
        if my_id_card != reservation["_HotelReservation__id_card"]:
            raise HotelManagementException(
                "Error: Localizer is not correct for this IdCard")
        # regenerar clave y ver si coincide
        reservation_date = datetime.fromtimestamp(
            reservation["_HotelReservation__reservation_date"])
        with freeze_time(reservation_date):
            new_reservation = HotelReservation(
                credit_card_number=reservation[
                    "_HotelReservation__credit_card_number"],
                id_card=reservation["_HotelReservation__id_card"],
                num_days=reservation["_HotelReservation__num_days"],
                room_type=reservation["_HotelReservation__room_type"],
                arrival=reservation["_HotelReservation__arrival"],
                name_surname=reservation[
                    "_HotelReservation__name_surname"],
                phone_number=reservation[
                    "_HotelReservation__phone_number"])
        if new_reservation.localizer != my_localizer:
            raise HotelManagementException(
                "Error: reservation has been manipulated")
        return new_reservation

    def find_reservation(self, my_localizer, store_list):
        for item in store_list:
            if my_localizer == item["_HotelReservation__localizer"]:
                return item
        raise HotelManagementException("Error: localizer not found")

    @staticmethod
    def validate_id_card(my_id_card):
        id_card = IdCard(my_id_card)
        return id_card.value

    @staticmethod
    def validate_localizer(localizer_value):
        """validates the localizer format using a regex"""
        localizer = Localizer(localizer_value)
        return localizer.value

    def save_checkout(self, checkout_data):
        """manages the checkout of a guest"""
        self.validate_roomkey(checkout_data)
        # check thawt the roomkey is stored in the checkins file
        file_store = JSON_FILES_PATH + "store_check_in.json"

        room_key_list = self.read_json_not_empty(file_store,
                                                 "guest_checkout")

        # comprobar que esa room_key es la que me han dado
        found = False
        for item in room_key_list:
            if checkout_data == item["_HotelStay__room_key"]:
                departure_date_timestamp = item["_HotelStay__departure"]
                found = True
        if not found:
            raise HotelManagementException("Error: room key not found")

        today = datetime.utcnow().date()
        if datetime.fromtimestamp(departure_date_timestamp).date() != today:
            raise HotelManagementException(
                "Error: today is not the departure day")

        file_store_checkout = JSON_FILES_PATH + "store_check_out.json"

        room_key_list = self.load_json_store(file_store_checkout)

        for checkout in room_key_list:
            if checkout["room_key"] == checkout_data:
                raise HotelManagementException("Guest is already out")

        room_checkout = {"room_key": checkout_data,
                         "checkout_time": datetime.timestamp(
                             datetime.utcnow())}

        room_key_list.append(room_checkout)

        self.write_json(file_store_checkout, room_key_list)

        return True

    @staticmethod
    def validate_roomkey(roomkey_value):
        """validates the roomkey format using a regex"""
        room_key = RoomKey(roomkey_value)
        return room_key.value
