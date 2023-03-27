# Generated by Django 4.1.5 on 2023-01-22 15:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='title')),
                ('price', models.IntegerField(verbose_name='price')),
                ('short_description', models.CharField(db_index=True, max_length=300, null=True, verbose_name='short description')),
                ('description', models.TextField(db_index=True, verbose_name='description')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, max_length=200, unique=True, verbose_name='title in url')),
                ('is_active', models.BooleanField(default=False, verbose_name='active / not active')),
                ('is_delete', models.BooleanField(verbose_name='is delete / is not delete')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
            },
        ),
        migrations.CreateModel(
            name='ProductBrand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=300, verbose_name='title')),
                ('url_title', models.CharField(db_index=True, max_length=300, verbose_name='title in url')),
                ('is_active', models.BooleanField(verbose_name='active / not active')),
            ],
            options={
                'verbose_name': 'brand',
                'verbose_name_plural': 'brands',
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=300, verbose_name='title')),
                ('url_title', models.CharField(db_index=True, max_length=300, verbose_name='url in title')),
                ('is_active', models.BooleanField(verbose_name='active / not active')),
                ('is_delete', models.BooleanField(verbose_name='delete / not delete')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='ProductVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=30, verbose_name='user ip')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_module.product', verbose_name='product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'product visit',
                'verbose_name_plural': 'products visit',
            },
        ),
        migrations.CreateModel(
            name='ProductTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(db_index=True, max_length=300, verbose_name='title')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_tags', to='product_module.product')),
            ],
            options={
                'verbose_name': 'products tag',
                'verbose_name_plural': 'products tags',
            },
        ),
        migrations.CreateModel(
            name='ProductGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/product-gallery', verbose_name='image')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_module.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'gallery',
                'verbose_name_plural': 'galleries',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(related_name='product_categories', to='product_module.productcategory', verbose_name='categories'),
        ),
    ]