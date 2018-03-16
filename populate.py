import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pawpals_project.settings")

import django
django.setup()

from django.utils import timezone
from pawpals.models import *


def populate():
    
    ### Dog Trust data ###
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
         "is_childfriendly" : True},
        {"name": "Lisa",
         "bio": "Fierce lady.",
         "profile_picture": None,
         "breed": "Puddle",
         "difficulty": 5,
         "size": "S",
         "gender": "F",
         "is_puppy": False,
         "is_childfriendly": False},
        {"name": "Atos",
         "bio": "Old but strong! Huge. Obedient. Protective.",
         "profile_picture": None,
         "breed": "Mongrel",
         "difficulty": 1,
         "size": "L",
         "gender": "M",
         "is_puppy": False,
         "is_childfriendly": True},
        {"name": "Sawa",
         "bio": "Very playful, active, guard dog.",
         "profile_picture": None,
         "breed": "Mongrel",
         "difficulty": 5,
         "size": "M",
         "gender": "F",
         "is_puppy": False,
         "is_childfriendly": False}
        ]
    
    dog_trust_manager = {"username" : "jsmith",
                        "fullname" : "John Smith",
                        "phone_contact" : "121212112",
                        "email" : "jsmith@mail.co.uk"
                        }

    ### Blue Cross For Pets data ###

    blue_cross_dogs = [
        {"name": "Jonathan",
         "bio": "Calm, loves running.",
         "profile_picture": None,
         "breed": "Husky",
         "difficulty": 2,
         "size": "L",
         "gender": "M",
         "is_puppy": False,
         "is_childfriendly": True},
        {"name": "Helix",
         "bio": "Loves purple balls",
         "profile_picture": None,
         "breed": "Shih-tzu",
         "difficulty": 3,
         "size": "S",
         "gender": "M",
         "is_puppy": False,
         "is_childfriendly": True},
        {"name": "Speed",
         "bio": "Loves cuddles and treats.",
         "profile_picture": None,
         "breed": "Pug",
         "difficulty": 4,
         "size": "M",
         "gender": "N",
         "is_puppy": False,
         "is_childfriendly": False},
        {"name": "Amino",
         "bio": "Has a long tongue",
         "profile_picture": None,
         "breed": "Shih-tzu",
         "difficulty": 4,
         "size": "S",
         "gender": "N",
         "is_puppy": False,
         "is_childfriendly": True},
    ]

    blue_cross_manager = {"username": "abrown",
                         "fullname": "Anna Brown",
                         "phone_contact": "1313131313",
                         "email": "abrown@mail.co.uk"
                         }

    ### Shelters ###

    shelters = {"Dog Trust" : {
                    "manager": dog_trust_manager,
                    "dogs": dog_trust_dogs,
                    "bio": "315 Hamilton Road Uddingston Glasgow G71 7SL",
                    "webpage": "https://www.dogstrust.org.uk/our-centres/glasgow/",
                    "phone_contact": "+44 123456789",
                    "availability_info": "Everyday 8am-3pm",
                    "location": "Glasgow",
                    "avg_rating": 4
                    },
                "Blue Cross For Pets" : {
                    "manager": blue_cross_manager,
                    "dogs": blue_cross_dogs,
                    "bio": "Rehoming for cats, dogs & rabbits Parklands,Thirsk,YO7 3SE",
                    "webpage": "https://www.bluecross.org.uk/yorkshire-thirsk-rehoming-centre",
                    "phone_contact": "+44 987654321",
                    "availability_info": "Tuesday - Saturday 8am-3pm",
                    "location": "Yorkshire",
                    "avg_rating": 3
                    }}
    
    ### Shelter, dog, manager creation ###

    for shelter, shelter_data in shelters.items():
        manager_data = shelter_data["manager"]
        sh_manager = add_user(is_manager=True,
                             username=manager_data["username"],
                             fullname=manager_data["fullname"],
                             email=manager_data["email"],
                             profile_picture=None,
                             phone_contact=manager_data["phone_contact"])
            
        sh = add_shelter(manager=sh_manager,
                         name=shelter,
                         bio=shelter_data["bio"],
                         webpage=shelter_data["webpage"],
                         phone_contact=shelter_data["phone_contact"],
                         availability_info=shelter_data["availability_info"],
                         location=shelter_data["location"],
                         avg_rating=shelter_data["avg_rating"])
        
        for dog in shelter_data["dogs"]:
            add_dog(shelter=sh,
                    name=dog["name"],
                    bio=dog["bio"],
                    breed=dog["breed"],
                    difficulty=dog["difficulty"],
                    size=dog["size"],
                    gender=dog["gender"],
                    is_puppy=dog["is_puppy"],
                    is_childfriendly=dog["is_childfriendly"])
    

    ### Users ###

    users = {"jojo2": {"fullname" : "Joseph Joestar",
                       "email" :"jojo2@gmail.com",
                       "phone_contact" : "+44 000000",
                       "reviews": {Dog.objects.all().get(id=1) : {"rating": 5,
                                                                    "comment": "Good doggo!",
                                                                    "date": "2018-02-01T13:20:30+03:00"
                                                                    },
                                   Dog.objects.all().get(id=2): {"rating": 1,
                                                                   "comment": "Bad doggo!",
                                                                   "date": "2018-02-11T13:20:30+03:00"
                                                                   }
                                   }
                       },
        "optiplex": {"fullname" : "Ann Dawn",
                     "email" : "optiplex@mail.com",
                     "phone_contact": "+44 11111111",
                     "reviews": {Dog.objects.all().get(id=3) : {"rating": 2,
                                                                "comment": "So fluffy!!",
                                                                "date": "2018-02-10T13:20:30+03:00"
                                                                },
                                 Dog.objects.all().get(id=4): {"rating": 3,
                                                               "comment": "Bites a bit, otherwise great",
                                                               "date": "2018-03-01T13:20:30+03:00"
                                                               }
                                 }
                     },
        "lilylith": {"fullname" : "Lily Lithium",
                     "email" : "llith@mail.com",
                     "phone_contact" : "+44 222222222",
                     "reviews": {Dog.objects.all().get(id=5) : {"rating": 5,
                                                                "comment": "Nice walk.",
                                                                "date": "2018-03-11T13:20:30+03:00"
                                                                },
                                 Dog.objects.all().get(id=6): {"rating": 5,
                                                               "comment": "Very playful, nice walk.",
                                                               "date": "2018-03-21T13:20:30+03:00"
                                                               }
                                 }
                     }
    }

     ### Users and review creation ###
    for user, user_data in users.items():
        u = add_user(is_manager=False,
                     username=user,
                     fullname=user_data["fullname"],
                     email=user_data["email"],
                     phone_contact=user_data["phone_contact"]
                     )

        for reviewed_dog, review_data in user_data["reviews"].items():
            add_review(user=u,
                       dog=reviewed_dog,
                       date=review_data["date"],
                       rating=review_data["rating"],
                       comment=review_data["comment"]
                       )



    ### Request creation ###
    requests = {0 : {"user" : StandardUser.objects.all().get(pk = "jojo2"), 
                     "shelter_manager" : ShelterManagerUser.objects.all().get(pk = "jsmith"), 
                     "dog" : Dog.objects.all().get(pk = 1), 
                     "date" : "2018-03-21T13:20:30+03:00",
                     "confirmation_status" : "P",
                     "message" : "Hi! Can I walk that doggie next week?"},
                1 : {"user" : StandardUser.objects.all().get(pk = "jojo2"), 
                     "shelter_manager" : ShelterManagerUser.objects.all().get(pk = "jsmith"), 
                     "dog" : Dog.objects.all().get(pk = 2), 
                     "date" : "2018-03-21T13:20:30+03:00",
                     "confirmation_status" : "A",
                     "message" : "Next Friday 11am?"},
                2 : {"user" : StandardUser.objects.all().get(pk = "lilylith"), 
                     "shelter_manager" : ShelterManagerUser.objects.all().get(pk = "jsmith"), 
                     "dog" : Dog.objects.all().get(pk = 3), 
                     "date" : "2018-03-21T13:20:30+03:00",
                     "confirmation_status" : "C",
                     "message" : "Usual?"},
                }
    
    for request_id, request in requests.items():
        add_request(user = request["user"], 
                    shelter_manager = request["shelter_manager"], 
                    dog = request["dog"], 
                    date = request["date"], 
                    confirmation_status = request["confirmation_status"], 
                    message = request["message"])


    ### Print confirmation ###
    
    # Print shelter, dogs and manager
    print("\n>>> Shelters and dogs")
    for sh in Shelter.objects.all():
        print(str(sh) + " managed by: " +str(sh.manager))
        for dog in Dog.objects.filter(dog_shelter=sh):
            print("\t - " + str(dog))
    print("\n>>> Users and comments")
    for user in StandardUser.objects.all():
        print(str(user) + "'s comments:")
        for review in Review.objects.filter(reviewing_user = user):
            print("\t - " + str(review))
    print("\n>>> Requests: ")    
    for request in Request.objects.all():
        print("\t - " + str(request))




def add_user(is_manager, username, fullname, email, phone_contact, profile_picture=None):
    
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


def add_shelter(manager, name, bio, webpage, phone_contact, availability_info, location, avg_rating, profile_picture=None):
    sh = Shelter.objects.get_or_create(manager=manager, name=name)[0]
    sh.bio = bio
    sh.webpage = webpage
    sh.profile_picture = profile_picture
    sh.phone_contact = phone_contact
    sh.availability_info = availability_info
    sh.location = location
    sh.avg_difficulty_rating = avg_rating
    sh.save()
    return sh


def add_dog(shelter, name, bio, breed, difficulty, size, gender, profile_picture=None, is_puppy=False, is_childfriendly=False):
    
    d = Dog.objects.get_or_create(dog_shelter=shelter, name=name)[0]
    
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
    
    # Note: since user can comment and review after each walk (request status "taken place")
    #       there can be many reviews by the same user on the same dog but with different DATE
    rev = Review.objects.get_or_create(reviewing_user=user, reviewed_dog=dog, date=date)[0]

    rev.difficulty_rating = rating
    rev.comment = comment
    
    rev.save()
    
    return rev

    
def add_request(user, shelter_manager, dog, date, confirmation_status, message):
    
    req = Request.objects.get_or_create(requesting_user=user, request_manager=shelter_manager, requested_dog=dog)[0]
    
    req.date = date
    
    req.status = confirmation_status 
    req.message = message  
    
    req.save()
    
    return req


if __name__ == "__main__":
    print("Starting population script...")
    populate()

