from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class RegisterForm(forms.Form):
    email = forms.EmailField(
        label=_('email...'),
        widget=forms.EmailInput(),
        validators=[
            validators.EmailValidator,
            validators.MaxLengthValidator(100)
        ]
    )
    password = forms.CharField(
        label=_('password...'),
        widget=forms.PasswordInput(),
        validators=[

            validators.MaxLengthValidator(100)
        ]
    )
    confirm_password = forms.CharField(
        label=_('confirm password...'),
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        raise ValidationError('password with confirm it is not match ')


class LoginForm(forms.Form):
    email = forms.EmailField(
        label=_('email...'),
        widget=forms.EmailInput(),
        validators=[
            validators.EmailValidator,
            validators.MaxLengthValidator(100)
        ]
    )
    password = forms.CharField(
        label=_('password...'),
        widget=forms.PasswordInput(),
        validators=[

            validators.MaxLengthValidator(100)
        ]
    )


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label=_('email...'),
        widget=forms.EmailInput(),
        validators=[
            validators.EmailValidator,
            validators.MaxLengthValidator(100)
        ]
    )


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        label=_('password...'),
        widget=forms.PasswordInput(),
        validators=[

            validators.MaxLengthValidator(100)
        ]
    )
    confirm_password = forms.CharField(
        label=_('confirm password...'),
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        raise ValidationError('password with confirm it is not match ')
