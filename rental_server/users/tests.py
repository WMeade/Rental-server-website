from django.test import TestCase
from .models import CustomUser

# Create your tests here.
class Test(TestCase):
    def setUp(self):
        self.test_user = CustomUser.objects.create(fname="mark",lname="leonard",dob='10-11-2001',address1="home",address2="home",address3="home")

    def tearDown(self):
        del self.test_user
    
    def test_value_fname(self):
        expected_fname = "mark"
        self.assertEqual(self.test_user.fname, expected_fname)
        
    def test_value_lname(self):
        expected_lname = "leonard"
        self.assertEqual(self.test_user.lname, expected_lname)
    
    def test_value_dob(self):
        expected_dob= '10-11-2001'
        self.assertEqual(self.test_user.dob, expected_dob)

    def test_value_address1(self):
        expected_address1 = "home"
        self.assertEqual(self.test_user.address1, expected_address1)
    
    def test_value_address2(self):
        expected_address2 = "home"
        self.assertEqual(self.test_user.address2, expected_address2)
    
    def test_value_address3(self):
        expected_address3 = "home"
        self.assertEqual(self.test_user.address3, expected_address3)
    
