# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20160617_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pand',
            name='beschrijving',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]
