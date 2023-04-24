from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.
class WeatherModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=20)

    # def __str__(self):
    #     return str(self.user)

