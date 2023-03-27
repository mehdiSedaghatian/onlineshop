from django import forms
from django.utils.translation import gettext_lazy as _
from contact_module.models import ContactUs


class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['full_name', 'email', 'message', 'title']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'message'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control'

            })
        }
        labels = {
            'full_name': _('name'),
            'email': _('your email'),
            'title': _('title...'),
            'message': _('your message')
        }

        error_messages = {
            'full_name': {
                'required': 'you must fill it',
                'max_length': 'fuck you'
            }
        }

# class ContactUsForm(forms.Form):
#     full_name = forms.CharField(label='what is your name?', max_length=20, error_messages={
#         'required': 'please fill the blank',
#         'max_length': 'oh it is more than 50 char'
#     },
#
#                                 widget=forms.TextInput(attrs={
#                                     'class': 'form-control',
#                                     'placeholder': 'name...'
#                                 }))
#     email = forms.EmailField(label='emaillllll', widget=forms.EmailInput(attrs={
#         'class': 'form-control',
#         'placeholder': 'email...'
#     }))
#     subject = forms.CharField(label='subject...', widget=forms.TextInput(attrs={
#         'class': 'form-control',
#         'placeholder': 'subject...'
#     }))
#     text = forms.CharField(label='message',
#                            widget=forms.Textarea(attrs={
#                                'class': 'form-control',
#                                'placeholder': 'text...',
#                                'id': 'message'
#                            }))
# class ProfileForm(forms.Form):
#     user_image = forms.ImageField()
