from django.shortcuts import render

# Create your views here.

""" INDEX FUNCTION FOR HOME PAGE """


def index(request):
    # projectlist = Project.objects.all()
    template = 'front/index.html'
    # context = {'project_list' : projectlist }

    return render(request, template)


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
