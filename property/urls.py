from django.urls import path
from . import views

app_name = 'property'

urlpatterns = [
    path('my-property', views.user_property, name='user_property'),
    path('property-search', views.search_list, name='property_search'),
    path('property-list', views.property_list, name='property_list'),
    path('property-detail/<slug:property_slug>',
         views.property_detail, name='property_detail'),

    #path('<slug:category_slug>' , views.productlist , name='product_list_category') ,
    #path('detail/<slug:product_slug>' , views.productdetail , name='product_detail'),


]
