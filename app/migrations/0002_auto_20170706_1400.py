# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-06 12:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beszallito',
            name='beszallito_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
