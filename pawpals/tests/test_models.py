from django.test import TestCase

from pawpals.models import *


#Tests most important attributes of Shelter entity
class ShelterModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Shelter.objects.create(name='Test Shelter', location='Glasgow', webpage= 'http://www.shelter.com', manager_id=1)


    def test_name_label(self):
        shelter=Shelter.objects.get(manager_id=1)
        field_label = shelter._meta.get_field('name').verbose_name
        self.assertTrue(field_label, 'name')

    def test_location_label(self):
        shelter=Shelter.objects.get(manager_id=1)
        field_label = shelter._meta.get_field('location').verbose_name
        self.assertTrue(field_label, 'location')

    def test_webpage_label(self):
        shelter=Shelter.objects.get(manager_id=1)
        field_label = shelter._meta.get_field('webpage').verbose_name
        self.assertTrue(field_label, 'webpage')

#Tests most important attributes of User model
class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        User.objects.create(username='foo', password='helloWorld', is_standard = True)


    def test_username_label(self):
        user=User.objects.get(username='foo')
        field_label = User._meta.get_field('username').verbose_name
        self.assertTrue(field_label, 'username')

    def test_password_label(self):
        user=User.objects.get(username='foo')
        field_label = User._meta.get_field('password').verbose_name
        self.assertTrue(field_label, 'password')

    #Test user type attribute
    def test_userType_label(self):
        user=User.objects.get(username='foo')
        field_label = User._meta.get_field('is_standard')   .verbose_name
        self.assertTrue(field_label,'is_standard')

#Tests most important attributes of Dog entity
class DogModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        shelter=Shelter.objects.create(name = 'goodHome', manager_id=2)
        shelter_name = shelter.name
        Dog.objects.create(dog_shelter=shelter, name='goodboi', difficulty = 3)


    #test dog_shelter attribute
    def test_dogShelter_label(self):
        user=Dog.objects.get(dog_shelter='goodHome')
        field_label = Dog._meta.get_field('dog_shelter').verbose_name
        self.assertTrue(field_label, 'dog_shelter')

    #test dog name attribute
    def test_name_label(self):
        user=Dog.objects.get(name='goodboi')
        field_label = Dog._meta.get_field('name').verbose_name
        self.assertTrue(field_label, 'name')

    #test dog difficulty attribute
    def test_difficulty_label(self):
        user=Dog.objects.get(difficulty='3')
        field_label = Dog._meta.get_field('difficulty').verbose_name
        self.assertTrue(field_label, 'difficulty')
