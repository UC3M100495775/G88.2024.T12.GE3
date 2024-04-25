from datetime import datetime
from uc3m_travel.storage.json_store import JsonStore
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from uc3m_travel.hotel_management_exception import HotelManagementException

class CheckoutStoreJson(JsonStore):
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
