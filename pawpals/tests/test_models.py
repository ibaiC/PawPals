from django.test import TestCase

from pawpals.models import *



class ShelterModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Shelter.objects.create(name='Test Shelter', location='Glasgow', manager_id=1)

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_name_label(self):
        shelter=Shelter.objects.get(manager_id=1)
        field_label = shelter._meta.get_field('name').verbose_name
        self.assertTrue(field_label, 'name')

    def test_location_label(self):
        shelter=Shelter.objects.get(manager_id=1)
        field_label = shelter._meta.get_field('location').verbose_name
        self.assertTrue(field_label, 'location')
