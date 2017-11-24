# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-22 14:24
from __future__ import unicode_literals

from django.db import migrations, models
import system.storage


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0026_auto_20171117_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picturerecord',
            name='picture',
            field=models.ImageField(blank=True, storage=system.storage.ImageStorage(), upload_to='article_image', verbose_name='\u56fe\u7247'),
        ),
    ]
