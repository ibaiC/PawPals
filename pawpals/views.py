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


#from pawpals.forms import CategoryForm, PageForm, UserForm, UserProfileForm


def home(request):
    dogs_list = Dog.objects.order_by('completed_request_count')[:6]
    context_dict = {'dogs': dogs_list}

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    response = render(request, "pawpals/home.html", context_dict)
    return response

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
        
        
    if request.method == "POST":
        
        user_form = UserCoreEditForm(request.POST, instance = request.user)
        user_profile_form = UserEditingForm(request.POST, instance = UserProfile.objects.get(user = request.user))

        if request.user.is_manager:
            shelter_form = ShelterEditingForm(request.POST, instance = shelter)

            if shelter_form.is_valid():
                
                shelter = form.save(commit = False)
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
            print (user_form.errors)
            print (user_profile_form.errors)
            
    
    return render(request, 'pawpals/edit.html', context_dict)


@login_required
def add_review(request, request_pk):
    request_object = Request.objects.get(pk = request_pk)
    
    form = ReviewForm()
    
    context_dict = {}

    if request.method == "POST":
        form = ReviewForm(request.POST)
        
        
        #review.request = request_object

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

@login_required
def show_requests(request):

    context_dict = {}
    if request.user.is_manager:
        requests_list = Request.objects.all().filter(request_manager = request.user)
        if request.method == 'POST':
            instance = get_object_or_404(Request, pk = request.POST.get("request_object"))
            form = RequestStatusForm(request.POST or None, instance=instance)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('requests'))

        else:
            form = RequestStatusForm()

    else:
        requests_list = Request.objects.all().filter(requesting_user = request.user).order_by('date')
        form = RequestStatusForm()

    context_dict['form'] = form
    context_dict['requests'] = requests_list

    return render(request, 'pawpals/requests.html', context_dict)



@standardUser_required
def request(request, dog_slug):

    #user =
    context_dict={}
    dog = Dog.objects.get(slug=dog_slug)
    context_dict['dog'] = dog

    context_dict['user'] = request.user
    #forms
    request_form= RequestForm(data= request.POST)
    request_object = request_form.save(commit=False)
    request_object.requesting_user= request.user
    request_object.status = "P"

    shelter = dog.dog_shelter
    shelter_manager = shelter.manager
    request_object.request_manager = shelter_manager

    request_object.save()

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


def register(request):
    registered = False

    if request.method == 'POST':
        user_form= UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,'pawpals/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})

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
