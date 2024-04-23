from uc3m_travel.attributes.attribute import Attribute
from uc3m_travel.hotel_management_exception import HotelManagementException

class NumDays(Attribute):
    """Definition of attribute NumDays"""

    #pylint: disable=super-init-not-called, too-few-public-methods
    def __init__(self, attr_value):
        """Definition of attribute NumDays init"""
        self._validation_pattern = r'^[0-9]{8}[A-Z]{1}$'
        self._error_message = "Invalid IdCard format"
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value):
        try:
            days = int(attr_value)
        except ValueError as value_error:
            raise HotelManagementException("Invalid num_days datatype") from\
                value_error
        if (days < 1 or days > 10):
            raise HotelManagementException(
                "Numdays should be in the range 1-10")
        return attr_value

