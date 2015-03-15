# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ticker_symbol', models.CharField(max_length=5)),
                ('exchange_symbol', models.CharField(max_length=10)),
                ('instrument_id', models.IntegerField(default=0)),
                ('num_followers', models.IntegerField(default=0)),
                ('earnings_announcement', models.DateField(null=True, blank=True)),
                ('percent_change_historical', models.DecimalField(max_digits=11, decimal_places=5)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
