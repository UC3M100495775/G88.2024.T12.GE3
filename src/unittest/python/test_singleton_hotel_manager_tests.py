import unittest
from unittest import TestCase
from uc3m_travel import HotelManager
class MyTestCase(TestCase):
    """Test cases for the hotel manager singleton"""
    def test_singleton_hotel_manager(self):
        """Instance three singletons and check that
        they are all the same instance (pointint to the same memory address)"""
        manager1 = HotelManager()
        manager2 = HotelManager()
        manager3 = HotelManager()
        self.assertEqual(manager1, manager2)
        self.assertEqual(manager2, manager3)
        self.assertEqual(manager1, manager3)