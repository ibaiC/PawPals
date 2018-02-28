from django.conf.urls import url
from pawpals import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
]