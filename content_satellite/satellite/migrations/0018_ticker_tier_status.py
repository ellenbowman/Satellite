# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0017_auto_20150531_2136'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticker',
            name='tier_status',
            field=models.CharField(max_length=50, null=True, verbose_name=b'tier status', blank=True),
            preserve_default=True,
        ),
    ]
