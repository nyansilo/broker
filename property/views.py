from django.shortcuts import render

# Create your views here.
""" INDEX FUNCTION FOR HOME PAGE """


def propertylist(request):
    # projectlist = Project.objects.all()
    template = 'property/property-list.html'
    # context = {'project_list' : projectlist }

    return render(request, template)
