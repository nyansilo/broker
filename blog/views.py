from django.shortcuts import render

# Create your views here.
""" INDEX FUNCTION FOR HOME PAGE """


def bloglist(request):
    # projectlist = Project.objects.all()
    template = 'blog/blog.html'
    # context = {'project_list' : projectlist }

    return render(request, template)
