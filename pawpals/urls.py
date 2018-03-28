from django.conf.urls import url
from pawpals import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # General pages for basic interactions such as browsing to home, about, login and logout
    url(r'^shelters$', views.shelters, name='shelters'),
    url(r'^$', views.home, name='home'),
    url(r'^about', views.about, name='about'),
    url(r'^request/(?P<dog_slug>[\w\-]+)/$', views.request, name='request'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^login/requests/$', views.show_requests, name='requests'),
    url(r'^logout/', auth_views.logout, {'next_page': 'home'}, name='logout'),    #redirects to homepage

    # Pages to delete user accounts and dogs
    url(r'^delete/$', views.deactivate_user, name='deactivate_user'),
    url(r'^delete_dog/(?P<dog_slug>[\w\-]+)/$', views.remove_dog, name='remove_dog'),

    # pages related to reviews (adding and deleting reviews)
    url(r'^add-review/(?P<request_pk>[\w\-]+)$', views.add_review, name="add_review"),
    url(r'^edit-review/(?P<request_pk>[\w\-]+)$', views.edit_review, name="edit_review"),

    # Account registration and management pages
    url(r'^register/$',views.register,name='register'),
    url(r'^professional/$',views.professional,name='professional'),
    url(r'^personal/$',views.personal,name='personal'),
    url(r'^edit/$', views.edit, name='edit'),

    # Main entity pages (dogs and shelter displays)
    url(r'^shelters/(?P<shelter_slug>[\w\-]+)/$', views.show_shelter, name='show_shelter'),
    url(r'^dogs/(?P<dog_slug>[\w\-]+)/$', views.show_dog, name='show_dog'),
    url(r'^dogs/$',views.dog_search, name='dogs'),

    # AJAX version of reviews and dogs pages
    url(r'^ajax/show_reviews/', views.show_reviews, name = "show_reviews"),
    url(r'^ajax/get_dogs/', views.get_dogs, name = "get_dogs"),


]
