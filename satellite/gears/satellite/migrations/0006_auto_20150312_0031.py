# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0005_auto_20150312_0320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticker',
            name='percent_change_historical',
            field=models.DecimalField(max_digits=11, decimal_places=3),
            preserve_default=True,
        ),
    ]
