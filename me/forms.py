from django import forms
from .models import Policeprofile, CitizenProfile, Complains, get_user_model
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm

class ProfileCreationForm(forms.Form):
    image = forms.ImageField()
    rank = forms.CharField(label="Rank")
    first_name = forms.CharField(label="First Nanme",)
    last_name = forms.CharField(label="Last Name")


class CitizenCreationForm(forms.Form):
    first_name = forms.CharField(label="First Name", )
    last_name = forms.CharField(label="Last Name")
    email = forms.EmailField(label="Enter your valid email")
    ghana_card_id = forms.CharField(label="Ghana Card Id")
    ghana_card_image_front= forms.ImageField()
    ghana_card_image_back= forms.ImageField()
    drivers_license_id = forms.CharField(label="Drivers license Id")
    drivers_license_image= forms.ImageField()   
    post_address = forms.CharField(label="Postal Address")
    phone_number = forms.CharField(label="Phone Number")

    



# class ComplainsForm(forms.ModelForm):
#     citizen = forms.CharField(label="Enter Citizens Drivers ID")
#     description = forms.CharField(label="Enter Offense")
#     region = forms.CharField(label="Region")
#     landmark = forms.CharField(label="Landmark")


class ComplainsForm(forms.ModelForm):
    citizen_id = forms.CharField(label='Citizen ID', max_length=20)  # Add a CharField for manual input

    class Meta:
        model = Complains
        fields = ['officer', 'citizen_id', 'region', 'land_mark', 'fine_paid']


class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['newpassword1','new_password2']
