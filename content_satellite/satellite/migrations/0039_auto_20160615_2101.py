# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0038_auto_20160602_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticker',
            name='earnings_announcement',
            field=models.DateField(null=True, verbose_name=b'next earnings date ', blank=True),
            preserve_default=True,
        ),
    ]
