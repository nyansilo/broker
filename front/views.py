from django.shortcuts import render
from property.models import Property

# Create your views here.

""" INDEX FUNCTION FOR HOME PAGE """


def index(request):
    proplist = Property.objects.order_by('-created')[:8]
    template = 'front/index.html'
    context = {'prop_list': proplist}
    return render(request, template, context)


""" ABOUT FUNCTION FOR ABOUT PAGE """


def about(request):
    # projectlist = Project.objects.all()
    template = 'front/about.html'
    # context = {'project_list' : projectlist }

    return render(request, template)


""" CONTACT FUNCTION FOR CONATACT US PAGE """


def contact(request):
    # projectlist = Project.objects.all()
    template = 'front/contact.html'
    # context = {'project_list' : projectlist }

    return render(request, template)
