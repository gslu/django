# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-04 11:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0018_postclass'),
    ]

    operations = [
    ]
