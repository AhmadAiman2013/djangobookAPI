from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
         ("user", "User"),
        ("author", "Author")
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")

class Books(models.Model):
    
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(decimal_places=0, max_digits=3)
    genre = models.CharField(max_length=100)
    publication_date = models.DateField()
    

