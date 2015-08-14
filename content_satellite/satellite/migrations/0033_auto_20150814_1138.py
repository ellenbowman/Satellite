# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0032_ticker_promised_coverage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticker',
            name='promised_coverage',
            field=models.TextField(max_length=500, null=True, verbose_name=b'promised coverage', blank=True),
            preserve_default=True,
        ),
    ]
