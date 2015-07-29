# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0029_auto_20150712_1308'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
    ]
