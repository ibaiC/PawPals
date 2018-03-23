import os

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.fields.related import ManyToManyField, OneToOneField
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.template.defaultfilters import slugify, default
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import redirect



import numpy as np


# default values
phone_len = 20
standard_char_len = 200
extended_char_len = 500
difficulty_validators = [MinValueValidator(0), MaxValueValidator(5)]

class User(AbstractUser):
    # username, first_name, last_name, email, password, groups, user_permissions, is_staff, is_active, is_superuser, last_login, date_joined
    is_manager = models.BooleanField("manager status", default=False)
    is_standard = models.BooleanField("standard user status", default=False)


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key = True, on_delete=models.CASCADE)

    def user_image_path(self, filename):
        return (os.path.join("user_profile_images", filename))

    profile_picture = models.ImageField(upload_to=user_image_path, blank="True")
    phone_contact = models.CharField(max_length = phone_len, unique = True, blank = "True", null = True)

    def __str__(self):
        return self.user.username

class Shelter(models.Model):
    # relationships
    manager = OneToOneField(User, blank = True, on_delete=models.CASCADE)

    name = models.CharField(max_length = 128, primary_key = True) # name and surname
    bio = models.CharField(max_length = extended_char_len)
    webpage = models.URLField(blank = "True")
    phone_contact = models.CharField(max_length = phone_len, unique = True)
    availability_info = models.CharField(max_length = extended_char_len)
    location = models.CharField(max_length = standard_char_len)
    avg_difficulty_rating = models.IntegerField(default = 5, validators = difficulty_validators)

    slug = models.SlugField(unique = True)


    def shelter_image_path(self, filename):
        return (os.path.join("shelters_profile_images", filename))

    profile_picture = models.ImageField(upload_to=shelter_image_path, blank="True")
     
    """def clean(self):
            if self.pk:
                if not(self.manager.is_manager):
                    raise ValidationError("User does not have permission to be manager.")
    """
       
    def save(self, *args, **kwargs):
        """

        :rtype: object
        """
        self.slug = slugify(self.name)

        sum = 0
        count = 0

        shelter_dogs = Dog.objects.all().filter(dog_shelter = self)

        for dog in shelter_dogs:
            reviews = Review.objects.all().filter(reviewed_dog = dog)
            sum += np.sum([review.difficulty_rating for review in reviews])
            count += len(reviews)

        if (count):
            self.avg_difficulty_rating = int(sum/count)
        else:
            self.avg_difficulty_rating = 0

        super(Shelter, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Dog(models.Model):
    # relationships
    dog_shelter = models.ForeignKey(Shelter, blank = True, on_delete=models.CASCADE)

    # ID (or pk) is implicitly made by Django
    # id = models.AutoField(primary_key=True)

    name = models.CharField(max_length = standard_char_len)
    bio = models.CharField(max_length = extended_char_len)
    breed = models.CharField(max_length = standard_char_len)

    difficulty = models.IntegerField(default = 0, validators = difficulty_validators)

    size = models.CharField(max_length = 1, choices = (("S", "Small"),
                                       ("M", "Medium"),
                                       ("L", "Large")))
    gender = models.CharField(max_length = 1, choices = (("M", "Male"),
                                                         ("F", "Female")))

    is_puppy = models.BooleanField(default = "False")
    is_childfriendly = models.BooleanField(default = "False")

    slug = models.SlugField(unique = True)

    completed_request_count = models.IntegerField(default=0)

    def dog_image_path(self, filename):
        return (os.path.join("dogs_profile_images", filename))

    profile_picture = models.ImageField(upload_to=dog_image_path, blank="True")


    def save(self, *args, **kwargs):
        
        reviews = Review.objects.all().filter(reviewed_dog = self)

        if reviews:
            avg_difficulty = 0

            for review in reviews:
                avg_difficulty += review.difficulty_rating

            avg_difficulty = avg_difficulty/len(reviews)
        else:
            avg_difficulty = 3;

        self.difficulty = avg_difficulty


        self.completed_request_count = Request.objects.all().filter(Q(requested_dog=self) & (Q(status="C") | Q(status="R"))).count()

        # if called upon object creation, save first, so pk is created and slug in not None
        if not(self.pk):
            super().save(*args, **kwargs)
        else:
            self.slug = slugify(self.name + "-" + str(self.pk))
            super(Dog,self).save(*args, **kwargs)


    def clean(self):

        if self.pk:
            same_name = Dog.objects.all().filter(name=self.name, dog_shelter = self.dog_shelter).count()
    
            if same_name > 1:
                raise ValidationError("Dog of this name is already in the shelter.")

    def __str__(self):
        return self.name

# Sets up slug upon creation. This workaround deserves cookies and praise.
@receiver(post_save, sender = Dog)
def update_slug(sender, instance, created, *args, **kwargs):
    if created:
        instance.slug = slugify(instance.name + "-" + str(instance.pk))
        instance.save()

class Request(models.Model):
    # relationships
    requesting_user = models.ForeignKey(User, related_name="requesting_user", on_delete=models.CASCADE)
    request_manager = models.ForeignKey(User, related_name="request_manager", blank = True, on_delete=models.CASCADE)

    requested_dog = models.ForeignKey(Dog, on_delete=models.CASCADE)

    date = models.DateTimeField(default = timezone.now())
    status = models.CharField(max_length = 1, choices = (("A", "Accepted"),
                                                      ("D", "Denied"),
                                                      ("P", "Pending"),
                                                      ("C", "Completed"),
                                                      ("R", "Reviewed")))
    message = models.CharField(max_length = extended_char_len, blank = True)

    def __str__(self):
        dog_name = str(self.requested_dog)
        user_name = str(self.requesting_user)
        manger_name = str(self.request_manager)

        return (dog_name  + " - by " + user_name + " (" + self.date.strftime("%B %d, %Y") + ")")

    def save(self, *args, **kwargs):

        if (Review.objects.all().filter(request = self)) and not(self.status.__eq__("R")):
            self.status = "R"

        super(Request, self).save(*args, **kwargs)
        self.requested_dog.save()

    def clean(self):
        
        if self.pk:
            managed_shelter = Shelter.objects.all().filter(manager = self.request_manager)
            managed_dogs = Dog.objects.all().filter(dog_shelter = managed_shelter)
    
            if self.requested_dog not in managed_dogs:
                raise ValidationError("Dog does not belong to shelter managed by given shelter manager.")
    
            if not(self.request_manager.is_manager):
                raise ValidationError("User does not have permission to be manager.")
    
            if (self.requesting_user.is_manager):
                raise ValidationError("User is a manager, cannot add it as requesting user.")

class Review(models.Model):
    # relationships
    request = models.OneToOneField(Request, on_delete=models.CASCADE)

    reviewing_user = models.ForeignKey(User, on_delete=models.CASCADE) 
    reviewed_dog = models.ForeignKey(Dog, on_delete=models.CASCADE) 

    difficulty_rating = models.IntegerField(default = 3, validators = difficulty_validators, blank=True)
    comment = models.CharField(max_length = extended_char_len)
    date = models.DateTimeField(default = timezone.now())

    def save(self, *args, **kwargs):

        self.reviewing_user = self.request.requesting_user
        self.reviewed_dog = self.request.requested_dog

        # update dog upon creating/changing review
        super(Review, self).save(*args, **kwargs)

        # change request to "Reviewed"
        self.request.status = "R"
        self.request.save()

        # self.reviewed_dog.
        self.reviewed_dog.save()
        self.reviewed_dog.dog_shelter.save()

    def __str__(self):
        dog_name = str(self.reviewed_dog)
        user_name = str(self.reviewing_user)

        return (dog_name  + " (" + self.date.strftime("%B %d, %Y") + ")")
