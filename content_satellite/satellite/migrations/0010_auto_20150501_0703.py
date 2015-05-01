# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0009_dataharvesteventlog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataharvesteventlog',
            name='data_type',
            field=models.IntegerField(default=1, choices=[(1, b'articles import'), (2, b'market performance'), (3, b'earnings dates'), (4, b'scorecard recs')]),
            preserve_default=True,
        ),
    ]
