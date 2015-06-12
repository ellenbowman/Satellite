# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0023_coveragetype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticker',
            name='coverage_type',
        ),
    ]
