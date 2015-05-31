# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0012_auto_20150505_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date_pub',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
