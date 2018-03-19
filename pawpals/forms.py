from django import forms
from django.contrib.auth.models import User
from pawpals.models import AbstractUser as UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture','phone_contact')

# class ReviewForm(forms.ModelForm):
#     difficulty = forms.IntegerField()
#     userComment = forms.CharField()
#     reviewDate = forms.DateTimeField()
#
#     class Meta:
#         model = Review
#         fields = ('difficulty', 'userComment', 'reviewDate')
#
#
# class RequestForm(forms.ModelForm):
#     #Need to link dogName to ID
#     #is dogName + shelterName enough ?
#     dogShelter = forms.CharField()
#     dogName = forms.CharField()
#     timeslot = forms.DateTimeField()
