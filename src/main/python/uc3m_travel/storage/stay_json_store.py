from datetime import datetime
from uc3m_travel.storage.json_store import JsonStore
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.hotel_stay import HotelStay
from uc3m_travel.hotel_reservation import HotelReservation
from uc3m_travel.hotel_reservation import HotelReservation
from freezegun import freeze_time

class StayStoreJson(JsonStore):
    def save_checkin(self, checkin_data):
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
        new_reservation = HotelReservation.create_reservation_from_arrival(my_id_card, my_localizer)

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


    def find_reservation(self, my_localizer, store_list):
        for item in store_list:
            if my_localizer == item["_HotelReservation__localizer"]:
                return item
        raise HotelManagementException("Error: localizer not found")

