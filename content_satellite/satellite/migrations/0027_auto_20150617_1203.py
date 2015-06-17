# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0026_coveragetype_coverage_type_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coveragetype',
            name='coverage_type_description',
        ),
        migrations.AddField(
            model_name='coveragetype',
            name='author',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Analyst', blank=True),
            preserve_default=True,
        ),
    ]
