from django import forms

from app.models import Quote, Tag


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ('text', 'tags')


# TODO: Add ability to create new tags in quote form
