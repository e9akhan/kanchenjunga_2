"""
    Module name :- models
"""


from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class CustomUser(models.Model):
    """
        Custom User Model.
    """
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
