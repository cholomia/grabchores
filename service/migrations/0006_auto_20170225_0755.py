# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-24 23:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('service', '0005_merge_20170223_0727'),
    ]

    operations = [
        migrations.AddField(
            model_name='userratingavail',
            name='availer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='availer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userratingrender',
            name='render',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='render', to=settings.AUTH_USER_MODEL),
        ),
    ]