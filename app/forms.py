from django import forms
from django.contrib.auth.models import User

from app.models import Quote, Tag


# TODO: Add ability to create new tags in quote form
class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ('text', 'tags')


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('text',)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
