# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0014_auto_20150530_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='date_time_pub',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
