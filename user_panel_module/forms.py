from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from account_module.models import User


class EditProfileModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar', 'address', 'about_user']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',

            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control'

            }),
            'about_user': forms.Textarea(attrs={
                'class': 'form-control'

            })
        }
        labels = {
            'first_name': _('name'),
            'last_name': _('last name'),
            'avatar': _('avatar'),
            'address': _('address')
        }


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label=_(' old password...'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }),
        validators=[

            validators.MaxLengthValidator(100)
        ]
    )
    new_password = forms.CharField(
        label=_('new password...'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        }),
        validators=[

            validators.MaxLengthValidator(100)
        ]
    )
    confirm_password = forms.CharField(
        label=_('confirm password...'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        }),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        raise ValidationError('password with confirm it is not match ')
