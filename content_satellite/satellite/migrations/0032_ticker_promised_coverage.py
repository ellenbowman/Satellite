# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0031_auto_20150730_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticker',
            name='promised_coverage',
            field=models.CharField(max_length=500, null=True, verbose_name=b'promised coverage', blank=True),
            preserve_default=True,
        ),
    ]
