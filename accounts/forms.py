from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

from string import Template
from django.utils.safestring import mark_safe


class UserRegisterForm(UserCreationForm):

    email = forms.EmailInput(attrs={'class': 'input', 'required': True})
    username = forms.CharField(max_length=30)

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input-text', 'autofocus': True, 'placeholder': 'Enter your usernmae', }),
            'password1': forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-text'})),
            'password2': forms.CharField(label="Repeat password", widget=forms.PasswordInput(attrs={'class': 'input-text'}))
        }


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailInput(attrs={})

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', ]:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={}),
        }


class ProfileUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs['class'] = 'upload'

    image = forms.ImageField(label=False, required=False, error_messages={
                             'invalid': ("Image files only")}, widget=forms.FileInput)
    name = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'name', }))
    title = forms.CharField(
        label="Your Title", widget=forms.TextInput(attrs={'id': 'title', }))
    phone = forms.IntegerField(
        label="Phone", widget=forms.TextInput(attrs={'id': 'phone', }))
    description = forms.CharField(
        label="About Me",
        widget=forms.Textarea(attrs={
            'id': 'about',
            'rows': '10',
            'cols': '30'
        }))

    class Meta:
        model = Profile
        fields = ['image', 'name', 'title', 'phone', 'description']
