from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from datetime import datetime
from realtor.models import Realtor


# Create your models here.
PROPERTY_CATEGORY = (
    ("Plot", "Plot"),
    ("Apartment", "Apartment"),
    ("Frame", "Frame"),
    ("Auto-Mobile", "Auto-Mobile"),
    ("House", "House"),
)


PROPERTY_TYPE = (
    ("For Rent", "For Rent"),
    ("For Sale", "For Sell"),
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
    # for product category
    category_name = models.CharField(max_length=50, choices=PROPERTY_CATEGORY)
    #image = models.ImageField(upload_to='category/', blank=True, null=True)
    """
    slug = models.SlugField(blank=True  , null=True)


    def save(self , *args , **kwargs):
        if not self.slug and self.category_name :
            self.slug = slugify(self.category_name)
        super(Category , self).save(*args , **kwargs)
    """
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name
