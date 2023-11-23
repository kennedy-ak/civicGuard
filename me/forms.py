from django import forms
from .models import Policeprofile, CitizenProfile

class ProfileCreationForm(forms.Form):
    image = forms.ImageField()
    rank = forms.CharField(label="Rank")
    first_name = forms.CharField(label="First Nanme",)
    last_name = forms.CharField(label="Last Name")


class CitizenCreationForm(forms.Form):
    first_name = forms.CharField(label="First Nanme", )
    last_name = forms.CharField(label="Last Name")
    ghana_card_id = forms.CharField(label="Ghana Card Id")
    ghana_card_image_front= forms.ImageField()
    ghana_card_image_back= forms.ImageField()
    drivers_license_id = forms.CharField(label="Drivers license Id")
    drivers_license_image= forms.ImageField()   
    post_address = forms.CharField(label="Postal Address")
    phone_number = forms.CharField(label="Phone Number")

    