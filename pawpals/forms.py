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

    previous_status = forms.CharField(widget=forms.HiddenInput)
    CHOICES =  (("", "-----"),
                ("A", "Accepted"),
                ("D", "Denied"),
                ("C", "Completed"))

    status = forms.ChoiceField(choices = CHOICES)

    class Meta:
        model = Request
        fields = ('status',)

    def clean(self):
        cleaned_data = super().clean()
        c_status = cleaned_data.get("status")
        p_status= cleaned_data.get("previous_status")
        
        # pending to accepted
        p_a = (p_status == "P") and (c_status == "A")
        # pending to denied
        p_d = (p_status == "P") and (c_status == "D")
        # accept to completed
        a_c = (p_status == "A") and (c_status == "C")

        if not(p_a) and not(p_d) and not(a_c):
            raise forms.ValidationError("Cannot change status backward.")

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
