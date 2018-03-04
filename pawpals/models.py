from django.db import models
from django.db.models.fields.related import ManyToManyField, OneToOneField
from django.template.defaultfilters import slugify, default


# default fields
phone_char_field = models.CharField(max_length = 20, unique = True)
standard_char_field = models.CharField(max_length = 200)
extended_char_field = models.CharField(max_length = 500)
datetime_field = models.DateTimeField()

class User(models.Model):
    username = models.CharField(max_length = 128, primary_key = True)
    fullname = standard_char_field # name and surname
    profile_picture = models.ImageField(upload_to="users_profile_images", blank="True")
    
    class Meta:
        abstract = True;

class StandardUser(User):
    phone_contact = phone_char_field

class ShelterManagerUser(User):
    shelter = OneToOneField(Shelter)

class Shelter(models.Model):
    # relationship
    
    name = models.CharField(max_length = 128, primary_key = True) # name and surname
    bio = extended_char_field
    webpage = models.URLField()
    profile_picture = models.ImageField(upload_to="shelters_profile_images", blank="True")
    phone_contact = phone_char_field
    availability_info = extended_char_field
    location = standard_char_field
    avg_rating = models.IntegerField()
    
    slug = models.SlugField(unique = True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    
class Dog(models.Model):
    # relationships
    shelter = models.ForeignKey(Shelter)
    
    name = standard_char_field
    id = models.AutoField(primary_key=True)
    bio = extended_char_field
    profile_picture = models.ImageField(upload_to="dogs_profile_images", blank="True")
    breed = standard_char_field

    difficulty = models.IntegerField()

    size = models.CharField(choices = (("S", "Small"),
                                       ("M", "Medium"),
                                       ("L", "Large")))
    gender = models.CharField(choices = (("M", "male"),
                                         ("F", "female")))
                                         
    is_puppy = models.BooleanField()
    is_childfriendly = models.BooleanField()
    
    slug = models.SlugField(unique = True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name + self.id)
        super(Category, self).save(*args, **kwargs)

class Review(models.Model):
    # relationshios
    user = ManyToManyField(StandardUser)
    dog = ManyToManyField(Dog)
    
    rating = models.IntegerField()
    comment = extended_char_field
    date = datetime_field

class Request(models.Model):
    # relationships
    user = ManyToManyField(StandardUser)
    shelter_manager = ManyToManyField(ShelterManagerUser)
    dog = ManyToManyField(Dog)
    
    date = datetime_field
    confirmation_status = models.CharField(choices = (("C", "Confirmed"),
                                                      ("D", "Denied"),
                                                      ("P", "Pending")))
    message = extended_char_field
    
#class Confirmation(models.Model):

