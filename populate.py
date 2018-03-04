import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pawpals.settings")

import django
django.setup()

from rango.models import *


def populate():
    
    dog_trust_dogs = [
        {"title" : "Bottl",
         "url" : "http://bottlepy.org/docs/dev/",
         "views" : 77},
        {"title" : "Flask",
         "url" : "http://flask.pocoo.org/",
         "views" : 88}
        ]
    
    shelters = {"Dog Trust" : {"dogs": dog_trust_dogs, 
                               "name": "Dogs Trust Glasgow",
                               "bio": "315 Hamilton Road Uddingston Glasgow G71 7SL",
                               "webpage": "https://www.dogstrust.org.uk/our-centres/glasgow/",
                               "phone_contact": "+44 123456789",
                               "availability_info": "Everyday 8am-3pm",
                               "location": "Glasgow",
                               "avg_rating": 4
                               }}
     availability_info, location, avg_rating):


    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data["views"], cat_data["likes"])
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"], p["views"])
    
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} -{1}".format(str(c), str(p)))
    

def add_user(is_manager, username, fullname, profile_picture = None, phone_contact):
    
    if is_manager:
        user = ShelterManagerUser.objects.get_or_create(username=username)[0]
    else:
        user = StandardUser.objects.get_or_create(username=username)[0]

    user.fullname = fullname
    user.phone_contact = phone_contact
    
    # in case we wanted to test and populate with pictures
    if profile_picture:
        user.profile_picture = profile_picture
    
    user.save()
    return user

def add_shelter(manager, name, bio, webpage, profile_picture, phone_contact, availability_info, location, avg_rating):
    sh = Shelter.objects.get_or_create(manager=manager, name=name)[0]
    sh.bio = bio
    sh.webpage = webbage
    sh.profile_picture = profile_picture
    sh.phone_contact = phone_contact
    sh.availability_info = availability_info
    sh.location = location
    sh.avg_rating = avg_rating
    sh.save()
    return sh

def add_dog(shelter, name, bio, profile_picture, breed, difficulty, size, gender, is_puppy=False, is_childfriendly=False):
    
    d = Dog.objects.get_or_create(shelter = shelter, name=name)[0]
    
    d.bio = bio 
    d.profile_picture = profile_picture  
    d.breed = breed 

    d.difficulty = difficulty

    d.size = size
    d.gender = gender        
    d.is_puppy = is_puppy
    d.is_childfriendly = is_childfriendly

    d.save()
    return d

def add_review(user, dog, date, rating, comment):
    
    rev = Review.objects.get_or_create(user = user, dog = dog, date = date)
    
    rev.rating = rating
    rev.comment = comment
    
    rev.save()
    
    return rev
    
def add_request(user, shelter_manager, dog, date, confirmation_status, message):
    
    req = Request.objects.get_or_create(user = user, shelter_manager = shelter_manager, dog = dog)[0]
    
    req.date = date
    
    req.confirmation_status = confirmation_status 
    req.message = message  
    
    rew.save()
    
    return req

if __name__ == "__main__":
    print("Starting population script...")
    populate()




