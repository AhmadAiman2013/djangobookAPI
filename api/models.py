from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
         ("user", "User"),
        ("author", "Author")
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")



