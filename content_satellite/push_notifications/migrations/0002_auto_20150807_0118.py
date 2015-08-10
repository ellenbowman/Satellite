# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('push_notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickermovementrule',
            name='message_today',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tickermovementrule',
            name='timestamp_satisfied',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tickermovementrule',
            name='condition',
            field=models.CharField(default=(b'gt', b'better than'), max_length=5, choices=[(b'gt', b'better than'), (b'lt', b'worse than')]),
            preserve_default=True,
        ),
    ]
