from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
User = get_user_model()

# Create your models here.

class Policeprofile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    service_id = models.CharField(max_length=10,unique=True)
    first_name = models.CharField(max_length=100,null = True,blank=True)
    image = models.ImageField(null=True,blank=True, upload_to="images/")

    last_name= models.CharField(max_length=50,null = True,blank=True)
    rank = models.CharField(max_length=20,null = True,blank=True)
    

    def __str__(self):
        return f"{self.first_name}"
    

class CitizenProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    first_name= models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=50,null=True,blank=True)
    ghana_card_id = models.CharField(max_length=30,null=True,blank=True)
    ghana_card_image_front = models.ImageField(null=True,blank = True,upload_to="ghana_card_frontImage/")
    ghana_card_image_back = models.ImageField(null=True,blank = True,upload_to="ghana_card_backImage/")
    drivers_linence_id = models.CharField(max_length=10,blank=True,null=True)
    driver_linence_Image_front = models.ImageField(null=True,blank = True,upload_to="drivers_linence_Image/")
    postal_address = models.CharField(max_length=50,null=True,blank=True)
    phone_number = models.CharField(max_length=10,null=True,blank=True)


    def __str__(self):
        return f"{self.first_name}"
    

