"""Hotel reservation class"""
import hashlib
from datetime import datetime
import re
from .hotel_management_exception import HotelManagementException
from uc3m_travel.attributes.attribute_phone_number import PhoneNumber
from uc3m_travel.attributes.attribute_arrival_date import ArrivalDate
from uc3m_travel.attributes.attribute_name_surname import NameSurname
from uc3m_travel.attributes.attribute_credit_card import CreditCard
from uc3m_travel.attributes.attribute_id_card import IdCard
from uc3m_travel.attributes.attribute_numdays import NumDays
from uc3m_travel.attributes.attribute_room_type import RoomType
from uc3m_travel.attributes.attribute_localizer import Localizer
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from freezegun import freeze_time
from uc3m_travel.storage.reservation_json_store import ReservationStoreJson

class HotelReservation:
    """Class for representing hotel reservations"""
    #pylint: disable=too-many-arguments, too-many-instance-attributes
    def __init__(self,
                 id_card:str,
                 credit_card_number:str,
                 name_surname:str,
                 phone_number:str,
                 room_type:str,
                 arrival:str,
                 num_days:int):
        """constructor of reservation objects"""
        self.__credit_card_number = CreditCard(credit_card_number).value
        self.__id_card = IdCard(id_card).value
        justnow = datetime.utcnow()
        self.__arrival = ArrivalDate(arrival).value
        self.__reservation_date = datetime.timestamp(justnow)
        self.__name_surname = NameSurname(name_surname).value
        self.__phone_number = PhoneNumber(phone_number).value
        self.__room_type = RoomType(room_type).value
        self.__num_days = NumDays(num_days).value
        self.__localizer =  hashlib.md5(str(self).encode()).hexdigest()

    def __str__(self):
        """return a json string with the elements required to calculate the localizer"""
        #VERY IMPORTANT: JSON KEYS CANNOT BE RENAMED
        json_info = {"id_card": self.__id_card,
                     "name_surname": self.__name_surname,
                     "credit_card": self.__credit_card_number,
                     "phone_number:": self.__phone_number,
                     "reservation_date": self.__reservation_date,
                     "arrival_date": self.__arrival,
                     "num_days": self.__num_days,
                     "room_type": self.__room_type,
                     }
        return "HotelReservation:" + json_info.__str__()

    ### CLASSMETHODS ###
    @classmethod
    def create_reservation_from_arrival(cls, my_id_card, my_localizer):
        reservation_store = ReservationStoreJson()
        reservation_store.validate_id_card(my_id_card)
        reservation_store.validate_localizer(my_localizer)

        # self.validate_localizer() hay que validar
        # buscar en almacen
        file_store = JSON_FILES_PATH + "store_reservation.json"
        # leo los datos del fichero , si no existe deber dar error porque el almacen de reserva
        # debe existir para hacer el checkin
        store_list = reservation_store.read_json_not_empty(file_store, "guest_arrival")
        # compruebo si esa reserva esta en el almacen
        reservation = HotelReservation.find_reservation(my_localizer, store_list)
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

    @classmethod
    def find_reservation(cls, my_localizer, store_list):
        for item in store_list:
            if my_localizer == item["_HotelReservation__localizer"]:
                return item
        raise HotelManagementException("Error: localizer not found")

    @property
    def credit_card(self):
        """property for getting and setting the credit_card number"""
        return self.__credit_card_number

    @credit_card.setter
    def credit_card(self, value):
        self.__credit_card_number = value

    @property
    def id_card(self):
        """property for getting and setting the id_card"""
        return self.__id_card

    @id_card.setter
    def id_card(self, value):
        self.__id_card = value

    @property
    def localizer(self):
        """Returns the md5 signature"""
        return self.__localizer

    @property
    def arrival(self):
        """Returns the arrival date"""
        return self.__arrival

    @property
    def num_days(self):
        """Returns the number of days"""
        return self.__num_days

    @property
    def room_type(self):
        """Returns the room type"""
        return self.__room_type

