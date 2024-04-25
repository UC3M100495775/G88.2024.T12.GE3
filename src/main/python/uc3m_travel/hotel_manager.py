"""Module for the hotel manager"""
from uc3m_travel.hotel_reservation import HotelReservation
from uc3m_travel.attributes.attribute_phone_number import PhoneNumber
from uc3m_travel.attributes.attribute_arrival_date import ArrivalDate
from uc3m_travel.attributes.attribute_localizer import Localizer
from uc3m_travel.attributes.attribute_roomkey import RoomKey
from uc3m_travel.attributes.attribute_name_surname import NameSurname
from uc3m_travel.attributes.attribute_credit_card import CreditCard
from uc3m_travel.attributes.attribute_id_card import IdCard
from uc3m_travel.attributes.attribute_numdays import NumDays
from uc3m_travel.storage.json_store import JsonStore
from uc3m_travel.storage.reservation_json_store import ReservationStoreJson
from uc3m_travel.storage.stay_json_store import StayStoreJson
from uc3m_travel.storage.checkout_json_store import CheckoutStoreJson

class HotelManager:
    class __HotelManager:
        """Class with all the methods for managing reservations and stays"""
        def __init__(self):
            pass

        def validate(self, attribute, value):
            """Generic validation method"""
            validators = {
                "credit_card": CreditCard,
                "arrival_date": ArrivalDate,
                "phone_number": PhoneNumber,
                "num_days": NumDays,
                "localizer": Localizer,
                "room_key": RoomKey,
                "name_surname": NameSurname,
                "id_card": IdCard
            }
            validator = validators.get(attribute)
            if validator:
                return validator(value).value
            else:
                raise ValueError("Invalid attribute")

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

            self.validate("id_card", id_card)
            self.validate("name_surname", name_surname)
            credit_card = self.validate("credit_card", credit_card)
            arrival_date = self.validate("arrival_date", arrival_date)
            num_days = self.validate("num_days", num_days)
            phone_number = self.validate("phone_number", phone_number)

            my_reservation = HotelReservation(id_card=id_card,
                                              credit_card_number=credit_card,
                                              name_surname=name_surname,
                                              phone_number=phone_number,
                                              room_type=room_type,
                                              arrival=arrival_date,
                                              num_days=num_days)

            reservation_store = ReservationStoreJson()
            return reservation_store.save_reservation(my_reservation)

        def guest_arrival(self, file_input:str)->str:
            checkin = StayStoreJson()
            return checkin.save_chekin(file_input)

        def guest_checkout(self, room_key:str)->bool:
            checkout = CheckoutStoreJson()
            return checkout.save_checkout(room_key)

    __instance = None;
    def __new__(cls):
        if not HotelManager.__instance:
            HotelManager.__instance = HotelManager.__HotelManager()
        return HotelManager.__instance