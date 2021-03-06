# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-23 03:39
from __future__ import unicode_literals

from django.db import migrations, models
import system.storage


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20171022_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bgimg',
            field=models.ImageField(blank=True, storage=system.storage.ImageStorage(), upload_to='image/bg_img', verbose_name='\u80cc\u666f'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, storage=system.storage.ImageStorage(), upload_to='image/user_img', verbose_name='\u5934\u50cf'),
        ),
    ]
