from django.contrib import admin
from .models import Property, Category, PropertyImages

# Register your models here.

admin.site.register(Property)
admin.site.register(Category)
admin.site.register(PropertyImages)
