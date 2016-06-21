# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_auto_20160617_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='pand',
            name='bouwjaar',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pand',
            name='oppervlakte',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
    ]
