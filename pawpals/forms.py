from django import forms
from django.contrib.auth.models import User
from pawpals.models import *


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture','phone_contact')

class ReviewForm(forms.ModelForm):
        
    class Meta:
        model = Review
        fields = ('difficulty_rating', 'comment')


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('message',)

class RequestStatusForm(forms.ModelForm):

    class Meta:
        model = Request
        fields = ('status',)

class UserEditingForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'phone_contact')

class UserCoreEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)


class ShelterEditingForm(forms.ModelForm):
    manager = forms.CharField()

    class Meta:
        model = Shelter
        fields = ('name', 'bio', 'webpage', 'phone_contact', 'availability_info', 'location', 'profile_picture')

class DogEditingForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = ('name', 'bio', 'breed', 'size', 'gender', 'is_puppy', 'is_childfriendly', 'profile_picture')
