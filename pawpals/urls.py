from django.conf.urls import url
from pawpals import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about', views.about, name='about'),
    url(r'^(?P<dog_slug>[\w\-]+)/$', views.show_dog, name='show_dog'),
    url(r'^(?P<shelter_slug>[\w\-]+)/$', views.show_shelter, name='show_shelter'),

]