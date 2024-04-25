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

class HotelManager:
    class __HotelManager:
        """Class with all the methods for managing reservations and stays"""
        def __init__(self):
            pass

        @staticmethod
        def validatecreditcard(card_number):
            """validates the credit card number using luhn altorithm"""
            #taken form
            # https://allwin-raju-12.medium.com/
            # credit-card-number-validation-using-luhns-algorithm-in-python-c0ed2fac6234
            # PLEASE INCLUDE HERE THE CODE FOR VALIDATING THE GUID
            # RETURN TRUE IF THE GUID IS RIGHT, OR FALSE IN OTHER CASE
            credit_card = CreditCard(card_number)
            return credit_card.value

        @staticmethod
        def validate_arrival_date(arrival_date):
            """validates the arrival date format  using regex"""
            date = ArrivalDate(arrival_date)
            return date.value

        @staticmethod
        def validate_phonenumber(phone_number):
            """validates the phone number format  using regex"""
            phone = PhoneNumber(phone_number)
            return phone.value

        @staticmethod
        def validate_numdays(num_days):
            """validates the number of days"""
            days = NumDays(num_days)
            return days.value

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

        @staticmethod
        def validate_name_surname(name_surname):
            name = NameSurname(name_surname)
            return name.value

        @staticmethod
        def validate_id_card(my_id_card):
            id_card = IdCard(my_id_card)
            return id_card.value

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

            reservation_store = JsonStore()
            return reservation_store.save_reservation(my_reservation)

        def guest_arrival(self, file_input:str)->str:
            checkin = JsonStore()
            return checkin.save_chekin(file_input)

        def guest_checkout(self, room_key:str)->bool:
            checkout = JsonStore()
            return checkout.save_checkout(room_key)

    __instance = None;
    def __new__(cls):
        if not HotelManager.__instance:
            HotelManager.__instance = HotelManager.__HotelManager()
        return HotelManager.__instance
