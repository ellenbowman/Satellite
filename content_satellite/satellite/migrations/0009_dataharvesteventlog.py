# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0008_auto_20150501_0535'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataHarvestEventLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_type', models.IntegerField(default=1, choices=[(1, b'articles import'), (2, b'market performance'), (3, b'earnings dates')])),
                ('date_started', models.DateTimeField(auto_now_add=True)),
                ('date_finished', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(max_length=5000, null=True, blank=True)),
            ],
            options={
                'ordering': ['-date_started'],
            },
            bases=(models.Model,),
        ),
    ]
