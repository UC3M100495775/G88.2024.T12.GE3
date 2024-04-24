"""Module for the hotel manager"""
import re
import json
from datetime import datetime
from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.hotel_reservation import HotelReservation
from uc3m_travel.hotel_stay import HotelStay
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from uc3m_travel.attributes.attribute_phone_number import PhoneNumber
from uc3m_travel.attributes.attribute_arrival_date import ArrivalDate
from uc3m_travel.attributes.attribute_localizer import Localizer
from uc3m_travel.attributes.attribute_roomkey import RoomKey
from uc3m_travel.attributes.attribute_name_surname import NameSurname
from uc3m_travel.attributes.attribute_credit_card import CreditCard
from uc3m_travel.attributes.attribute_id_card import IdCard
from uc3m_travel.attributes.attribute_numdays import NumDays
from freezegun import freeze_time

class HotelManager:
    class __HotelManager:
        """Class with all the methods for managing reservations and stays"""
        def __init__(self):
            pass

        def validatecreditcard(self, card_number):
            """validates the credit card number using luhn altorithm"""
            #taken form
            # https://allwin-raju-12.medium.com/
            # credit-card-number-validation-using-luhns-algorithm-in-python-c0ed2fac6234
            # PLEASE INCLUDE HERE THE CODE FOR VALIDATING THE GUID
            # RETURN TRUE IF THE GUID IS RIGHT, OR FALSE IN OTHER CASE
            credit_card = CreditCard(card_number)
            return credit_card.value

        def validate_arrival_date(self, arrival_date):
            """validates the arrival date format  using regex"""
            date = ArrivalDate(arrival_date)
            return date.value

        def validate_phonenumber(self, phone_number):
            """validates the phone number format  using regex"""
            phone = PhoneNumber(phone_number)
            return phone.value

        def validate_numdays(self,num_days):
            """validates the number of days"""
            days = NumDays(num_days)
            return days.value

        def validate_localizer(self, localizer_value):
            """validates the localizer format using a regex"""
            localizer = Localizer(localizer_value)
            return localizer.value

        def validate_roomkey(self, roomkey_value):
            """validates the roomkey format using a regex"""
            room_key = RoomKey(roomkey_value)
            return room_key.value

        def validate_name_surname(self, name_surname):
            name = NameSurname(name_surname)
            return name.value

        def validate_id_card(self, my_id_card):
            id_card = IdCard(my_id_card)
            return id_card.value

        def read_data_from_json(self, json_file_path):
            """reads the content of a json file with two fields: CreditCard and phoneNumber"""
            json_data = self.read_json_not_empty(json_file_path,
                                                 "read_data_from_json")

            try:
                card_data = json_data["CreditCard"]
                phone_number = json_data["phoneNumber"]
                reservation_obj = HotelReservation(id_card="12345678Z",
                                       credit_card_number=card_data,
                                       name_surname="John Doe",
                                       phone_number=phone_number,
                                       room_type="single",
                                       num_days=3,
                                       arrival="20/01/2024")
            except KeyError as key_error:
                raise HotelManagementException("JSON Decode Error - Invalid "
                                               "JSON Key") from key_error
            if not self.validatecreditcard(card_data):
                raise HotelManagementException("Invalid credit card number")
            # Close the file
            return reservation_obj

        def load_json_store(self, file_store):
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

        def write_json(self, file, list):
            # Method for writing the data from the given
            # data in the given file
            try:
                with open(file, "w", encoding="utf-8",
                          newline="") as file:
                    json.dump(list, file, indent=2)
            except FileNotFoundError as file_not_found_error:
                raise HotelManagementException("Wrong file  or file path") \
                    from file_not_found_error

        # pylint: disable=too-many-arguments
        def room_reservation(self,
                             credit_card:str,
                             name_surname:str,
                             id_card:str,
                             phone_number:str,
                             room_type:str,
                             arrival_date: str,
                             num_days:int)->str:
            """manages the hotel reservation: creates a reservation and
            saves it into a json file"""

            self.validate_id_card(id_card)

            self.validate_name_surname(name_surname)
            credit_card = self.validatecreditcard(credit_card)
            arrival_date = self.validate_arrival_date(arrival_date)
            num_days = self.validate_numdays(num_days)
            phone_number = self.validate_phonenumber(phone_number)

            my_reservation = HotelReservation(id_card=id_card,
                                              credit_card_number=credit_card,
                                              name_surname=name_surname,
                                              phone_number=phone_number,
                                              room_type=room_type,
                                              arrival=arrival_date,
                                              num_days=num_days)

            # escribo el fichero Json con todos los datos
            file_store = JSON_FILES_PATH + "store_reservation.json"

            data_list = self.load_json_store(file_store)

            #compruebo que esta reserva no esta en la lista
            for item in data_list:
                if my_reservation.localizer == item["_HotelReservation__localizer"]:
                    raise HotelManagementException ("Reservation already exists")
                if my_reservation.id_card == item["_HotelReservation__id_card"]:
                    raise HotelManagementException("This ID card has another reservation")
            #añado los datos de mi reserva a la lista , a lo que hubiera
            data_list.append(my_reservation.__dict__)

            #escribo la lista en el fichero
            self.write_json(file_store, data_list)

            return my_reservation.localizer

        def guest_arrival(self, file_input:str)->str:
            """manages the arrival of a guest with a reservation"""
            input_list = self.read_json_not_empty(file_input, "guest_arrival")

            # comprobar valores del fichero
            try:
                my_localizer = input_list["Localizer"]
                my_id_card = input_list["IdCard"]
            except KeyError as key_error:
                raise HotelManagementException("Error - Invalid Key in "
                                               "JSON") from key_error

            self.validate_id_card(my_id_card)
            self.validate_localizer(my_localizer)
            # self.validate_localizer() hay que validar

            #buscar en almacen
            file_store = JSON_FILES_PATH + "store_reservation.json"

            #leo los datos del fichero , si no existe deber dar error porque el almacen de reservaa
            # debe existir para hacer el checkin
            store_list = self.read_json_not_empty(file_store, "guest_arrival")
            # compruebo si esa reserva esta en el almacen
            reservation = self.find_reservation(my_localizer, store_list)

            if my_id_card != reservation["_HotelReservation__id_card"]:
                raise HotelManagementException("Error: Localizer is not correct for this IdCard")
            # regenerar clave y ver si coincide
            reservation_date = datetime.fromtimestamp(reservation[
                                                          "_HotelReservation__reservation_date"])

            with freeze_time(reservation_date):
                new_reservation = HotelReservation(
                    credit_card_number=reservation[
                        "_HotelReservation__credit_card_number"],
                    id_card=reservation["_HotelReservation__id_card"],
                    num_days=reservation["_HotelReservation__num_days"],
                    room_type=reservation["_HotelReservation__room_type"],
                    arrival=reservation["_HotelReservation__arrival"],
                    name_surname=reservation["_HotelReservation__name_surname"],
                    phone_number=reservation["_HotelReservation__phone_number"])
            if new_reservation.localizer != my_localizer:
                raise HotelManagementException("Error: reservation has been manipulated")

            # compruebo si hoy es la fecha de checkin
            reservation_format = "%d/%m/%Y"
            date_obj = datetime.strptime(new_reservation.arrival,
                                         reservation_format)
            if date_obj.date()!= datetime.date(datetime.utcnow()):
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

        def find_reservation(self, my_localizer, store_list):
            for item in store_list:
                if my_localizer == item["_HotelReservation__localizer"]:
                    return item
            raise HotelManagementException("Error: localizer not found")

        def guest_checkout(self, room_key:str)->bool:
            """manages the checkout of a guest"""
            self.validate_roomkey(room_key)
            #check thawt the roomkey is stored in the checkins file
            file_store = JSON_FILES_PATH + "store_check_in.json"

            room_key_list = self.read_json_not_empty(file_store,
                                                     "guest_checkout")

            # comprobar que esa room_key es la que me han dado
            found = False
            for item in room_key_list:
                if room_key == item["_HotelStay__room_key"]:
                    departure_date_timestamp = item["_HotelStay__departure"]
                    found = True
            if not found:
                raise HotelManagementException ("Error: room key not found")

            today = datetime.utcnow().date()
            if datetime.fromtimestamp(departure_date_timestamp).date() != today:
                raise HotelManagementException("Error: today is not the departure day")

            file_store_checkout = JSON_FILES_PATH + "store_check_out.json"

            room_key_list = self.load_json_store(file_store_checkout)

            for checkout in room_key_list:
                if checkout["room_key"] == room_key:
                    raise HotelManagementException("Guest is already out")

            room_checkout={"room_key":  room_key, "checkout_time":datetime.timestamp(datetime.utcnow())}

            room_key_list.append(room_checkout)

            self.write_json(file_store_checkout, room_key_list)

            return True

    __instance = None;
    def __new__(cls):
        if not HotelManager.__instance:
            HotelManager.__instance = HotelManager.__HotelManager()
        return HotelManager.__instance
