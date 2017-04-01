# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-04-01 12:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0012_pand_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pand',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
