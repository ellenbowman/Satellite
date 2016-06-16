# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0037_auto_20160426_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticker',
            name='earnings_announcement',
            field=models.CharField(max_length=30, null=True, verbose_name=b'next earnings date', blank=True),
            preserve_default=True,
        ),
    ]
