from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from pawpals.models import *
from datetime import datetime
from pawpals.forms import UserForm, UserProfileForm


#from pawpals.forms import CategoryForm, PageForm, UserForm, UserProfileForm

def base(request):
    shelters_list = Shelter.objects.order_by('-avg_difficulty_rating')[:5]
    context_dict = {'shelters': shelters_list}
    response = render(request, "pawpals/home.html", context_dict)
    return response

def home(request):
    dogs_list = Dog.objects.order_by('-difficulty')[:5]
    context_dict = {'dogs': dogs_list}

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    response = render(request, "pawpals/home.html", context_dict)
    return response

def about(request):
    reponse = render(request, 'pawpals/about.html')
    return reponse

def edit(request):
    response = render (request, 'pawpals/edit.html')
    AbstractUser= AbstractUser.objects.get(slug=AbstractUser_slug)
    #give information about user
    return response

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

    try:
        dog = Dog.objects.get(slug=dog_slug)
        context_dict['dog'] = dog


    except Dog.DoesNotExist:
        context_dict = {}

    return render(request, 'pawpals/dog.html', context_dict)

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
        return render(request, 'pawpals/login.html', {'shelters': shelters_list})

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
