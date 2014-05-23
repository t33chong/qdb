from django import forms
from django.contrib.auth.models import User

from app.models import Quote


class QuoteForm(forms.ModelForm):
    tag_string = forms.CharField()

    class Meta:
        model = Quote
        fields = ('text', 'tag_string')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
