# Generated by Django 4.1.5 on 2023-02-12 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_module', '0005_slider_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('url', models.URLField(blank=True, max_length=400, null=True, verbose_name='url')),
                ('image', models.ImageField(upload_to='images/banners', verbose_name='baner')),
                ('is_active', models.BooleanField(verbose_name='active/disable')),
                ('position', models.CharField(choices=[('product_detail', 'product detail page'), ('product_list', 'product list page')], max_length=200, verbose_name='position')),
            ],
            options={
                'verbose_name': 'site banner',
                'verbose_name_plural': 'site banners',
            },
        ),
    ]
