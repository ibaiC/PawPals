from django.conf.urls import url
from pawpals import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.base, name='base'),
    url(r'^$', views.home, name='home'),
    url(r'^about', views.about, name='about'),
    url(r'^login/$',auth_views.LoginView.as_view(template_name='pawpals/login.html'),name='login'),
    url(r'^register/$',views.register,name='register'),
    url(r'^(?P<shelter_slug>[\w\-]+)/$', views.show_shelter, name='show_shelter'),
    url(r'^(?P<dog_slug>[\w\-]+)/$', views.show_dog, name='show_dog'),
    url(r'^edit', views.edit, name='about'),
]