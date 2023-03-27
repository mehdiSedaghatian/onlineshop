# Generated by Django 4.1.5 on 2023-02-04 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('site_module', '0002_alter_sitesetting_site_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='FooterLinkBox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='footer link box')),
            ],
            options={
                'verbose_name': 'footer link box',
                'verbose_name_plural': 'footer link boxes',
            },
        ),
        migrations.AlterField(
            model_name='sitesetting',
            name='address',
            field=models.CharField(max_length=200, verbose_name=' address'),
        ),
        migrations.CreateModel(
            name='FooterLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('url', models.URLField(max_length=500, verbose_name='url')),
                ('footer_link_box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='site_module.footerlinkbox', verbose_name='footer link box')),
            ],
            options={
                'verbose_name': 'footer link ',
                'verbose_name_plural': 'footer links ',
            },
        ),
    ]
