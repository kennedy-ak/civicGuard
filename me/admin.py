from django.contrib import admin
from .models import Policeprofile,CitizenProfile, Complains
# Register your models here.

@admin.register(Policeprofile)

class PoliceprofileAdmin(admin.ModelAdmin):
    list_display = ('service_id','first_name','last_name','rank')
    search_fields = ('service_id',)
    list_filter = ('rank',)



@admin.register(CitizenProfile)
class CitzenAdmin(admin.ModelAdmin):
    list_display =('username','first_name','last_name','drivers_license_id','ghana_card_id','phone_number')
    search_fields = ('drivers_license_id','ghana_card_id')
    

@admin.register(Complains)

class ComplainsAdmin(admin.ModelAdmin):
    list_display = ('officer','citizens','date_created','region')
    search_fields = ('officer','citizens')
    list_filter =('citizens','officer','date_created')
