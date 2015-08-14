# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('risk_ratings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hint',
            name='function_name',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
    ]
