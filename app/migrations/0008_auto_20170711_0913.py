# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-11 07:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20170711_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bevetel',
            name='bevetel_mennyiseg',
            field=models.DecimalField(decimal_places=2, max_digits=9),
        ),
        migrations.AlterField(
            model_name='ertekesit',
            name='eladas_mennyiseg',
            field=models.DecimalField(decimal_places=2, max_digits=9),
        ),
        migrations.AlterField(
            model_name='raktarkeszlet',
            name='keszlet',
            field=models.DecimalField(decimal_places=2, max_digits=9),
        ),
    ]
