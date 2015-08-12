# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('push_notifications', '0004_auto_20150810_0037'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationsubscriber',
            name='is_active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
