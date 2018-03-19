from django.contrib import admin
from pawpals.models import *
from django.contrib.admin.templatetags.admin_modify import prepopulated_fields_js
from django.contrib.admin.helpers import AdminReadonlyField

class DogAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class ShelterAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Dog, DogAdmin)
admin.site.register(Shelter, ShelterAdmin)
admin.site.register(Review)
admin.site.register(Request)


