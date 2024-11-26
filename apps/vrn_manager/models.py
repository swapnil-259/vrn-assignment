from django.db import models
from apps.vrn_common.models import BaseModal
from django.contrib.auth.models import User

# Create your models here.
class Organization(BaseModal):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='org_user')
    name = models.CharField(max_length=50)
    phone_number = models.PositiveBigIntegerField(null=True)
    address = models.CharField(max_length=200)
    description = models.CharField(max_length=150)

class Events(BaseModal):
    org = models.ForeignKey(Organization,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    start_date = models.DateTimeField(null=True)
    end_date= models.DateTimeField(null=True)
    location = models.CharField(max_length=200)
    capacity = models.PositiveBigIntegerField(default=0)
    is_cancelled = models.BooleanField(default=False)