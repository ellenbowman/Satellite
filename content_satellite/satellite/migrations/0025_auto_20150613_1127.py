# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0024_remove_ticker_coverage_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coveragetype',
            name='coverage_type',
            field=models.IntegerField(null=True, choices=[(1, b'10% Promise'), (2, b'5 and 3'), (3, b'Earnings Preview'), (4, b'Earnings Review'), (5, b'Risk Rating')]),
            preserve_default=True,
        ),
    ]
