from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from smtplib import SMTPException
from django.template.loader import get_template
from django.shortcuts import render, redirect, reverse
import sweetify


from property.models import Property
from property.choices import bedroom_choices
from property.choices import bathroom_choices
from property.choices import status_choices
from property.choices import type_choices

from .models import Contact
from .forms import ContactForm

# Create your views here.

""" INDEX FUNCTION FOR HOME PAGE """


def index(request):
    proplist = Property.objects.order_by('-created')[:8]
    template = 'front/index.html'
    context = {
        'prop_list': proplist,
        'bedroom_choices': bedroom_choices,
        'bathroom_choices': bathroom_choices,
        'status_choices': status_choices,
        'type_choices': type_choices,
    }
    return render(request, template, context)


""" ABOUT FUNCTION FOR ABOUT PAGE """


def about(request):
    # projectlist = Project.objects.all()
    template = 'front/about.html'
    # context = {'project_list' : projectlist }

    return render(request, template)


""" CONTACT FUNCTION FOR CONATACT US PAGE """


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')

            subject = subject
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [from_email, 'danielgeuza808@gmail.com']
            sweetify.success(
                request,
                icon='success',
                title='Your message has been sent, we will get back to you soon',
                confirmButtonText='False',
                showConfirmButton='False',
                timer=4000
            )

            # option 1

            # contact_message = "{0}, from {1} with email {2}".format(
            #   message, name, email)

            # option 2
            """
            ctx = {
                'user': name,
                'email': email,
                'message': message
            }

            contact_message = get_template('contact_message.txt').render(ctx)

            try:
                send_mail(subject, contact_message, from_email,
                          recipient_list, fail_silently=False)

            except SMTPException as e:
                print('There was an error sending an email: ', e)
                sweetify.error(
                    request,
                    icon='error',
                    title='error',
                    confirmButtonText='False',
                    showConfirmButton='False',
                    timer=3000
                )
                return e

            sweetify.success(
                request,
                icon='success',
                title='Your message has been sent, we will get back to you soon',
                confirmButtonText='False',
                showConfirmButton='False',
                timer=4000
            )
            """
            return redirect(reverse("front:contact"))
    else:
        form = ContactForm()

    template = 'front/contact.html'
    context = {
        'form': form,
        'title': 'Contacts',
    }
    return render(request, template, context)


"""
def contact(request):

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        contact = Contact(name=name, email=email,
                          subject=subject, message=message)

        contact.save()

        # Email ourselves the submitted contact message

        subject = subject
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [from_email, 'danielgeuza808@gmail.com']

        # option 1

        # contact_message = "{0}, from {1} with email {2}".format(
        #   message, name, email)

        # option 2

        context = {
            'user': name,
            'email': email,
            'message': message
        }

        contact_message = get_template('contact_message.txt').render(context)

        try:
            send_mail(subject, contact_message, from_email,
                      recipient_list, fail_silently=False)

        except SMTPException as e:
            print('There was an error sending an email: ', e)
            sweetify.error(
                request,
                icon='error',
                title='error',
                confirmButtonText='False',
                showConfirmButton='False',
                timer=3000
            )
            return e

        sweetify.success(
            request,
            icon='success',
            title='Your message has been sent, we will get back to you soon',
            confirmButtonText='False',
            showConfirmButton='False',
            timer=4000
        )
        return redirect(reverse("front:contact"))

    template = 'front/contact.html'
    return render(request, template)
"""
