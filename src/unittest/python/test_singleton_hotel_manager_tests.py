"""Test cases for the hotel manager singleton"""
from unittest import TestCase
# pylint: disable=import-error
from uc3m_travel import HotelManager
# pylint: disable=import-error
from uc3m_travel.attributes.attribute_name_surname import NameSurname
class MyTestCase(TestCase):
    """Test cases for the hotel manager singleton"""
    def test_singleton_hotel_manager(self):
        """Instance three singletons and check that
        they are all the same instance (pointing to the same memory address)"""
        manager1 = HotelManager()
        manager2 = HotelManager()
        manager3 = HotelManager()
        self.assertEqual(manager1, manager2)
        self.assertEqual(manager2, manager3)
        self.assertEqual(manager1, manager3)

        # We will now check that two classes without the singleton patter
        # will return different instances even if their value is the same.
        # For example with the NameSurname class.
        person_1 = NameSurname("Javier Castillo")
        person_2 = NameSurname("Javier Castillo")
        self.assertNotEqual(person_1, person_2)
