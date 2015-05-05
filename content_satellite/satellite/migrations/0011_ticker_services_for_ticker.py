# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0010_auto_20150501_0703'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticker',
            name='services_for_ticker',
            field=models.CharField(max_length=200, null=True, verbose_name=b'services for ticker', blank=True),
            preserve_default=True,
        ),
    ]
