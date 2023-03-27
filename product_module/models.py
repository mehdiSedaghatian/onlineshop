from django.db import models
from django.urls import reverse
from account_module.models import User
from django.utils.translation import gettext_lazy as _


# Create your models here.
class ProductCategory(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name=_('title'))
    url_title = models.CharField(max_length=300, db_index=True, verbose_name='url in title')
    is_active = models.BooleanField(verbose_name='active / not active')
    is_delete = models.BooleanField(verbose_name='delete / not delete')

    def __str__(self):
        return f'{self.title} _ {self.url_title}'

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class ProductBrand(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name=_('title'))
    url_title = models.CharField(max_length=300, verbose_name='title in url', db_index=True)
    is_active = models.BooleanField(verbose_name='active / not active')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'brand'
        verbose_name_plural = 'brands'


class Product(models.Model):
    title = models.CharField(max_length=300, verbose_name=_('title'))
    image = models.ImageField(upload_to='images/products', verbose_name='image', null=True, blank=True)
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, verbose_name='brand', null=True, blank=True)
    category = models.ManyToManyField(ProductCategory, related_name='product_categories', verbose_name='category')
    price = models.IntegerField(verbose_name='price')
    short_description = models.CharField(max_length=300, db_index=True, null=True, verbose_name=_('short description'))
    description = models.TextField(verbose_name=_('description'), db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, allow_unicode=True, unique=True, null=False, blank=True,
                            verbose_name='title in url')
    is_active = models.BooleanField(verbose_name='active / not active', default=False)
    is_delete = models.BooleanField(verbose_name='is delete / is not delete')

    def get_absolute_url(self):
        return reverse('product-detail', args=[self.slug])

    def save(self, *args, **kwargs):
        # self.slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}({self.price})'

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'


class ProductTag(models.Model):
    caption = models.CharField(verbose_name='title', max_length=300, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_tags')

    def __str__(self):
        return self.caption

    class Meta:
        verbose_name = 'products tag'
        verbose_name_plural = 'products tags'


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='product')
    image = models.ImageField(verbose_name='image', upload_to='images/product-gallery')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'gallery'
        verbose_name_plural = 'galleries'


class ProductVisit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='product')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user', null=True, blank=True)
    ip = models.CharField(max_length=30, verbose_name='user ip')

    def __str__(self):
        return f"{self.product} / {self.id}"

    class Meta:
        verbose_name = 'product visit'
        verbose_name_plural = 'products visit'



