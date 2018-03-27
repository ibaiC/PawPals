from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from pawpals.models import *
from datetime import datetime
from pawpals.forms import *
from pawpals.decorators import *
from .filters import DogFilter
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.forms import modelformset_factory

# Custom decorators:
# @standardUser_required : requires user to be a standard user in order to use the view
# @manager_required : requires user to be a shelter manager to use the view


# Home view, shows dogs who haven't had much attention, updates user visits
def home(request):
    dogs_list = Dog.objects.order_by('completed_request_count')[:6]
    context_dict = {'dogs': dogs_list}

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    response = render(request, "pawpals/home.html", context_dict)
    return response

#Shows all shelters
def shelters(request):
    shelters_list = Shelter.objects.all()
    context_dict = {'shelters': shelters_list}
    response = render(request, "pawpals/shelters.html", context_dict)
    return response

def about(request):
    reponse = render(request, 'pawpals/about.html')
    return reponse

@login_required
def edit(request):

    context_dict = {}
    user_form = UserCoreEditForm(instance = request.user)
    user_profile_form = UserEditingForm(instance = UserProfile.objects.get(user = request.user))

    context_dict["user_form"] = user_form
    context_dict["user_profile_form"] = user_profile_form

    if request.user.is_manager:

        shelter = Shelter.objects.get(manager = request.user)
        dogs = Dog.objects.all().filter(dog_shelter = shelter)
        context_dict["dogs"] = dogs

        shelter_form = ShelterEditingForm(instance = shelter)
        context_dict["shelter_form"] = shelter_form

        DogFormSet = modelformset_factory(Dog, fields=('name', 'bio', 'breed', 'size','gender', 'is_puppy', 'is_childfriendly',
                   'profile_picture'), extra=0)
        dog_formset = DogFormSet(queryset=dogs)
        context_dict["dog_formset"] = dog_formset

        empty_dog_form = DogEditingForm()
        context_dict["empty_dog_form"] = empty_dog_form


    if request.method == "POST":

        user_form = UserCoreEditForm(request.POST, instance = request.user)
        user_profile_form = UserEditingForm(request.POST, instance = UserProfile.objects.get(user = request.user))

        if request.user.is_manager:
            shelter_form = ShelterEditingForm(request.POST, instance = shelter)

            dog_formset = DogFormSet(request.POST, queryset=dogs)
            empty_dog_form = DogEditingForm(request.POST)

            if empty_dog_form.is_valid():
                dog = empty_dog_form.save(commit = False)
                dog.dog_shelter = shelter
                dog.save()

            for dog_form in dog_formset:
                if dog_form.is_valid():
                    dog = dog_form.save(commit = False)
                    dog.dog_shelter = shelter
                    dog.save()
                else:
                    print(dog_form.errors)

            if shelter_form.is_valid():
                shelter = shelter_form.save(commit = False)
                shelter.save()
            else:
                print(shelter_form.errors)

        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save()
            user.save()
            profile = user_profile_form.save(commit=False)

            profile.user = user

            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']

            profile.save()

            return redirect("edit")
        else:

            print(user_form.errors)
            print(user_profile_form.errors)

    return render(request, 'pawpals/edit.html', context_dict)


# This method of deleting users is better than outright deleting the user instance
# from the database as if the username is in use as a foreign key, deleting a user instance
# could cause database issues.
@login_required
def deactivate_user(request):
    context_dict = {}

    #grab current user object and deactivate it - without deleting the object
    user = request.user
    user.is_active = False
    user.save()
    context_dict['msg'] = 'Profile successfully disabled.'

    #logout and deactivate user user
    logout(request)
    return redirect('deactivate_user')
    #return render(request, 'pawpals/edit.html', context_dict)

#Allows standard user to add a review of a dog
@login_required
def add_review(request, request_pk):

    request_object = Request.objects.get(pk = request_pk)

    #get an instance of the review form
    form = ReviewForm()

    context_dict = {}


    if request.method == "POST":

        #fill form with request data once it has been filled
        form = ReviewForm(request.POST)

        #validate reviw and save it to database
        if form.is_valid():
            review = form.save(commit = False)

            review.request = request_object

            review.save()

            return redirect("requests")
        else:
            print (form.errors)

    context_dict["form"] = form
    context_dict["review"] = None
    context_dict["dog"] = request_object.requested_dog

    return render (request, 'pawpals/review.html', context_dict)


#Allows user to edit one of their own dog reviews
@login_required
def edit_review(request, request_pk):
    request_object = Request.objects.get(pk = request_pk)

    existing_review = Review.objects.get(request = request_object)

    form = ReviewForm(instance = existing_review)
    context_dict = {}

    if request.method == 'POST':

        form = ReviewForm(instance = existing_review, data = request.POST)

        if form.is_valid():
            review = form.save(commit = False)
            review.save()
            return redirect("requests")
        else:
            print (form.errors)

    context_dict["form"] = form
    context_dict["review"] = Review.objects.get(request = request_object)
    context_dict["dog"] = request_object.requested_dog

    return render (request, 'pawpals/review.html', context_dict)

#Passes review to its form through POST request and saves it to database
@login_required
@standardUser_required
def review(request, dog_slug):
    dog = Dog.objects.get(slug=dog_slug)
    context_dict['dog'] = dog
    review_form= ReviewForm(data= request.POST)
    review = review_form.save(commit=False)
    #from forms
    #review.reviewing_user = get current user
    #review.request = get current request
    review.reviewed_dog = dog
    review.save()
    return render (request, 'pawpals/dog.html', context_dict)

# Shows the requests made for all requested dogs
@login_required
def show_requests(request):

    context_dict = {}
    if request.user.is_manager:
        requests_list = Request.objects.all().filter(request_manager = request.user).order_by('-date')
        if request.method == 'POST':
            instance = get_object_or_404(Request, pk = request.POST.get("request_object"))
            form = RequestStatusForm(request.POST or None, instance=instance)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('requests'))

        else:
            form = RequestStatusForm()

    else:
        requests_list = Request.objects.all().filter(requesting_user = request.user).order_by('-date')
        form = RequestStatusForm()
    print(form)
    context_dict['form'] = form
    context_dict['requests'] = requests_list

    return render(request, 'pawpals/requests.html', context_dict)


@standardUser_required
def request(request, dog_slug):

    context_dict = {}

    dog = Dog.objects.get(slug=dog_slug)

    context_dict['dog'] = dog
    context_dict['user'] = request.user

    form = RequestForm()

    if request.method == "POST":

        form = RequestForm(request.POST)

        if form.is_valid():
            request_obj = form.save(commit = False)

            request_obj.requesting_user = request.user
            request_obj.request_manager = dog.dog_shelter.manager

            request_obj.requested_dog = dog
            request_obj.status = "P"

            request_obj.save()

            return redirect("requests")
        else:
            print (form.errors)

    return render(request, 'pawpals/request.html', context_dict)


def show_shelter(request, shelter_slug):
    context_dict = {}
    try:
        shelter = Shelter.objects.get(slug=shelter_slug)
        dog_list = Dog.objects.all().filter(dog_shelter = shelter)
        context_dict['shelter'] = shelter
        context_dict['dog'] = dog_list

    except Shelter.DoesNotExist:
        context_dict = {}

    return render(request, 'pawpals/shelter.html', context_dict)

def show_dog(request, dog_slug):
    context_dict = {}

    try:
        dog = Dog.objects.get(slug=dog_slug)
        context_dict['dog'] = dog

        reviews = Review.objects.all().filter(reviewed_dog = dog)
        context_dict["reviews"] = reviews

    except Dog.DoesNotExist:
        context_dict = {}

    return render(request, 'pawpals/dog.html', context_dict)

def dog_search(request):
    dog_list = Dog.objects.all()
    dog_filter = DogFilter(request.GET, queryset = dog_list)
    return render(request, "pawpals/dogSearch.html", {"filter" : dog_filter})

def show_reviews(request):
    dog_slug = request.GET.get("dog_slug", None)
    dog = Dog.objects.get(slug = dog_slug)

    data = {
        "reviews": []
        }

    for review in Review.objects.all().filter(reviewed_dog = dog):
        user_profile = UserProfile.objects.get(user = review.reviewing_user)
        new_review = {"username" : review.reviewing_user.username,
                      "rating" : review.difficulty_rating,
                      "comment" : review.comment,
                      "date" : review.date,
                      "profile_picture" : user_profile.profile_picture.path
                      }
        data["reviews"].append(new_review)

    return JsonResponse(data)

def professional(request):
    shelter_form = ShelterEditingForm()
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        shelter_form = ShelterEditingForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.is_manager = True
            user.save()


            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']

            profile.save()

            if shelter_form.is_valid():
                shelter = shelter_form.save(commit=False)
                shelter.manager = user
                shelter.save()
            else:
                print(shelter_form.errors)

            registered = True

            return redirect("login")

        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        shelter_form = ShelterEditingForm()

    return render(request, 'pawpals/professional.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered,
                   'shelter_form': shelter_form,
                   })
def personal(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.is_standard=True
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_picture' in request.FILES:
                profile_picture = request.FILES['profile_picture']

            profile.save()
            registered = True
            return redirect("login")
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'pawpals/personal.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered,
                   })

def register(request):

    return render(request,'pawpals/register.html')

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("Your PawPals account is disabled.")
        else:
            context_dict = {'error': 'The username or password you have entered is invalid'}
            return render(request, 'pawpals/login.html', context_dict)
    else:
        return render(request, 'pawpals/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def visitor_cookie_handler(request):

    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request,'last_visit',
                                               str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        #Update the last visit cookie after updating the count
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    # Update/set the visits cookie
    request.session['visits'] = visits

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val
