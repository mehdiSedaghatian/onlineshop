from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class SiteSetting(models.Model):
    site_name = models.CharField(verbose_name='site name', max_length=200)
    site_url = models.CharField(verbose_name='site url', max_length=200)
    address = models.CharField(verbose_name=' address', max_length=200)
    phone = models.CharField(verbose_name='phone', null=True, blank=True, max_length=200)
    fax = models.CharField(verbose_name='fax', null=True, blank=True, max_length=200)
    email = models.CharField(verbose_name='email', null=True, blank=True, max_length=200)
    copyright = models.TextField(verbose_name='copyright')
    about_us_text = models.TextField(verbose_name='a bout us')
    site_logo = models.ImageField(upload_to='images/site_setting', verbose_name='logo')
    is_main_setting = models.BooleanField(verbose_name='main setting')

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = 'site setting'
        verbose_name_plural = 'site settings'


class FooterLinkBox(models.Model):
    title = models.CharField(max_length=200, verbose_name='footer link box')

    class Meta:
        verbose_name = 'footer link box'
        verbose_name_plural = 'footer link boxes'

    def __str__(self):
        return self.title


class FooterLink(models.Model):
    title = models.CharField(max_length=200, verbose_name='title')
    url = models.URLField(verbose_name='url', max_length=500, )
    footer_link_box = models.ForeignKey(FooterLinkBox, on_delete=models.CASCADE, verbose_name='footer link box')

    class Meta:
        verbose_name = 'footer link '
        verbose_name_plural = 'footer links '

    def __str__(self):
        return self.title


class Slider(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('title'))
    description = models.TextField(verbose_name=_('description'))
    url = models.URLField(verbose_name='url', max_length=200)
    url_title = models.CharField(verbose_name=_('url title'), max_length=200)
    image = models.ImageField(upload_to='images/sliders', verbose_name='image')
    is_active = models.BooleanField(default=True, verbose_name='active/disable')

    class Meta:
        verbose_name = 'slider'
        verbose_name_plural = 'sliders'

    def __str__(self):
        return self.title


class SiteBanner(models.Model):
    class SiteBannerPosition(models.TextChoices):
        product_detail = 'product_detail', 'product detail page'
        product_list = 'product_list', 'product list page'

    title = models.CharField(max_length=200, verbose_name='title')
    url = models.URLField(max_length=400, verbose_name='url', null=True, blank=True)
    image = models.ImageField(upload_to='images/banners', verbose_name='baner')
    is_active = models.BooleanField(verbose_name='active/disable')
    position = models.CharField(max_length=200, choices=SiteBannerPosition.choices, verbose_name='position')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'site banner'
        verbose_name_plural = 'site banners'
