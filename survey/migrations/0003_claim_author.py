# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-15 00:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('survey', '0002_remove_claim_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='claim',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
