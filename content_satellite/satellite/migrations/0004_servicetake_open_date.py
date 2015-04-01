# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0003_ticker_company_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicetake',
            name='open_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
