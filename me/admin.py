from django.contrib import admin
from .models import Policeprofile,CitizenProfile, Complains
# Register your models here.
admin.site.register(Policeprofile)
admin.site.register(CitizenProfile)

admin.site.register(Complains)