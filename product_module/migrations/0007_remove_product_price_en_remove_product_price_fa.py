# Generated by Django 4.1.5 on 2023-03-22 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0006_product_brand_en_product_brand_fa_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price_en',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price_fa',
        ),
    ]
