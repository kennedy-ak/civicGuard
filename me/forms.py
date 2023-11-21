from django import forms
from .models import Policeprofile

class ProfileCreationForm(forms.Form):
    image = forms.ImageField()
    rank = forms.CharField(label="Rank")
    first_name = forms.CharField(label="First Nanme",)
    last_name = forms.CharField(label="Last Name")