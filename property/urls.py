from django.urls import path
from . import views

app_name = 'property'

urlpatterns = [
    path('property-list', views.propertylist, name='propertylist'),


]
