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
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books',
                                           to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='postclass',
            name='post',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='blog.Post'),
        ),
        migrations.AlterField(
            model_name='postclass',
            name='post_type',
            field=models.CharField(
                choices=[('self', '\u539f\u521b'), ('reprint', '\u8f6c\u8f7d'), ('collect', '\u6536\u85cf')],
                default='self', max_length=10),
        ),
        migrations.AlterField(
            model_name='postclass',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='classes',
                                    to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='book',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='posts', to='blog.Book'),
        ),
    ]
