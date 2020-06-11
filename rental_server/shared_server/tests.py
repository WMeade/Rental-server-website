from django.test import TestCase
from .models import user_saved
from servers.models import unrented_server
# Create your tests here.
class Test(TestCase):
    def setUp(self):
        self.test_server = unrented_server.create(secondary_id="0000", server_id="0000", CPU="Ryzen 3 3900x",motherboard="X570 AORUS XTREME", RAM="4x32gb RAM", HDD="50 tb HDD", SSD="10tb SSD", GPU="SLI QUADRO 8000")

    def tearDown(self):
        del self.test_server

    def test_value_secondary_id(self):
        expected_secondary_id = "0000"
        self.assertEqual(self.test_server.secondary_id, expected_secondary_id)
    
    def test_server_id(self)
    expected_server_id = "0000"
        self.assertEqual(self.test_server.server_id, expected_server_id)
    
    def test_CPU(self)
    expected_CPU = "Ryzen 3 3900x"
        self.assertEqual(self.test_server.CPU, expected_CPU)
    
    def test_motherboard(self)
    expected_motherboard = "X570 AORUS XTREME"
        self.assertEqual(self.test_server.motherboard, expected_motherboard)
    
    def test_RAM(self)
    expected_RAM = "4x32gb RAM"
        self.assertEqual(self.test_server.RAM, expected_RAM)
    
    def test_HDD(self)
    expected_HHD = "50 tb HDD"
        self.assertEqual(self.test_server.HDD, expected_HDD)
    
    def test_SSD(self)
    expected_SSD = "10tb SSD"
        self.assertEqual(self.test_server.SDD, expected_SDD)
    
    def test_GPU(self)
    expected_GPU = "SLI QUADRO 8000"
        self.assertEqual(self.test_server.GPU, expected_GPU)
    
    
    
