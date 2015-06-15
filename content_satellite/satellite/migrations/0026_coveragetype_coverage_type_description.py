# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0025_auto_20150613_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='coveragetype',
            name='coverage_type_description',
            field=models.CharField(max_length=100, null=True, choices=[(1, b'10% Promise'), (2, b'5 and 3'), (3, b'Earnings Preview'), (4, b'Earnings Review'), (5, b'Risk Rating')]),
            preserve_default=True,
        ),
    ]
