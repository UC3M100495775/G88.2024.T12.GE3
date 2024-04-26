"""Definition of attribute NameSurname"""
from uc3m_travel.attributes.attribute import Attribute


class NameSurname(Attribute):
    """Definition of attribute NameSurname"""

    # pylint: disable=super-init-not-called, too-few-public-methods
    def __init__(self, attr_value):
        """Definition of attribute NameSurname init"""
        self._validation_pattern = r"^(?=^.{10,50}$)([a-zA-Z]+(\s[" \
                                    r"a-zA-Z]+)+)$"
        self._error_message = "Invalid name format"
        self._attr_value = self._validate(attr_value)
