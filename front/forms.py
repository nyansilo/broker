from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={
        'required': True,
        'placeholder': 'Your Name',
        'id': 'name',
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'required': True,
        'pattern': '^[A-Za-z0-9](([_\.\-]?[a-zA-Z0-9]+)*)@([A-Za-z0-9]+)(([\.\-]?[a-zA-Z0-9]+)*)\.([A-Za-z]{2,})$',
        'placeholder': 'Email Address',
        'id': 'email',
    }))
    subject = forms.CharField(widget=forms.TextInput(attrs={
        'required': True,
        'placeholder': 'Subject',
        'id': 'subject',
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'spellcheck': True,
        'required': True,
        'placeholder': 'Type your message',
        'id': 'comments',
        'rows': '3',
        'cols': '40'
    }))

    class Meta:
        model = Contact
        fields = ('name', 'email', 'subject', 'message', )
