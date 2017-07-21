# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-06 11:54
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Beszallito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beszallito_nev', models.CharField(max_length=255)),
                ('beszallito_cim', models.CharField(blank=True, max_length=255, null=True)),
                ('beszallito_ugyintezo', models.CharField(blank=True, max_length=255, null=True)),
                ('beszallito_email', models.CharField(blank=True, max_length=255, null=True)),
                ('beszallito_telefon', models.CharField(blank=True, max_length=255, null=True)),
                ('megjegyzes', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Beszállítók',
            },
        ),
        migrations.CreateModel(
            name='Bevetel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bevetel_mennyiseg', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('ar_bevetel_netto', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('eladas_datum', models.DateField()),
                ('szallitolevel_szam', models.CharField(blank=True, max_length=255, null=True)),
                ('megjegyzes', models.TextField(blank=True, null=True)),
                ('beszallito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Beszallito')),
            ],
            options={
                'verbose_name_plural': 'Bételezés',
            },
        ),
        migrations.CreateModel(
            name='Ertekesit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eladas_mennyiseg', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('ar_eladas_brutto', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('eladas_datum', models.DateField()),
                ('megjegyzes', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Értékesítések',
            },
        ),
        migrations.CreateModel(
            name='Raktar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raktar_nev', models.CharField(max_length=255, unique=True)),
                ('megjegyzes', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Raktárak',
            },
        ),
        migrations.CreateModel(
            name='Raktarkeszlet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keszlet', models.IntegerField()),
                ('raktar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Raktar')),
            ],
            options={
                'verbose_name_plural': 'Raktárkészlet',
            },
        ),
        migrations.CreateModel(
            name='Termek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('termek_nev', models.CharField(max_length=255)),
                ('gyari_cikkszam', models.CharField(max_length=255)),
                ('sajat_cikkszam', models.CharField(blank=True, max_length=255, null=True)),
                ('ar_web_netto', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('ar_bolt_brutto', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('elhelyezes', models.CharField(max_length=255)),
                ('min_keszlet', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('mennyisegi_egyseg', models.CharField(choices=[('', 'Kérem válasszon'), ('csomag', 'Csomag'), ('db', 'db'), ('kg', 'Kilogramm'), ('meter', 'Méter')], max_length=255)),
                ('mennyiseg', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('web_link', models.CharField(blank=True, max_length=255, null=True)),
                ('megjegyzes', models.TextField(blank=True, null=True)),
                ('aktiv', models.BooleanField()),
            ],
            options={
                'verbose_name_plural': 'Termékek',
            },
        ),
        migrations.CreateModel(
            name='TermekKategoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('termekkategoria', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Termék kategóriák',
            },
        ),
        migrations.AddField(
            model_name='termek',
            name='termekkategoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.TermekKategoria'),
        ),
        migrations.AddField(
            model_name='raktarkeszlet',
            name='termek',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Termek'),
        ),
        migrations.AddField(
            model_name='ertekesit',
            name='raktar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Raktar'),
        ),
        migrations.AddField(
            model_name='ertekesit',
            name='termek',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Termek'),
        ),
        migrations.AddField(
            model_name='bevetel',
            name='raktar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Raktar'),
        ),
        migrations.AddField(
            model_name='bevetel',
            name='termek',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Termek'),
        ),
        migrations.AlterUniqueTogether(
            name='termek',
            unique_together=set([('gyari_cikkszam', 'termek_nev')]),
        ),
    ]
