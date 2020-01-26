from django.db import models
from datetime import datetime

# Create your models here.


class Realtor(models.Model):

    # contain all the proprties informations
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    district = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    photo = models.ImageField(
        upload_to='realtor/%Y/%m/%d/', blank=True, null=True)
    #created = models.DateTimeField(default=timezone.now)
    is_mvp = models.BooleanField(default=False)
    created = models.DateTimeField(default=datetime.now)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.first_name
