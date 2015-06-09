# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0020_analystforticker'),
    ]

    operations = [
        migrations.RenameField(
            model_name='analystforticker',
            old_name='analyst',
            new_name='priority',
        ),
    ]
