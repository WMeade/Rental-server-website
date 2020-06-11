from django.test import TestCase
from .models import server_component
# Create your tests here.
class Test(TestCase):
    def setUp(self):
        self.test_server_component = server_component.objects.create(part_id = "34, RTX TITAN",part_type = "GPU",rental_cost = 50.0,quantity = 175,hardware_cost = 200.0,specifications = "24GB VRAM",socket_type = "PCIE")

    def tearDown(self):
        del self.test_server_component

    def test_value_part_id(self):
        expected_part_id = "34, RTX TITAN"
        self.assertEqual(self.test_user.part_id, expected_part_id)

    def test_value_part_type(self):
        expected_part_type = "GPU"
        self.assertEqual(self.test_user.part_type, expected_part_type)

    def test_value_rental_cost(self):
        expected_rental_cost = 50.0
        self.assertEqual(self.test_user.rental_cost, expected_rental_cost)

    def test_value_quantity(self):
        expected_quantity = 175
        self.assertEqual(self.test_user.quantity, expected_quantity)

    def test_value_hardware_cost(self):
        expected_hardware_cost = 200.0
        self.assertEqual(self.test_user.hardware_cost, expected_hardware_cost)

    def test_value_specifications(self):
        expected_specifications = "24GB VRAM"
        self.assertEqual(self.test_user.specifications, expected_specifications)
