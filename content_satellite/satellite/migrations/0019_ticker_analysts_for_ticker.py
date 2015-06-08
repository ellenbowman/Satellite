# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0018_ticker_tier_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticker',
            name='analysts_for_ticker',
            field=models.CharField(max_length=500, null=True, verbose_name=b'analysts for ticker', blank=True),
            preserve_default=True,
        ),
    ]
