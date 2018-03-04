import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pawpals_project.settings")

import django
django.setup()

from pawpals.models import *


def populate():
    
    ### Dog trust ###
    dog_trust_dogs = [
        {"name" : "Leo",
         "bio" : "Very good boy.",
         "profile_picture" : None,
         "breed" : "Bulldog",
         "difficulty" : 3,
         "size" : "M",
         "gender" : "M",
         "is_puppy" : True,
         "is_childfriendly" : True},
        {"name" : "Difen",
         "bio" : "Extremely good boy.",
         "profile_picture" : None,
         "breed" : "Mongrel",
         "difficulty" : 1,
         "size" : "L",
         "gender" : "M",
         "is_puppy" : False,
         "is_childfriendly" : True}
        ]
    
    dog_trust_manager = {"username" : "jsmith",
                        "fullname" : "John Smith",
                        "phone_contact" : "121212112",
                        "email" : "jsmith@mail.co.uk"
                        }
    
    shelters = {"Dog Trust" : {"manager": dog_trust_manager,
                               "dogs": dog_trust_dogs, 
                               "bio": "315 Hamilton Road Uddingston Glasgow G71 7SL",
                               "webpage": "https://www.dogstrust.org.uk/our-centres/glasgow/",
                               "phone_contact": "+44 123456789",
                               "availability_info": "Everyday 8am-3pm",
                               "location": "Glasgow",
                               "avg_rating": 4
                               }}
    


    for shelter, shelter_data in shelters.items():
        manager_data = shelter_data["manager"]
        sh_manager = add_user(is_manager = True, 
                             username = manager_data["username"], 
                             fullname = manager_data["fullname"], 
                             email = manager_data["email"], 
                             profile_picture = None, 
                             phone_contact = manager_data["phone_contact"])
            
        sh = add_shelter(manager = sh_manager, 
                         name = shelter, 
                         bio = shelter_data["bio"], 
                         webpage = shelter_data["webpage"], 
                         phone_contact = shelter_data["phone_contact"], 
                         availability_info = shelter_data["availability_info"], 
                         location = shelter_data["location"], 
                         avg_rating = shelter_data["avg_rating"])
        
        for dog in shelter_data["dogs"]:
            add_dog(shelter = sh, 
                    name = dog["name"], 
                    bio = dog["bio"], 
                    breed = dog["breed"], 
                    difficulty = dog["difficulty"], 
                    size = dog["size"], 
                    gender = dog["gender"], 
                    is_puppy = dog["is_puppy"], 
                    is_childfriendly = dog["is_childfriendly"])
    
    for sh in Shelter.objects.all():
        for dog in Dog.objects.filter(dog_shelter = sh):
            print("- {0} -{1}".format(str(sh), str(dog)))
    

def add_user(is_manager, username, fullname, email, phone_contact, profile_picture = None):
    
    if is_manager:
        user = ShelterManagerUser.objects.get_or_create(username=username)[0]
    else:
        user = StandardUser.objects.get_or_create(username=username)[0]

    user.fullname = fullname
    user.email = email
    user.phone_contact = phone_contact
    user.profile_picture = profile_picture
    
    user.save()
    return user

def add_shelter(manager, name, bio, webpage, phone_contact, availability_info, location, avg_rating, profile_picture = None):
    sh = Shelter.objects.get_or_create(manager=manager, name=name)[0]
    sh.bio = bio
    sh.webpage = webpage
    sh.profile_picture = profile_picture
    sh.phone_contact = phone_contact
    sh.availability_info = availability_info
    sh.location = location
    sh.avg_rating = avg_rating
    sh.save()
    return sh

def add_dog(shelter, name, bio, breed, difficulty, size, gender, profile_picture = None, is_puppy=False, is_childfriendly=False):
    
    d = Dog.objects.get_or_create(dog_shelter = shelter, name=name)[0]
    
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




