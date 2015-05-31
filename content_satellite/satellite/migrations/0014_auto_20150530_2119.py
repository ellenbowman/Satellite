# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0013_auto_20150530_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date_pub',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
