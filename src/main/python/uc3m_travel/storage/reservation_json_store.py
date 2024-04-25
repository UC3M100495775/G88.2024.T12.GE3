from uc3m_travel.storage.json_store import JsonStore
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from uc3m_travel.hotel_management_exception import HotelManagementException

class ReservationStoreJson(JsonStore):
    def save_reservation(self, reservation_data):
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