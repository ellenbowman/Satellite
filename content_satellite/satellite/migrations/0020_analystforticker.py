# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0019_ticker_analysts_for_ticker'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalystForTicker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('analyst', models.CharField(max_length=50)),
                ('guide', models.BooleanField(default=False)),
                ('service', models.ForeignKey(to='satellite.Service')),
                ('ticker', models.ForeignKey(to='satellite.Ticker')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
