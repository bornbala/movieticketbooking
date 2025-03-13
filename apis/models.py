from django.db import models
from django.core.validators import validate_email


# Create your models here.
class User(models.Model):
    email = models.EmailField(unique=True,validators=[validate_email])
    password = models.CharField(max_length=255)