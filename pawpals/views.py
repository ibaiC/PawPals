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
    if request.method == 'POST':
        form = UserEditingForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('home') ) #Goes to home after valid form submitted
    else:
        form = UserEditingForm()    #provide a blank form if request is GET type
    return render(request, 'pawpals/edit.html', {'form': form})

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
        requests_list = Request.objects.all().filter(requesting_user = request.user)
        form = RequestStatusForm()

    context_dict['form'] = form
    context_dict['requests'] = requests_list

    return render(request, 'pawpals/requests.html', context_dict)

@login_required
<<<<<<< HEAD
def request(request, dog_slug):
=======
@standardUser_required
def request(request):
>>>>>>> b8b1ac2196f5014a5e4c7884e2c2bc6b2139d5f1
    #user =
    context_dict={}
    dog = Dog.objects.get(slug=dog_slug)
    context_dict['dog'] = dog
<<<<<<< HEAD
    context_dict['user'] = request.user
    #forms
    request_form= RequestForm(data= request.POST)
    request_object = request_form.save(commit=False)
    request_object.requesting_user= request.user
    request_object.status = "P"
=======
    context_dict['user'] = User
    #forms
    request_form= RequestForm(data= request.POST)
    request = request_form.save(commit=False)
    request.requesting_user= User
    request.status = P
>>>>>>> b8b1ac2196f5014a5e4c7884e2c2bc6b2139d5f1

    shelter = dog.dog_shelter
    shelter_manager = shelter.manager
    request.request_manager = shelter_manager

    return render(request, 'pawpals/request.html', context_dict)


def show_shelter(request, shelter_slug):
    shelters_list = Shelter.objects.order_by('-avg_difficulty_rating')[:5]
    context_dict = {'shelters': shelters_list}
    try:
        shelter = Shelter.objects.get(slug=shelter_slug)
        dog_list = Dog.objects.all()
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
            return HttpResponse("Invalid login details supplied.")
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
