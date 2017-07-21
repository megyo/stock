# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-06 12:10
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20170706_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='termek',
            name='web_link',
            field=models.TextField(blank=True, null=True, validators=[django.core.validators.URLValidator()]),
        ),
    ]