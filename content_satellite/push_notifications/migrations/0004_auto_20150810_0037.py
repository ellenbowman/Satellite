# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('push_notifications', '0003_auto_20150809_2347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notificationsubscriber',
            name='email_address',
        ),
        migrations.RemoveField(
            model_name='notificationsubscriber',
            name='name',
        ),
    ]
