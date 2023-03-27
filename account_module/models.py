from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = models.ImageField(upload_to='images/profile', verbose_name='avatar', null=True, blank=True)
    email_active_code = models.CharField(max_length=100, verbose_name='email active code')
    about_user = models.TextField(null=True, blank=True, verbose_name='about user')
    address = models.TextField(null=True, blank=True, verbose_name='address')

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        if self.first_name is not '' and self.last_name is not '':
            return self.get_full_name()
        return self.email
