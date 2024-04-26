"""Definition of attribute RoomKey"""
from uc3m_travel.attributes.attribute import Attribute

class RoomKey(Attribute):
    """Definition of attribute RoomKey"""

    #pylint: disable=super-init-not-called, too-few-public-methods
    def __init__(self, attr_value):
        """Definition of attribute RoomKey init"""
        self._validation_pattern = r'^[a-fA-F0-9]{64}$'
        self._error_message = "Invalid room key format"
        self._attr_value = self._validate(attr_value)
