from django.shortcuts import render

def home(request):
    return render(request, "pawpals/home.html", context={})