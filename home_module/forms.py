from django import forms
from django.utils.translation import gettext_lazy as _


class SearchForm(forms.Form):
    search = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        label=_('search...')

    )
