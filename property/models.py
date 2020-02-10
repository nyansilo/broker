from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from datetime import datetime
from realtor.models import Realtor
from django.urls import reverse
from autoslug import AutoSlugField


# Create your models here.
PROPERTY_CATEGORY = (

    ("Lands", "Lands"),
    ("Apartments", "Apartments"),
    ("Commercials", "Commercials"),
    ("Vehicles", "Vehicles"),

)

PROPERTY_SUB_CATEGORY = (
    ("Plot", "Plot"),
    ("Farm", "Farm"),
    ("Apartment", "Apartment"),
    ("House", "House"),
    ("Room", "Room"),
    ("Hostel", "Hostel"),
    ("Office Place", "Office Place"),
    ("Frame", "Frame"),
    ("Car", "Car"),
    ("Motorcycle", "Motorcycle"),
    ("Bajaji", "Bajaji"),
)


PROPERTY_TYPE = (
    ("For Rent", "For Rent"),
    ("For Sale", "For Sale"),
)


class Property(models.Model):

    # contain all the proprties informations
    realtor = models.ForeignKey(Realtor, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    district = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    property_type = models.CharField(max_length=501, choices=PROPERTY_TYPE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.IntegerField(blank=True)
    rooms = models.IntegerField(blank=True)
    bathrooms = models.IntegerField(blank=True)
    garage = models.IntegerField(default=0)
    sqft = models.IntegerField()
    lot_size = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True)
    photo_main = models.ImageField(
        upload_to='main_photo/%Y/%m/%d/', blank=True, null=True)
    #created = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created = models.DateTimeField(default=datetime.now)
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super(Property, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'

    def __str__(self):
        return self.title


class PropertyImages(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='property/%Y/%m/%d/', blank=True, null=True)

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = 'Property Image'
        verbose_name_plural = 'Property Images'


class Category(models.Model):
    category_name = models.CharField(max_length=50, choices=PROPERTY_CATEGORY)
    slug = AutoSlugField(populate_from='category_name', null=True)
    #image = models.ImageField(upload_to='category/', blank=True, null=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    title = models.CharField(max_length=50, choices=PROPERTY_SUB_CATEGORY)
    slug = AutoSlugField(populate_from='title', null=True)
    created = models.DateTimeField(default=datetime.now)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'sub category'
        verbose_name_plural = 'sub categories'

    def __str__(self):
        return self.title
