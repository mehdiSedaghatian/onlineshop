# Generated by Django 4.1.5 on 2023-02-04 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_module', '0004_slider'),
    ]

    operations = [
        migrations.AddField(
            model_name='slider',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='active/disable'),
        ),
    ]