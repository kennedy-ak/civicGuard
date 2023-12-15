from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
User = get_user_model()

# Create your models here.

class PaidOffenses(models.Manager):
    def get_queryset(self):
        return super(PaidOffenses, self).get_queryset().filter(status='fine_paid')

class PendingOffenses(models.Manager):
    def get_queryset(self):
        return super(PendingOffenses, self).get_queryset().filter(status='pending_payment')
   

class Policeprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    service_id = models.CharField(max_length=10,unique=True)
    first_name = models.CharField(max_length=100,null = True,blank=True)
    image = models.ImageField(null=True,blank=True, upload_to="images/")

    last_name= models.CharField(max_length=50,null = True,blank=True)
    rank = models.CharField(max_length=20,null = True,blank=True)
    

    def __str__(self):
        return f"{self.first_name}"
    

class CitizenProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=30, null=True,blank=True)
    first_name= models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(default=True, null=True)
    last_name = models.CharField(max_length=50,null=True,blank=True)
    ghana_card_id = models.CharField(max_length=30,null=True,blank=True,unique=True)
    ghana_card_image_front = models.ImageField(null=True,blank = True,upload_to="ghana_card_frontImage/")
    ghana_card_image_back = models.ImageField(null=True,blank = True,upload_to="ghana_card_backImage/")
    drivers_license_id = models.CharField(max_length=10,blank=True,null=True)
    driver_license_Image_front = models.ImageField(null=True,blank = True,upload_to="drivers_linence_Image/")
    postal_address = models.CharField(max_length=50,null=True,blank=True)
    phone_number = models.CharField(max_length=10,null=True,blank=True)


    def __str__(self):
        return f"{self.first_name}"
    
class Complains(models.Model):
    STATUS_CHOICES = (
        ('pending_payment', 'Pending'),
        ('fine_paid', 'Paid')
    )

    officer = models.ForeignKey(Policeprofile, on_delete=models.PROTECT)
    citizens = models.ForeignKey(CitizenProfile, null=True, blank=True, on_delete=models.PROTECT)
    region = models.CharField(max_length=30)
    land_mark = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30,
                              choices=STATUS_CHOICES,
                              default='pending_payment', blank=True, null=True)
    objects = models.Manager()  # default manager
    fine_paid = PaidOffenses()
    pending = PendingOffenses()

    def __str__(self):
        return f"{self.officer}-{self.citizens}"

    