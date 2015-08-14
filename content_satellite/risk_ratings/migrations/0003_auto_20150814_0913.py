# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('risk_ratings', '0002_auto_20150814_0511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticker',
            name='exchange',
            field=models.CharField(max_length=20),
            preserve_default=True,
        ),
    ]
