from django.conf.urls import url
from pawpals import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^shelters$', views.shelters, name='shelters'),
    url(r'^$', views.home, name='home'),
    url(r'^about', views.about, name='about'),
    url(r'^login/$',auth_views.LoginView.as_view(template_name='pawpals/login.html'), name='login'),
    url(r'^register/$',views.register,name='register'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'home'}, name='logout'),    #redirects to homepage
    url(r'^shelters/(?P<shelter_slug>[\w\-]+)/$', views.show_shelter, name='show_shelter'),
    url(r'^dogs/(?P<dog_slug>[\w\-]+)/$', views.show_dog, name='show_dog'),
    url(r'^edit', views.edit, name='edit'),
    url(r'^dogsearch/$',views.dog_search, name='dogSearch'),
    url(r'^ajax/show_reviews/', views.show_reviews, name = "show_reviews")
]
