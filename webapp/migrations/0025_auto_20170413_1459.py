# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-04-13 12:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0024_auto_20170413_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='telefoonnr',
            field=models.CharField(max_length=128),
        ),
    ]
