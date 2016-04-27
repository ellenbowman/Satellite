# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0035_auto_20151017_2247'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticker',
            name='cloud_captain',
            field=models.CharField(max_length=50, null=True, verbose_name=b'cloud captain', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticker',
            name='points',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticker',
            name='sector',
            field=models.TextField(max_length=500, null=True, verbose_name=b'sector', blank=True),
            preserve_default=True,
        ),
    ]
