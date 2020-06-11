from django.test import TestCase
from .models import rental
# Create your tests here.
class Test(TestCase):
    def setUp(self):
        self.test_rental = rental.objects.create(start_time='10-9-2020',end_time='10-10-2020',owner = "hi@gmail.com",rental_unique_id = "123",total_cost = 50.0,charge_id = "123abc",refund_status = False,server_id = "321cba",)

    def tearDown(self):
        del self.test_rental
    
    def test_value_start_time(self):
        expected_start_time = '10-9-2020'
        self.assertEqual(self.test_rental.start_time, expected_start_time)
    
     def test_value_end_time(self):
        expected_end_time = '10-10-2020'
        self.assertEqual(self.test_rental.end_time, expected_end_time)
    
     def test_value_owner(self):
        expected_owner = "hi@gmail.com"
        self.assertEqual(self.test_rental.owner, expected_owner)
    
     def test_value_rental_unique_id(self):
        expected_rental_unique_id = "123"
        self.assertEqual(self.test_rental.rental_unique_id, expected_rental_unique_id)
    
     def test_value_total_cost(self):
        expected_total_cost = 50.0
        self.assertEqual(self.test_rental.total_cost, expected_total_cost)
    
     def test_value_charge_id(self):
        expected_charge_id = "123abc"
        self.assertEqual(self.test_rental.charge_id, expected_charge_id)
    
     def test_value_refund_status(self):
        expected_refund_status = False
        self.assertEqual(self.test_rental.refund_status, expected_refund_status)
    
     def test_value_server_id(self):
        expected_server_id= "321cba"
        self.assertEqual(self.test_rental.server_id, expected_server_id)

    