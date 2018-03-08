from django.db import models
from django.db.models.fields.related import ManyToManyField, OneToOneField
from django.template.defaultfilters import slugify, default
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


# default values
phone_len = 20
standard_char_len = 200
extended_char_len = 500
difficulty_validators = [MinValueValidator(0), MaxValueValidator(5)]

class User(models.Model):
    username = models.CharField(max_length = 128, primary_key = True)
    fullname = models.CharField(max_length = standard_char_len) # name and surname
    email = models.EmailField(unique = True)
    profile_picture = models.ImageField(upload_to="users_profile_images", blank="True")
    phone_contact = models.CharField(max_length = phone_len, unique = True, blank = "True")

    class Meta:
        abstract = True;

    def __str__(self):
        return self.fullname
    
class StandardUser(User):
    pass

class ShelterManagerUser(User):
    pass

class Shelter(models.Model):
    # relationships
    manager = OneToOneField(ShelterManagerUser)

    name = models.CharField(max_length = 128, primary_key = True) # name and surname
    bio = models.CharField(max_length = extended_char_len)
    webpage = models.URLField(blank = "True")
    profile_picture = models.ImageField(upload_to="shelters_profile_images", blank="True")
    phone_contact = models.CharField(max_length = phone_len, unique = True)
    availability_info = models.CharField(max_length = extended_char_len)
    location = models.CharField(max_length = standard_char_len)
    avg_difficulty_rating = models.IntegerField(default = 5, validators = difficulty_validators)
    
    slug = models.SlugField(unique = True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        
###        # Get average
        
        #shelter_dogs = Dog.objects().all().filter(dog_shelter = self)
        #reviews = Review.objects.all().filter()
        
        super(Shelter, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Dog(models.Model):
    # relationships
    dog_shelter = models.ForeignKey(Shelter)
    
    name = models.CharField(max_length = standard_char_len)
    id = models.AutoField(primary_key=True)
    bio = models.CharField(max_length = extended_char_len)
    profile_picture = models.ImageField(upload_to="dogs_profile_images", blank="True")
    breed = models.CharField(max_length = standard_char_len)
    
    difficulty = models.IntegerField(default = 0, validators = difficulty_validators)

    size = models.CharField(max_length = 1, choices = (("S", "Small"),
                                       ("M", "Medium"),
                                       ("L", "Large")))
    gender = models.CharField(max_length = 1, choices = (("M", "Male"),
                                                         ("F", "Female"),
                                                         ("N", "Neutered")))
                                         
    is_puppy = models.BooleanField(default = "False")
    is_childfriendly = models.BooleanField(default = "False")
    
    slug = models.SlugField(unique = True)

    def save(self, *args, **kwargs):
        
        reviews = Review.objects.all().filter(reviewed_dog = self)
    
        
        if reviews:
            avg_difficulty = 0
            
            for review in reviews:
                avg_difficulty += review.difficulty_rating
                print(avg_difficulty)
            
            avg_difficulty = avg_difficulty/len(reviews)
        else:
            avg_difficulty = 3;
        
        self.difficulty = avg_difficulty
        
        self.slug = slugify(self.name + "-" + str(self.id))
        super(Dog, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.name

class Review(models.Model):
    # relationships
    reviewing_user = models.ForeignKey(StandardUser)
    reviewed_dog = models.ForeignKey(Dog)
    
### 
    difficulty_rating = models.IntegerField(default = 3, validators = difficulty_validators)
    comment = models.CharField(max_length = extended_char_len)
    date = models.DateTimeField()

    def clean(self):
        # update dog upon creating/changing review  
        self.reviewed_dog.save()

    def __str__(self):
        dog_name = str(self.reviewed_dog)
        user_name = str(self.reviewing_user)

        return (dog_name  + " (" + self.date.strftime("%B %d, %Y") + ")")


class Request(models.Model):
    # relationships
    requesting_user = models.ForeignKey(StandardUser)
    request_manager = models.ForeignKey(ShelterManagerUser) 
    requested_dog = models.ForeignKey(Dog)
    
    date = models.DateTimeField(default = timezone.now())
    status = models.CharField(max_length = 1, choices = (("A", "Accepted"),
                                                      ("D", "Denied"),
                                                      ("P", "Pending"),
                                                      ("C", "Completed")))
    message = models.CharField(max_length = extended_char_len)
    
    def __str__(self):
        dog_name = str(self.requested_dog)
        user_name = str(self.requesting_user)
        manger_name = str(self.request_manager)

        return (dog_name  + " - by " + user_name + " (" + self.date.strftime("%B %d, %Y") + ")")    

    def clean(self):
        
        managed_shelter = Shelter.objects.all().filter(manager = self.request_manager)
        managed_dogs = Dog.objects.all().filter(dog_shelter = managed_shelter)
        if self.requested_dog not in managed_dogs:
            raise ValidationError("Dog does not belong to shelter managed by given shelter manager.")

