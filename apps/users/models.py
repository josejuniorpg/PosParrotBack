from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

class User(AbstractUser, TimeStampedModel):
    """Default user for Pos System, this is the owner of the restaurants."""
    email = models.EmailField(_("email address"), unique=True)
    profile_image = models.ImageField(upload_to='users/profileImages', blank=True, null=True)