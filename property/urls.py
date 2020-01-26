from django.urls import path
from . import views

app_name = 'property'

urlpatterns = [
    path('property-list', views.propertylist, name='property_list'),
    path('property-detail/<slug:property_slug>',
         views.propertydetail, name='property_detail'),
    #path('<slug:category_slug>' , views.productlist , name='product_list_category') ,
    #path('detail/<slug:product_slug>' , views.productdetail , name='product_detail'),
    #path('allprojects/', views.ProjectListApiView.as_view()),



]
