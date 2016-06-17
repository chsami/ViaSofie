# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20160617_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='foto_url',
            field=models.ImageField(upload_to=None),
        ),
    ]
