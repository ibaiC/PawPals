from django.contrib import admin
from pawpals.models import *
from django.contrib.admin.templatetags.admin_modify import prepopulated_fields_js

class DogAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", "id")}

admin.site.register(Dog, DogAdmin)
admin.site.register(Shelter)
admin.site.register(ShelterManagerUser)
admin.site.register(StandardUser)
admin.site.register(Review)
admin.site.register(Request)


