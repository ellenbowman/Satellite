# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0034_auto_20151017_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataharvesteventlog',
            name='data_type',
            field=models.IntegerField(default=1, choices=[(1, b'articles'), (2, b'market performance'), (3, b'earnings dates'), (4, b'new recs/status changes'), (5, b'bylines meta data'), (6, b'tier status')]),
            preserve_default=True,
        ),
    ]
