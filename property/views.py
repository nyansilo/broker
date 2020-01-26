from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib import messages


from .models import Property, PropertyImages, Category


# Create your views here.
""" INDEX FUNCTION FOR HOME PAGE """


def propertylist(request):

   #category = None
    propertytlist = Property.objects.all()
    #propertyimages = PropertyImages.objects.filter(property=propertytlist)
    """
    categorylist = Category.objects.annotate(total_projects=Count('project'))

    if category_slug :
        category = get_object_or_404(Category ,slug=category_slug)
        projectlist = projectlist.filter(category=category)
   
    search_query = request.GET.get('q')
    if search_query :
        projectlist = projectlist.filter(
            Q(name__icontains = search_query) |
            Q(description__icontains = search_query)|
            Q(condition__icontains = search_query)|
            Q(brand__brand_name__icontains = search_query) |
            Q(category__category_name__icontains = search_query) 
        )

    paginator = Paginator(projectlist, 1) # Show 25 contacts per page
    page = request.GET.get('page')

    projectlist = paginator.get_page(page)
    """
    template = 'property/property-list.html'
    context = {'property_list': propertytlist}

    #context = {'project_list' : projectlist , 'category_list' : categorylist ,'category' : category }
    return render(request, template, context)


def propertydetail(request, property_slug):
    print(property_slug)
    propertydetail = Property.objects.get(slug=property_slug)
    propertyimages = PropertyImages.objects.filter(property=propertydetail)
    template = 'property/property-detail.html'
    context = {'property_detail': propertydetail,
               'property_images': propertyimages}
    return render(request, template, context)
