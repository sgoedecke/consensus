# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-08 01:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0007_claim_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claim',
            name='type',
            field=models.BooleanField(),
        ),
    ]