from django.db import models
from apps.vrn_common.models import BaseModal
from apps.vrn_manager.models import Events
from django.contrib.auth.models import User


class Registration(BaseModal):
    event = models.ForeignKey(Events,on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='registered_user')
    is_cancelled = models.BooleanField(default=False)

