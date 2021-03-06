# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-22 15:45
from __future__ import unicode_literals

from django.db import migrations, models
import system.storage


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20171022_0732'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='motto',
            field=models.CharField(blank=True, default='\u65e0', max_length=50, verbose_name='\u5ea7\u53f3\u94ed'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('M', '\u7537'), ('F', '\u5973'), ('S', '\u4fdd\u5bc6')], default='S', max_length=10, verbose_name='\u6027\u522b'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, storage=system.storage.ImageStorage(), upload_to='image/user', verbose_name='\u5934\u50cf'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='nickname',
            field=models.CharField(blank=True, default='\u672a\u540d', max_length=20, verbose_name='\u6635\u79f0'),
        ),
    ]
