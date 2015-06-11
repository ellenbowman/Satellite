# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0022_ticker_coverage_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoverageType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('coverage_type', models.IntegerField(choices=[(1, b'10% Promise'), (2, b'5 and 3'), (3, b'Earnings Preview'), (4, b'Earnings Review'), (5, b'Risk Rating')])),
                ('service', models.ForeignKey(to='satellite.Service')),
                ('ticker', models.ForeignKey(to='satellite.Ticker')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
