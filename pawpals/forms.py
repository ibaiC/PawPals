from django import forms
from django.contrib.auth.models import User
from pawpals.models import AbstractUser as UserProfile
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
    difficulty = forms.IntegerField()
    userComment = forms.CharField()

    class Meta:
        model = Review
        fields = ('difficulty', 'userComment')


class RequestForm(forms.ModelForm):
    requestMessage = forms.CharField(max_length = extended_char_len, blank = False)

    class Meta:
        model = RequestForm
        fields = ('requestMessage')

## TODO: edit user, edit shelter, edit dog
