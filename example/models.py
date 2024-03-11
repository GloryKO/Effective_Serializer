from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048)
    release_date = models.DateField()
    rating = models.PositiveSmallIntegerField()

    us_gross = models.IntegerField(default=0)
    worldwide_gross = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title}'
    

class Resource(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    liked_by = models.ManyToManyField(to=User)

    def __str__(self):
        return f'{self.title}'
    

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    bio = models.TextField()
    birth_date = models.DateField()

    def __str__(self):
        return f'{self.user.username} profile'