# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-26 17:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('voornaam', models.CharField(max_length=128)),
                ('naam', models.CharField(max_length=128)),
                ('email', models.CharField(max_length=128, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('straatnaam', models.CharField(max_length=128)),
                ('huisnr', models.IntegerField()),
                ('busnr', models.CharField(blank=True, max_length=10)),
                ('telefoonnr', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Foto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Handelstatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('logText', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('straatnaam', models.CharField(max_length=128)),
                ('huisnr', models.SmallIntegerField()),
                ('handelstatus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Handelstatus')),
            ],
        ),
        migrations.CreateModel(
            name='PandType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pandtype', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Stad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postcode', models.SmallIntegerField()),
                ('stadsnaam', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagnaam', models.CharField(max_length=128)),
                ('Pand', models.ManyToManyField(to='webapp.Pand')),
            ],
        ),
        migrations.CreateModel(
            name='Voortgang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=128)),
            ],
        ),
        migrations.AddField(
            model_name='pand',
            name='pandtype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.PandType'),
        ),
        migrations.AddField(
            model_name='pand',
            name='postcodeID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Stad'),
        ),
        migrations.AddField(
            model_name='pand',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pand',
            name='voortgang',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Voortgang'),
        ),
        migrations.AddField(
            model_name='foto',
            name='pand',
            field=models.ManyToManyField(to='webapp.Pand'),
        ),
        migrations.AddField(
            model_name='user',
            name='postcode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Stad'),
        ),
    ]
