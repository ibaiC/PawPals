from django import forms
from django.contrib.auth.models import User
from pawpals.models import *

# Using Django's base User model
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture','phone_contact')

# All forms from here inherit the fields from the model specified in class Meta.
class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('difficulty_rating', 'comment')


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('message',)

class RequestStatusForm(forms.ModelForm):

    CHOICES =  (("", "-----"),
                ("A", "Accepted"),
                ("D", "Denied"),
                ("C", "Completed"))

    status = forms.ChoiceField(choices = CHOICES)

    class Meta:
        model = Request
        fields = ('status',)

    # def is_valid(self):
    #     # Basic principle is to see what the request status is now and not allow the status submitted to form to be x
    #     # steps: get current status, then get submitted status,
    #     # then check return true if change is admissible or false if not admissibke
    #     currentRequest = Request.objects.get(requested_dog=???)
    #     requestStatus = currentRequest.status
    #
    #     if requestStatus == ...... :
    #         #change is ok - return True
    #     else:
    #         return False

class UserEditingForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'phone_contact')

class UserCoreEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)


class ShelterEditingForm(forms.ModelForm):
    class Meta:
        model = Shelter
        fields = ('name', 'bio', 'webpage',
                  'phone_contact',
                  'availability_info',
                  'location')

class DogEditingForm(forms.ModelForm):

    class Meta:
        model = Dog
        fields = ('name', 'bio', 'breed', 'size',
                   'gender', 'is_puppy',
                   'is_childfriendly',
                   'profile_picture')
