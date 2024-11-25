from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class BaseModal(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    deleted_time = models.DateTimeField(null=True)
    deleted_status = models.BooleanField(default=False)
    updated_time = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        abstract = True


class Configuration(BaseModal):
    parent = models.CharField(max_length=150, null=True)
    child = models.ForeignKey(
        "Configuration",
        on_delete=models.SET_NULL,
        null=True,
        related_name="parent_name",
    )



class RoleUserMapping(BaseModal):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="user_mapped"
    )
    role = models.ForeignKey(
        Configuration, on_delete=models.SET_NULL, null=True, related_name="role_mapped"
    )
