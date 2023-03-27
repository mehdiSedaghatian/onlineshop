from django.db import models


# Create your models here.
class ContactUs(models.Model):
    email = models.EmailField(max_length=300, verbose_name='email')
    full_name = models.CharField(max_length=300, verbose_name='full name ')
    message = models.TextField(verbose_name='message')
    title = models.CharField(max_length=300, verbose_name='title')
    is_read_by_admin = models.BooleanField(verbose_name='is read by admin', default=False)
    response = models.BooleanField(verbose_name='response', null=True, blank=True)
    create_date = models.DateTimeField(verbose_name='create date', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'contact us '
        verbose_name_plural = 'list contact us'


class UserProfile(models.Model):
    image = models.ImageField(upload_to='images')
