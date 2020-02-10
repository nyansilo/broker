from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib import messages


from .models import Property, PropertyImages, Category
from .choices import bedroom_choices, bathroom_choices, status_choices, type_choices, room_choices


# Create your views here.

def is_valid_queryparam(param):
    return param != '' and param is not None


""" FILTER FUNCTION FOR SEARCHINGLISTING PROPERTIS """


def filter(request):
    qs = Property.objects.all()
    tab1 = request.GET.get('tab') == 'Any Status'
    tab2 = request.GET.get('tab') == 'For Sale'
    tab3 = request.GET.get('tab') == 'For Rent'

    status = request.GET.get('status')
    keyword = request.GET.get('keyword')
    category = request.GET.get('category')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    area_min = request.GET.get('area_min')
    area_max = request.GET.get('area_max')
    bed = request.GET.get('bed')
    bath = request.GET.get('bath')
    room = request.GET.get('room')

    # not_reviewed = request.GET.get('notReviewed')

    if is_valid_queryparam(status) and status != 'Any Status':
        qs = qs.filter(property_type__contains=status)

    if is_valid_queryparam(keyword):
        qs = qs.filter(
            Q(address__icontains=keyword) |
            Q(title__icontains=keyword) |
            Q(description__icontains=keyword) |
            Q(realtor__first_name__icontains=keyword)
        ).distinct()

    if is_valid_queryparam(category) and category != 'Any Type':
        qs = qs.filter(category__category_name=category)

    if is_valid_queryparam(price_min):
        qs = qs.filter(price__gte=price_min)

    if is_valid_queryparam(price_max):
        qs = qs.filter(price__lt=price_max)

    if is_valid_queryparam(area_min):
        qs = qs.filter(sqft__gte=area_min)

    if is_valid_queryparam(area_max):
        qs = qs.filter(sqft__lt=area_max)

    if is_valid_queryparam(bed) and bed != 'Beds(Any)':
        qs = qs.filter(bedrooms__contains=bed)

    if is_valid_queryparam(bath) and bed != 'Baths (Any)':
        qs = qs.filter(bathrooms__contains=bath)

    if is_valid_queryparam(room) and room != 'Rooms (Any)':
        qs = qs.filter(rooms__contains=room)

    if tab1 == 'on':
        qs = qs.filter(property_type=tab1)

    elif tab2 == 'on':
        qs = qs.filter(property_type=tab2)

    elif tab3 == 'on':
        qs = qs.filter(property_type=tab3)

    """
    if reviewed == 'on':
        qs = qs.filter(reviewed=True)

    elif not_reviewed == 'on':
        qs = qs.filter(reviewed=False)
    """
    return qs


""" SEARCH LIST FUNCTION FOR LISTING PROPERTIS """


def search_list(request):
   # category = None
    propertytlist = filter(request)
    paginator = Paginator(propertytlist, 2)  # Show 25 contacts per page
    page = request.GET.get('page')

    propertytlist = paginator.get_page(page)

    template = 'property/search-list.html'
    context = {
        'property_list': propertytlist,
        'bedroom_choices': bedroom_choices,
        'bathroom_choices': bathroom_choices,
        'status_choices': status_choices,
        'type_choices': type_choices,
        'room_choices': room_choices,
    }
    return render(request, template, context)


""" PROPERTY LIST FUNCTION FOR LISTING PROPERTIS """


def property_list(request):

    # category = None

    propertytlist = Property.objects.all()
    featured_list = Property.objects.filter(
        featured=True).order_by('-featured')[:4]
    latest_list = Property.objects.order_by('-created')[:8]
    # propertyimages = PropertyImages.objects.filter(property=propertytlist)
    """
    categorylist = Category.objects.annotate(total_projects=Count('project'))

    if category_slug :
        category = get_object_or_404(Category ,slug=category_slug)
        projectlist = projectlist.filter(category=category)
    """

    paginator = Paginator(propertytlist, 2)  # Show 25 contacts per page
    page = request.GET.get('page')

    propertytlist = paginator.get_page(page)

    template = 'property/property-list.html'
    context = {'property_list': propertytlist}

    # context = {'project_list' : projectlist , 'category_list' : categorylist ,'category' : category }
    return render(request, template, context)


def property_detail(request, property_slug):
    print(property_slug)
    propertydetail = Property.objects.get(slug=property_slug)
    propertyimages = PropertyImages.objects.filter(property=propertydetail)
    template = 'property/property-detail.html'
    context = {'property_detail': propertydetail,
               'property_images': propertyimages}
    return render(request, template, context)


def user_property(request):

    propertytlist = Property.objects.all()
    # propertyimages = PropertyImages.objects.filter(property=propertytlist)
    """
        categorylist = Category.objects.annotate(total_projects=Count('project'))

        if category_slug :
            category = get_object_or_404(Category ,slug=category_slug)
            projectlist = projectlist.filter(category=category)
        """

    paginator = Paginator(propertytlist, 2)  # Show 25 contacts per page
    page = request.GET.get('page')

    propertytlist = paginator.get_page(page)

    template = 'accounts/my-property.html'
    context = {'property_list': propertytlist}

    # context = {'project_list' : projectlist , 'category_list' : categorylist ,'category' : category }
    return render(request, template, context)
